# CS 532 — Introduction to Computer Networks

Coursework archive for CS 532 (graduate networks), Fall 2025. Textbook: Kurose & Ross,
*Computer Networking: A Top-Down Approach*.

Contents: two programming projects (an HTTP proxy and a six-router forwarding simulation),
five homework sets, four paper reviews, and chapter notes for the whole course.

```
.
├── projects/
│   ├── proj1/          HTTP/1.x proxy server with on-disk caching
│   └── proj2/          Six-router packet forwarding simulation over TCP
├── homework/           HW1–HW5 (PDF)
├── paper-reviews/      Four paper reviews (PDF)
└── notes/              Chapter notes, questions, and solutions (Obsidian vault)
```

## Projects

### Project 1 — HTTP Proxy Server

`projects/proj1/` — A single-threaded HTTP/1.x forward proxy written against the Python
standard library only (no dependencies). It relays GET, HEAD, and POST; preserves origin
status lines including 301 redirects and 404s; refuses `CONNECT`, so there is no HTTPS
tunneling; and caches successful GET responses to disk so repeat requests are served locally.

```bash
cd projects/proj1
python3 proxy_server.py 8888
curl -x 127.0.0.1:8888 http://httpforever.com/     # "Cache miss" on the first request
curl -x 127.0.0.1:8888 http://httpforever.com/     # "Read from cache" on the second
```

Cached objects land in `projects/proj1/cache/` (gitignored — regenerated at runtime).
`template.py` is the instructor-provided skeleton; `proxy_server.py` is the submitted work.
`screenshots/` holds the demo captures from the submission, and `projects/proj1/README.md`
maps each rubric line item to the command that demonstrates it.

The proxy does not set `SO_REUSEADDR`, so restarting it on the same port immediately after
stopping it can fail with `Address already in use` until the socket leaves `TIME_WAIT`.

### Project 2 — Router Forwarding Simulation

`projects/proj2/` — Six Python processes emulate a network of routers communicating over TCP
on loopback. Router 1 reads `input/packets.csv`, resolves each destination IP against the
address ranges in its forwarding table (falling back to the default route), decrements TTL,
and forwards the packet onward. Routers 2–6 are threaded servers that re-forward, deliver
locally when the next hop is `127.0.0.1`, or discard the packet when TTL reaches zero.
Delivered payloads are the words of the Star Wars opening crawl, split across the routers
that deliver them.

Topology (ports from `routers.env`):

```
R1 ──┬──> R2 (8002) ──┬──> R3 (8003)
     │                └──> R4 (default route)
     └──> R4 (8004) ──┬──> R5 (8005)
                      └──> R6 (8006)
```

```bash
cd projects/proj2
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # python-dotenv only
bash start.sh                          # Ctrl-C once the last packet is delivered (~80s)
bash test_output.sh                    # diffs output/ against the reference solution
```

`start.sh` must be run from the project root — the routers use relative paths. It creates
`logs/` and `output/`, then launches the routers in reverse order so the servers are listening
before Router 1 starts sending.

- `input/` — packet list and the six per-router forwarding tables (provided).
- `output_solution/` — the instructor's reference answer (tracked, not regenerated).
- `output/`, `logs/` — produced by each run (gitignored).
- `skeleton_code/` — instructor-provided starter files.

A full run matches all 17 reference files. `test_output.sh` diffs with `-B` because five of
the reference files carry a trailing blank line the routers do not emit; the non-blank content
is identical. `output/recieved_by_router1.txt` is extra logging with no counterpart in the
reference set, which the comparison ignores.

## Notes

`notes/` is an Obsidian vault (the small `.obsidian/` config directory comes along with it),
but the notes themselves are plain Markdown and read fine on GitHub. Every chapter has
`notes.md`. Chapters 4–6 also have `questions.md` with `answers.md` and `solutions.md`;
chapter 1 has `questions.md` alone; chapter 3 is notes only.

| Chapter | Topic |
| --- | --- |
| 1 | Internet fundamentals, network edge and core, circuit vs. packet switching, the four delays, layering |
| 2 | Application layer: HTTP, cookies and caching, email, DNS, P2P, video streaming and CDNs |
| 3 | Transport layer: UDP, reliable data transfer, Go-Back-N vs. Selective Repeat, TCP, congestion control |
| 4 | Network layer data plane: router internals, longest-prefix match, IPv4 addressing, NAT, IPv6, SDN |
| 5 | Network layer control plane: link-state and distance-vector routing, OSPF, BGP, SDN controllers, ICMP |
| 6 | Link layer: error detection, multiple-access protocols, Ethernet, ARP, switches, VLANs, data centers |

Chapter 4 is the direct background for Project 2's forwarding logic.

## Paper Reviews

- The development of the Domain Name System
- Congestion avoidance and control (TCP)
- *Lightyear*: using modularity to scale BGP control plane verification
- The multiple roles that IPv6 addresses can play in today's Internet

## Note

Assignment specs, rubrics, and skeleton code in this repository were provided by the course
and remain the property of their authors. Everything else is my own coursework, archived here
for reference.
