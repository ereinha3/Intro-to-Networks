#!/usr/bin/env python3
"""
CS 432/532 — Programming Assignment 1
HTTP Web Proxy Server with Caching and POST Support

Author: <Your Name>
Date: 2025-10-31
File: ProxyServer.py

Description
-----------
A minimal HTTP/1.0–HTTP/1.1 proxy that:
- Handles simple GET and POST requests
- Caches server responses to disk (no validation/replacement policy)
- Returns cached objects on cache hit
- Forwards error responses correctly (e.g., 404)
- Handles redirects (301/302/etc.) by forwarding (does not bypass proxy)
- Includes basic robustness (timeouts, header parsing) and multi-threading

Usage
-----
python ProxyServer.py <bind_ip> <port>

Examples
--------
Run the proxy on localhost:8888:
    python ProxyServer.py 127.0.0.1 8888

Then in your browser, set the HTTP proxy to 127.0.0.1:8888
—or— visit a URL through the proxy directly:
    http://localhost:8888/http://www.google.com/

Notes
-----
- HTTPS (CONNECT) is NOT implemented (out of scope for this assignment).
- Caching: GET responses are cached as raw bytes (status line + headers + body).
  POST responses are not cached by default.
"""

from __future__ import annotations

import os
import sys
import socket
import threading
import time
import hashlib
from http.client import HTTPResponse
from io import BytesIO

# ----------------------------- Configuration ---------------------------------

RECV_BUFSIZE = 65536         # 64 KiB chunks
SERVER_BACKLOG = 64
CONNECT_TIMEOUT = 8.0
IO_TIMEOUT = 20.0
CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# In-memory index: URL -> cache filepath
CACHE_INDEX: dict[str, str] = {}

# ----------------------------- Helper Functions ------------------------------

def safe_cache_path(url: str) -> str:
    """
    Map a URL to a stable, filesystem-safe cache file path.
    We use SHA-256 of the URL and keep an optional short prefix for readability.
    Example:
        >>> safe_cache_path("http://example.com/index.html").endswith(".cache")
        True
    """
    h = hashlib.sha256(url.encode("utf-8")).hexdigest()
    # include a short readable prefix from host/path (filtered)
    prefix = "".join(ch if ch.isalnum() else "_" for ch in url[:40])
    fname = f"{prefix}__{h}.cache"
    return os.path.join(CACHE_DIR, fname)


def parse_request_line(data: bytes) -> tuple[str, str, str]:
    """
    Parse the HTTP request line and return (method, url, version).

    The proxy expects 'absolute-form' for the request-target (RFC 7230 §5.3.2), e.g.:
        GET http://example.com/path HTTP/1.1
    For convenience, we also support "GET /http://example.com/path HTTP/1.1"
    (when user visits http://<proxy_host>:<port>/http://example.com/path)

    Raises ValueError if malformed.
    """
    try:
        line = data.split(b"\r\n", 1)[0].decode("iso-8859-1")
        parts = line.split()
        if len(parts) != 3:
            raise ValueError("Malformed request line")
        method, target, version = parts

        # Accept "proxy-prefix" style: /http://host/...
        if target.startswith("/") and target[1:].startswith(("http://", "https://")):
            target = target[1:]

        return method.upper(), target, version
    except Exception as e:
        raise ValueError(f"Bad request line: {e}")


def split_headers_and_body(raw: bytes) -> tuple[bytes, bytes]:
    """
    Split raw HTTP message bytes into (head, body) at the first CRLFCRLF.
    """
    sep = b"\r\n\r\n"
    i = raw.find(sep)
    if i == -1:
        return raw, b""
    return raw[: i + len(sep)], raw[i + len(sep):]


def read_all(sock: socket.socket, first_chunk: bytes) -> bytes:
    """
    Read the full HTTP request from client, including headers and body (if any).
    Stops once Content-Length is satisfied (for requests that carry a body).

    Returns complete raw bytes of the request.
    """
    sock.settimeout(IO_TIMEOUT)
    data = bytearray(first_chunk)

    # Read headers fully
    while b"\r\n\r\n" not in data:
        chunk = sock.recv(RECV_BUFSIZE)
        if not chunk:
            break
        data.extend(chunk)

    head, body = split_headers_and_body(bytes(data))
    # parse headers for Content-Length
    headers_text = head.decode("iso-8859-1", errors="replace")
    content_length = 0
    for line in headers_text.split("\r\n")[1:]:  # skip request line
        if not line:
            break
        k, _, v = line.partition(":")
        if k.lower() == "content-length":
            try:
                content_length = int(v.strip())
            except ValueError:
                content_length = 0
            break

    # Read remaining body if needed
    need = max(0, content_length - len(body))
    while need > 0:
        chunk = sock.recv(min(RECV_BUFSIZE, need))
        if not chunk:
            break
        body += chunk
        need -= len(chunk)

    return head + body


def build_origin_request(raw_client_req: bytes, method: str, url: str, version: str) -> bytes:
    """
    Convert absolute-form client request into origin-form request for the server,
    ensure Host header is set, and drop Proxy-Connection headers.
    """
    # Parse headers
    head, body = split_headers_and_body(raw_client_req)
    lines = head.decode("iso-8859-1").split("\r\n")
    req_line = lines[0]
    headers = lines[1:]

    # Extract host and path from URL
    # Basic parse (avoid importing urllib to keep it simple)
    if not url.startswith("http://"):
        # We don't support HTTPS CONNECT in this assignment.
        raise ValueError("Only http:// URLs are supported by this proxy.")

    # Strip scheme
    rest = url[len("http://") :]
    if "/" in rest:
        hostport, path = rest.split("/", 1)
        path = "/" + path
    else:
        hostport, path = rest, "/"

    # Split host:port (default 80)
    if ":" in hostport:
        host, port_s = hostport.rsplit(":", 1)
        try:
            port = int(port_s)
        except ValueError:
            port = 80
    else:
        host, port = hostport, 80

    # Rebuild request line in origin-form
    new_req_line = f"{method} {path} {version}"

    # Rebuild headers:
    new_headers = []
    have_host = False
    for h in headers:
        if not h:
            continue
        k, sep, v = h.partition(":")
        if not sep:
            continue
        lk = k.lower()
        # Remove hop-by-hop proxy headers
        if lk in ("proxy-connection", "proxy-authenticate", "proxy-authorization"):
            continue
        if lk == "connection":
            # We'll keep 'Connection: close' or pass-thru. It's OK.
            pass
        if lk == "host":
            have_host = True
        new_headers.append(f"{k}:{v}")

    if not have_host:
        new_headers.append(f"Host: {hostport}")

    # Close the origin connection after response for simplicity
    # (many servers honor this even for HTTP/1.1 if explicitly set)
    # Avoid persistent proxy<->server keepalives for assignment simplicity.
    forced_headers = []
    if not any(h.lower().startswith("connection:") for h in new_headers):
        forced_headers.append("Connection: close")

    # Assemble
    origin_head = "\r\n".join([new_req_line] + new_headers + forced_headers) + "\r\n\r\n"
    return origin_head.encode("iso-8859-1") + body


def connect_origin(host: str, port: int) -> socket.socket:
    """
    Create and return a TCP socket connected to (host, port) with a timeout.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(CONNECT_TIMEOUT)
    s.connect((host, port))
    s.settimeout(IO_TIMEOUT)
    return s


def origin_from_url(url: str) -> tuple[str, int, str]:
    """
    Return (host, port, path) parsed from http:// URL (simplified parse).
    """
    rest = url[len("http://") :]
    if "/" in rest:
        hostport, path = rest.split("/", 1)
        path = "/" + path
    else:
        hostport, path = rest, "/"
    if ":" in hostport:
        host, port_s = hostport.rsplit(":", 1)
        try:
            port = int(port_s)
        except ValueError:
            port = 80
    else:
        host, port = hostport, 80
    return host, port, path


def cache_get(url: str) -> bytes | None:
    """
    Return cached response bytes for URL if available, else None.
    """
    path = CACHE_INDEX.get(url)
    if path and os.path.isfile(path):
        try:
            with open(path, "rb") as f:
                return f.read()
        except OSError:
            return None
    return None


def cache_put(url: str, response_bytes: bytes) -> None:
    """
    Save response bytes to disk and update in-memory index.
    """
    path = safe_cache_path(url)
    try:
        with open(path, "wb") as f:
            f.write(response_bytes)
        CACHE_INDEX[url] = path
    except OSError:
        pass


def forward_response(client: socket.socket, data: bytes) -> None:
    """
    Send full HTTP response bytes to client.
    """
    total = 0
    mv = memoryview(data)
    while total < len(mv):
        sent = client.send(mv[total:])
        if sent <= 0:
            break
        total += sent


def handle_client(client_sock: socket.socket, client_addr: tuple[str, int]) -> None:
    """
    Handle a single client connection.
    """
    with client_sock:
        try:
            # Read initial data to get the request line & headers
            first = client_sock.recv(RECV_BUFSIZE)
            if not first:
                return

            method, url, version = parse_request_line(first)

            # Only support HTTP URLs (no CONNECT/HTTPS)
            if not url.startswith("http://"):
                resp = (b"HTTP/1.1 501 Not Implemented\r\n"
                        b"Connection: close\r\n"
                        b"Content-Type: text/plain\r\n\r\n"
                        b"Only plain HTTP (no TLS/CONNECT) is supported by this proxy.\n")
                client_sock.sendall(resp)
                return

            # Read complete request (including potential POST body)
            raw_client_req = read_all(client_sock, first)

            # Caching only for GET
            if method == "GET":
                cached = cache_get(url)
                if cached is not None:
                    print(f"[proxy] CACHE HIT -> {url}") 
                    forward_response(client_sock, cached)
                    return

            # Build request for origin
            origin_req = build_origin_request(raw_client_req, method, url, version)
            host, port, _ = origin_from_url(url)

            # Connect to origin and forward request
            with connect_origin(host, port) as origin_sock:
                origin_sock.sendall(origin_req)

                # Read full response
                chunks = []
                while True:
                    data = origin_sock.recv(RECV_BUFSIZE)
                    if not data:
                        break
                    chunks.append(data)
                response_bytes = b"".join(chunks)

            # Forward to client
            forward_response(client_sock, response_bytes)

            # Cache GET responses only (status 200 OK ideally)
            if method == "GET":
                try:
                    head, body = split_headers_and_body(response_bytes)
                    status_line = head.split(b"\r\n", 1)[0].decode("iso-8859-1", "replace")
                    # Cache only for 200 OK; skip errors and redirects
                    if " 200 " in status_line:
                        print(f"[proxy] CACHED (200) -> {url}") 
                        cache_put(url, response_bytes)
                except Exception:
                    # Be conservative: if parsing failed, do not cache
                    pass

        except socket.timeout:
            try:
                client_sock.sendall(b"HTTP/1.1 504 Gateway Timeout\r\nConnection: close\r\n\r\n")
            except Exception:
                pass
        except ValueError as e:
            msg = f"Bad Request: {e}\n".encode("utf-8", "replace")
            try:
                client_sock.sendall(b"HTTP/1.1 400 Bad Request\r\nConnection: close\r\nContent-Type: text/plain\r\n\r\n" + msg)
            except Exception:
                pass
        except Exception as e:
            # Generic error -> 502
            try:
                body = f"Proxy error: {type(e).__name__}: {e}\n".encode("utf-8", "replace")
                client_sock.sendall(b"HTTP/1.1 502 Bad Gateway\r\nConnection: close\r\nContent-Type: text/plain\r\n\r\n" + body)
            except Exception:
                pass


def serve(bind_ip: str, port: int) -> None:
    """
    Start the proxy server and accept clients forever.

    Example:
        >>> # serve("127.0.0.1", 8888)
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((bind_ip, port))
        server.listen(SERVER_BACKLOG)
        print(f"[Proxy] Listening on {bind_ip}:{port} (Ctrl+C to stop)")

        while True:
            try:
                client_sock, client_addr = server.accept()
                # Spawn a thread per connection (simple concurrency)
                t = threading.Thread(target=handle_client, args=(client_sock, client_addr), daemon=True)
                t.start()
            except KeyboardInterrupt:
                print("\n[Proxy] Shutting down...")
                break
            except Exception as e:
                print(f"[Proxy] Accept error: {e}", file=sys.stderr)


def main(argv: list[str]) -> int:
    """
    CLI entry point.
    """
    if len(argv) < 3:
        print("Usage: python ProxyServer.py <bind_ip> <port>")
        print("Example: python ProxyServer.py 127.0.0.1 8888")
        return 2
    bind_ip = argv[1]
    try:
        port = int(argv[2])
    except ValueError:
        print("Port must be an integer.", file=sys.stderr)
        return 2
    serve(bind_ip, port)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
