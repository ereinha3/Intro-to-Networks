# CS 532 Programming Assignment 1 — HTTP Proxy

Author: Ethan Reinhart  
Date: October 31, 2025

This project implements a lightweight HTTP/1.x proxy server with on-disk caching. The proxy forwards GET, HEAD, and POST requests, preserves origin status lines (including redirects and 404s), and caches successful GET responses so repeat requests are served locally.

## Getting Started

```bash
python proxy_server.py <port>
```

Example:

```bash
python proxy_server.py 8888
```

Configure your HTTP client (browser or curl) to use `127.0.0.1:<port>` as its HTTP proxy.

## Demonstrating Task 1 (9 points)

| Requirement | Command / Evidence |
| ----------- | ------------------ |
| Respond to a GET request (2 pts) | `curl -x 127.0.0.1:8888 http://httpforever.com/ -I` → prints HTTP headers from origin via proxy. |
| GET an index webpage (3 pts) | `curl -x 127.0.0.1:8888 http://wikipedia.org/ -o wiki.html` → saves the index HTML; console shows proxy logs. |
| Return webpage response to client (3 pts) | Open Chrome set to the proxy and visit `http://127.0.0.1:8888/http://httpforever.com/`; take screenshot of rendered page and proxy terminal output. |
| GET an arbitrary page (1 pt) | `curl -x 127.0.0.1:8888 http://en.wikipedia.org/wiki/Computer_security -o security.html` → downloads article through proxy. |

## Demonstrating Task 2 (9 points)

| Requirement | Command / Evidence |
| ----------- | ------------------ |
| Error messages work (2 pts total) | `curl -x 127.0.0.1:8888 http://httpforever.com/missing` → origin 404 relayed by proxy. |
| 301 redirect (0.5 pts) | `curl -x 127.0.0.1:8888 http://httpbin.org/status/301 -I` → shows 301 status and `Location` header without bypassing proxy. |
| Other errors (404) (1.5 pts) | Same 404 command above; screenshot terminal output with status line and body. |
| POST support (2 pts) | `curl -x 127.0.0.1:8888 -X POST http://httpbin.org/post -d "name=proxy" -i` → returns JSON echo proving POST body forwarded. |
| Caching objects (2 pts) | First run: `curl -x 127.0.0.1:8888 http://httpforever.com/ -o /tmp/a.html` (terminal shows “Cache miss”). |
| Return cached object (3 pts) | Second run: same command; proxy prints “Read from cache” and `/cache/` directory contains saved file. |

## Tips for Screenshots / Submission

1. Start the proxy, then capture the terminal window showing `Ready to serve…` and request logs.  
2. In the browser, visit targets via `http://127.0.0.1:<port>/http://…` and screenshot the rendered page.  
3. Include curl command output demonstrating redirects, 404s, and POST JSON response.  
4. Show the `cache/` directory listing after GET requests to prove artifacts were saved.


