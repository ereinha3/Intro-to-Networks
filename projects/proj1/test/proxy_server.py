"""CS 532 Programming Assignment 1 HTTP Proxy.

Author: Ethan Reinhart
Date: 2025-10-31

This module implements a lightweight HTTP/1.x proxy with basic caching.
It supports forwarding GET and POST requests, preserves origin error/redirect
responses, and stores successful GET responses on disk for future cache hits.

Example:
    $ python proxy_server.py 8888
    Ready to serve...
"""

from socket import *
import os
import sys


# Size of socket read/write chunks to balance throughput vs. memory usage.
BUFFER_SIZE = 4096
# Cache directory lives alongside this script so relative paths remain stable.
CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")


def ensure_cache_dir():
    """Create the cache directory if it does not already exist.

    Example:
        >>> ensure_cache_dir()
    """

    # Create the cache once so individual handler calls just touch the files.
    if not os.path.isdir(CACHE_DIR):
        os.makedirs(CACHE_DIR)


def split_headers_and_body(raw_bytes):
    """Split raw HTTP data into header bytes and body bytes.

    Args:
        raw_bytes: Complete HTTP message as bytes.

    Returns:
        Tuple ``(head_bytes, body_bytes)``.

    Example:
        >>> split_headers_and_body(b"GET / HTTP/1.0\r\n\r\nbody")
        (b'GET / HTTP/1.0\r\n\r\n', b'body')
    """

    # Standard CRLF CRLF sequence separates headers from body.
    separator = b"\r\n\r\n"
    index = raw_bytes.find(separator)
    if index == -1:
        return raw_bytes, b""
    cut = index + len(separator)
    return raw_bytes[:cut], raw_bytes[cut:]


def read_request(sock):
    """Read a full HTTP request (headers and optional body) from a client.

    Args:
        sock: Connected client socket.

    Returns:
        Raw request bytes, or ``b""`` if the socket closes early.

    Example:
        >>> data = read_request(client_socket)
    """

    sock.settimeout(5.0)
    buffer = bytearray()

    try:
        # Read until we capture the blank line that terminates the headers.
        while b"\r\n\r\n" not in buffer:
            chunk = sock.recv(BUFFER_SIZE)
            if not chunk:
                return b""
            buffer.extend(chunk)

        head, body = split_headers_and_body(bytes(buffer))
        headers_text = head.decode("iso-8859-1", "ignore")
        content_length = 0
        for line in headers_text.split("\r\n"):
            if line.lower().startswith("content-length:"):
                try:
                    content_length = int(line.split(":", 1)[1].strip())
                except ValueError:
                    content_length = 0
                break

        # If the request carries a body (e.g., POST), read the remaining bytes.
        while len(body) < content_length:
            chunk = sock.recv(BUFFER_SIZE)
            if not chunk:
                break
            buffer.extend(chunk)
            head, body = split_headers_and_body(bytes(buffer))
    except OSError:
        return b""

    return bytes(buffer)


def parse_target(message):
    """Parse the request line to extract method, host, port, and path.

    Args:
        message: Full HTTP request text as a string.

    Returns:
        A tuple ``(method, host, port, resource, cache_name, version)`` when the
        request contains an absolute HTTP URL. Returns ``None`` for unsupported
        or malformed requests.

    Example:
        >>> parse_target('GET /http://example.com/ HTTP/1.1\r\n\r\n')
        ('GET', 'example.com', 80, '/', 'example.com_80__', 'HTTP/1.1')
    """

    # Split on CRLF so we can inspect the request line and headers.
    lines = message.splitlines()
    if not lines:
        return None

    request_parts = lines[0].split()
    if len(request_parts) < 2:
        return None

    method = request_parts[0].upper()
    target = request_parts[1].lstrip("/")
    version = request_parts[2] if len(request_parts) >= 3 else "HTTP/1.0"

    if target.startswith("http://"):
        raw_path = target[len("http://") :]
    elif target.startswith("https://"):
        return None
    else:
        return None

    if not raw_path:
        return None

    if "/" in raw_path:
        # Separate host[:port] from the origin-form path.
        host_port, resource = raw_path.split("/", 1)
        resource = "/" + resource
    else:
        host_port, resource = raw_path, "/"

    if ":" in host_port:
        host, port_str = host_port.split(":", 1)
        try:
            port = int(port_str)
        except ValueError:
            port = 80
    else:
        host = host_port
        port = 80

    # Construct a simple cache key that encodes host, port, and path.
    cache_name = f"{host}_{port}_{resource.replace('/', '_')}"
    if not cache_name:
        cache_name = "index.html"

    return method, host, port, resource, cache_name, version


def cache_path(name):
    """Return a filesystem-safe cache filename for the requested resource.

    Example:
        >>> cache_path('example.com_80__index.html')
        '/.../cache/example.com_80__index.html'
    """

    # Strip directory traversal characters to keep cache writes in-bounds.
    safe = name.replace("..", "").strip("/")
    if not safe:
        safe = "index.html"
    return os.path.join(CACHE_DIR, safe)


def send_cached_response(client_sock, path):
    """Send the cached response from disk if present.

    Returns:
        ``True`` when the cache handled the response, ``False`` otherwise.
    """

    # Nothing cached yet; caller must fetch from origin.
    if not os.path.isfile(path):
        return False

    try:
        with open(path, "rb") as cached:
            while True:
                chunk = cached.read(BUFFER_SIZE)
                if not chunk:
                    break
                client_sock.sendall(chunk)
        print("Read from cache")
        return True
    except OSError:
        return False


def build_origin_request(method, resource, version, head_bytes, body_bytes, host_header):
    """Construct the request to forward to the origin server.

    Args:
        method: HTTP method (e.g., ``GET`` or ``POST``).
        resource: Path portion of the URL.
        version: HTTP version string.
        head_bytes: Original request headers (including request line).
        body_bytes: Request body.
        host_header: Host header string (e.g., ``example.com`` or ``host:port``).

    Returns:
        Bytes ready to send to the origin server.

    Example:
        >>> build_origin_request('GET', '/', 'HTTP/1.1', b'...', b'', 'example.com')
    """

    header_text = head_bytes.decode("iso-8859-1", "ignore")
    # Skip the original request line so we can rebuild it in origin-form.
    header_lines = header_text.split("\r\n")[1:]

    forward_headers = []
    connection_added = False
    for line in header_lines:
        if not line:
            continue
        name, _, value = line.partition(":")
        if not _:
            continue
        lname = name.lower()
        if lname in {"proxy-connection", "connection"}:
            continue
        if lname == "host":
            continue
        forward_headers.append(f"{name}:{value}")
        if lname == "connection":
            connection_added = True

    forward_headers.append(f"Host: {host_header}")
    if not connection_added:
        forward_headers.append("Connection: close")

    # Rebuild the HTTP request line using origin-form path.
    request_line = f"{method} {resource} {version}"
    origin_head = "\r\n".join([request_line] + forward_headers) + "\r\n\r\n"
    return origin_head.encode("iso-8859-1") + body_bytes


def forward_to_origin(host, port, payload):
    """Send the prepared request to the origin server and return the response.

    Example:
        >>> forward_to_origin('example.com', 80, b'GET / HTTP/1.0\r\n\r\n')
    """

    with socket(AF_INET, SOCK_STREAM) as origin_sock:
        origin_sock.connect((host, port))
        origin_sock.sendall(payload)

        response = bytearray()
        while True:
            data = origin_sock.recv(BUFFER_SIZE)
            if not data:
                break
            response.extend(data)

    return bytes(response)


def log_request_summary(message):
    """Print a concise summary of the incoming client request.

    Example:
        >>> log_request_summary('GET /http://example.com HTTP/1.1\r\nHost: ...')
    """

    lines = message.splitlines()
    if not lines:
        return

    request_line = lines[0]
    host_line = next((line for line in lines if line.lower().startswith("host:")), "")
    referer_line = next((line for line in lines if line.startswith("Referer:")), "")

    print(request_line)
    if host_line:
        print(host_line)
    if referer_line:
        print(referer_line)


def should_cache(method, response_bytes):
    """Decide whether to cache the origin response.

    Args:
        method: HTTP method used for the request.
        response_bytes: Raw origin response bytes.

    Returns:
        ``True`` when the response should be cached.

    Example:
        >>> should_cache('GET', b'HTTP/1.0 200 OK\r\n\r\n')
        True
    """

    # Only cache idempotent GET requests to keep semantics simple.
    if method != "GET":
        return False

    head, _ = split_headers_and_body(response_bytes)
    try:
        status_line = head.decode("iso-8859-1", "ignore").split("\r\n", 1)[0]
    except IndexError:
        return False
    return " 200 " in status_line


def handle_client(client_sock):
    """Handle a single client connection.

    Args:
        client_sock: Connected client socket created by ``accept``.

    Example:
        >>> handle_client(client_socket)
    """

    # Pull the full request off the wire, including any body.
    raw_request = read_request(client_sock)
    if not raw_request:
        return

    request_text = raw_request.decode("iso-8859-1", "ignore")
    log_request_summary(request_text)

    target = parse_target(request_text)
    if not target:
        try:
            client_sock.sendall(b"HTTP/1.0 400 Bad Request\r\nConnection: close\r\n\r\n")
        except OSError:
            pass
        return

    method, host, port, resource, cache_name, version = target

    if method == "CONNECT":
        response = (
            b"HTTP/1.0 501 Not Implemented\r\nConnection: close\r\n\r\n"
            b"CONNECT not supported by this proxy.\n"
        )
        try:
            client_sock.sendall(response)
        except OSError:
            pass
        return

    if method not in {"GET", "POST", "HEAD"}:
        response = (
            b"HTTP/1.0 501 Not Implemented\r\nConnection: close\r\n\r\n"
            b"Only GET, HEAD, and POST are supported.\n"
        )
        try:
            client_sock.sendall(response)
        except OSError:
            pass
        return

    # Repurpose the original request into something the origin understands.
    head_bytes, body_bytes = split_headers_and_body(raw_request)
    host_header = f"{host}:{port}" if port != 80 else host
    origin_payload = build_origin_request(method, resource, version, head_bytes, body_bytes, host_header)

    cache_file = cache_path(cache_name)
    if method == "GET" and send_cached_response(client_sock, cache_file):
        return

    print(f"Cache miss -> fetching {host}:{port}{resource}")
    try:
        response = forward_to_origin(host, port, origin_payload)
    except OSError:
        try:
            client_sock.sendall(b"HTTP/1.0 502 Bad Gateway\r\nConnection: close\r\n\r\n")
        except OSError:
            pass
        return

    if should_cache(method, response):
        try:
            with open(cache_file, "wb") as cached_file:
                cached_file.write(response)
            print(f"Cached response at {cache_file}")
        except OSError:
            pass

    try:
        client_sock.sendall(response)
    except OSError:
        pass


def main():
    """Entry point: start the proxy server and accept connections.

    Example:
        >>> main()
    """

    if len(sys.argv) != 2:
        print('Usage : "python proxy_server.py port"\n[port : It is the Port Number of Proxy Server]')
        sys.exit(2)

    try:
        listen_port = int(sys.argv[1])
    except ValueError:
        print("Port must be an integer.")
        sys.exit(2)

    ensure_cache_dir()

    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(("", listen_port))
    tcpSerSock.listen(1)

    while True:
        print("Ready to serve...")
        tcpCliSock, addr = tcpSerSock.accept()
        print("Received a connection from:", addr)
        with tcpCliSock:
            handle_client(tcpCliSock)
        print()


if __name__ == "__main__":
    main()

