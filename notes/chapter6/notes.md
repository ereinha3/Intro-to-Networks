# Chapter 6 – Link Layer & LANs (Cheat Sheet)

---

## 1. Big Picture: What the Link Layer Does

* We’re now at the **link layer** (L2), just above the physical layer.
* Responsibility: **move a datagram between adjacent nodes over a single link.**

  * Routers and hosts = **nodes**
  * Links = wired (Ethernet, fiber), wireless (WiFi, LTE), etc.

Key tasks (not all are always implemented):

1. **Framing & link access**

   * Encapsulate IP datagram into a **frame** (header + trailer).
   * Decide **who gets to transmit** on a shared medium (MAC = Multiple Access Control).

2. **Link-layer addressing**

   * Use **MAC addresses** to deliver frames on local link.

3. **Error detection & correction**

   * Detect (and sometimes correct) bit flips on the link.

4. **Reliability / flow control (optional)**

   * Some link layers provide local reliability and pacing between neighbors.
   * Often used over **wireless**, rarely over clean wired links.

Link layer is implemented mostly in **NIC hardware** + some firmware/software. 

---

## 2. Where the Link Layer Lives

* Implemented in **every host and router** on each interface.
* Usually on a **network interface card (NIC)** or integrated on motherboard:

  * Handles **PHY** (modulation, line coding).
  * Handles **MAC** (framing, addressing, error detection, MAC protocol).
* Sender NIC:

  * Takes IP datagram from network layer, **encapsulates** into frame.
* Receiver NIC:

  * Verifies frame (checksum/CRC).
  * If OK and MAC dest matches (or is broadcast), strips header/trailer and hands IP datagram up.

---

## 3. Link-Layer Services (More Detail)

Possible services a link-layer protocol may offer to network layer: 

* **Framing**: add header/trailer delimiters around datagram.
* **Link access** (for broadcast links): ensure only one node sends at a time.
* **Reliable delivery**:

  * Local ACK/NAK, retransmissions (like mini-rdt between neighbors).
  * Useful on **noisy wireless**; often redundant on clean wired + TCP.
* **Flow control**: match sending rate to receiving NIC’s capacity.
* **Error detection / correction**:

  * Detect (and possibly correct) bit errors without involving the transport layer.
* **Half-duplex vs full-duplex**:

  * Half: both ends can transmit but **not simultaneously**.
  * Full: simultaneous transmit/receive allowed.

---

## 4. Error Detection and Correction

We want to detect/correct bit flips on a single link.

### 4.1 Parity Checks

**Single-bit parity**:

* Add **1 parity bit** to data bits.
* **Even parity**: parity bit chosen so total number of 1s is **even**.
* Detects any **single bit error**, but not all multi-bit errors.

**Two-dimensional parity**: 

* Arrange data in a **2D grid**, add parity bits for each row and column.
* Can:

  * **Detect and correct** any single-bit error (intersection of row/column with wrong parity).
  * **Detect** (but not necessarily correct) certain multi-bit errors.

Homework P1–P2 directly practice 2D parity: constructing parity bits and showing what patterns can/can’t be corrected. 

---

### 4.2 Internet Checksum (Review)

Used in **UDP**, **TCP**, **IPv4 header**. 

**Sender:**

1. Treat data (e.g., UDP segment) as a sequence of **16-bit integers**.
2. Compute the **one’s complement sum** (add all 16-bit words, wraparound carry).
3. Take the **one’s complement** of the sum → write into checksum field.

**Receiver:**

1. Compute the one’s complement sum over received data **including** checksum field.
2. If result is **all 1s**, assume no error; otherwise, error detected.

Not perfect, but catches most random errors.

Homework P3–P4: compute checksums for different byte patterns (ASCII “Internet”, numbers, letters). 

---

### 4.3 Cyclic Redundancy Check (CRC)

Much stronger error detection; heavily used in practice (Ethernet, WiFi). 

* Data bits: `D`
* Generator polynomial: `G` (bit pattern of length `r+1`)
* We want to find **R** (r bits) such that `<D, R>` is divisible by `G` in mod-2 arithmetic.

Construction:

1. Multiply `D` by `2^r` → append `r` zeros: `D·2^r`.
2. Divide `D·2^r` by `G` (mod 2, XOR-based division).
3. Let remainder be `R` (r bits).
4. Transmit `D` followed by `R`. Receiver divides `<D,R>` by `G`. If remainder ≠ 0 → error.

Properties:

* Detects **all burst errors** shorter than `r+1` bits.
* Very low probability of undetected longer bursts.

Homework P5–P7: practice computing CRC remainders and reasoning about detection of single/odd-bit errors. 

---

## 5. Multiple Access Links & Protocols

Link types:

* **Point-to-point**: one sender, one receiver (e.g., router–router fiber link).
* **Broadcast**: many nodes share a **single channel**:

  * Classic Ethernet on a bus
  * WiFi
  * Cable upstream
  * Satellite

We need a **multiple access protocol** for broadcast links.

### 5.1 Requirements for a “Good” MAC Protocol

Given link rate R, ideally:

1. When just **one node** wants to send → it can use the **full rate R**.
2. When **M nodes** have packets → each should get average rate ≈ **R/M**.
3. **Fully distributed**: no central controller, no global clock.
4. **Simple** to implement. 

No real protocol achieves all four perfectly; tradeoffs exist.

### 5.2 Taxonomy of MAC Protocol Types

1. **Channel partitioning** (static)

   * TDMA (time slots)
   * FDMA (frequency bands)
   * CDMA (codes)
2. **Random access**

   * Nodes transmit at will and handle **collisions** via retransmissions.
   * ALOHA, Slotted ALOHA, CSMA, CSMA/CD, CSMA/CA.
3. **Taking turns**

   * Nodes coordinate to take turns: polling, token passing.

---

## 6. Channel Partitioning MAC Protocols

### 6.1 TDMA – Time Division Multiple Access

* Time divided into **frames**, each containing **N time slots** for N nodes.
* Each node gets a **fixed slot** per frame.
* If node has nothing to send → its slot is wasted (idle).

### 6.2 FDMA – Frequency Division Multiple Access

* Total bandwidth split into **frequency bands**.
* Each node gets a **fixed frequency band**.
* Time wasted if a node has nothing to send in its band.

**Pros:** fair sharing, no collisions at high load.
**Cons:** inflexible, inefficient at low load (unused capacity).

---

## 7. Random Access MAC Protocols

Nodes transmit at **full rate R** whenever they have data. Collisions handled by retransmissions.

### 7.1 Slotted ALOHA

Assumptions:

* All frames same size.
* Time divided into **slots** equal to frame transmission time.
* Nodes can transmit only at **slot boundaries**.
* Nodes are synchronized. 

Operation:

* Each node with a new frame transmits in next slot.
* If collision → node retransmits in later slots with probability `p` until success.

Efficiency derivation (homework P8–P9): 

* Suppose `N` nodes, each transmits in a given slot with probability `p`.
* Probability a **given node** succeeds:
  `p * (1-p)^(N-1)`
* Probability **some node** succeeds:
  `N p (1-p)^(N-1)`

Maximize this over `p`, as `N → ∞`, optimum gives **max efficiency**:

[
\text{Max efficiency (slotted ALOHA)} = 1/e \approx 0.37
]

So at best, only ~37% of slots carry successful transmissions; rest are idle or collisions.

---

### 7.2 Pure ALOHA

Differences:

* No slots, no synchronization.
* Node transmits immediately when it gets a frame.
* Vulnerable to collisions with frames starting anytime in a **2-frame-time window**.

Max efficiency (homework P9 and slide derivation):

[
\text{Max efficiency (pure ALOHA)} = \frac{1}{2e} \approx 0.18
]

Even worse than slotted ALOHA.

Homework P10–P12: analyze throughput/efficiency for unequal `p` values and small N. 

---

### 7.3 CSMA / CSMA/CD

**Carrier Sense Multiple Access (CSMA):**

* Sense channel before transmit.
* If idle → send.
* If busy → defer.
* Helps reduce collisions, but not eliminate: **propagation delay** means two nodes might not “hear” one another’s start in time.

**CSMA/CD** (with Collision Detection): 

* Used in classic Ethernet (on shared medium).
* Node listens while transmitting.

  * If it detects a collision → **aborts** transmission and sends **jam signal**.
* After collision, performs **binary exponential backoff**:

  * After m-th collision: choose random K from `{0, 1, …, 2^m − 1}`.
  * Wait K * (slot time) before reattempt.

Homework R6: probability of K=4 after 5th collision, and resulting delay on 10 Mbps Ethernet. 

**Efficiency** depends on:

* `t_prop`: max propagation delay across LAN.
* `t_trans`: time to transmit a maximum-size frame.

Rough idea:

* Collision wasted time ≤ 2·t_prop.
* If `t_trans >> t_prop`, collisions cost relatively little → high efficiency.

---

### 7.4 “Taking Turns” MAC: Polling & Token Passing

**Polling:**

* A **master node** polls each slave in turn and grants transmit permission.
* Pros: no collisions, can prioritize.
* Cons:

  * Polling overhead and delay.
  * Single point of failure (master).

**Token passing (e.g., Token Ring):**

* A **token** circulates among nodes in a fixed order.
* A node can transmit only when it has the token.
* Pros: no collisions, predictable access.
* Cons:

  * Token overhead.
  * Single point of failure (lost token, malfunctioning node).

Homework R5, R7–R8 use the “cocktail party” analogy and discuss token inefficiency on very large rings. 

---

### 7.5 Polling Throughput

Homework P13:

* Broadcast channel rate = R bps.
* Polling delay between nodes = `d_poll`.
* Each node can send at most `Q` bits per round.

In one **polling cycle** over N nodes:

* Maximum data transmitted: `N * Q` bits.
* Time: `N*Q/R + N*d_poll` (transmission + polling overhead).

Throughput:

[
\text{Throughput} = \frac{NQ}{NQ/R + Nd_{\text{poll}}} = \frac{Q}{Q/R + d_{\text{poll}}}
]

Notice **N cancels**; throughput depends on Q, R, and `d_poll`. 

---

## 8. MAC Addresses & ARP

### 8.1 MAC Addresses

* **48-bit** identifier burned into NIC ROM (usually).
* Written in hex: e.g., `1A-2F-BB-76-09-AD`.
* Used for **local delivery** on a LAN; independent of IP address. 

Address space sizes (homework R9):

* MAC: 2^48 ≈ 2.8 × 10^14 addresses.
* IPv4: 2^32 ≈ 4.3 × 10^9.
* IPv6: 2^128 (astronomically larger). 

**Flat** addressing:

* MAC addresses do not encode location/subnet.
* IP addresses are **hierarchical** (subnets, prefixes).

---

### 8.2 ARP – Address Resolution Protocol

Goal: map **IP address → MAC address** on the same LAN. 

Each node has an **ARP table**:

* Entries: (IP, MAC, TTL).
* Stale entries are removed after TTL expires (~20 min).

**ARP Query:**

* Sender doesn’t know MAC for target IP.
* Sends **broadcast Ethernet frame** (dest MAC = `FF:FF:FF:FF:FF:FF`).
* Contains ARP request: “Who has IP X? Tell Y.”

**ARP Reply:**

* Only the node with IP X replies.
* Reply uses **unicast** frame to requester’s MAC.

Homework R10–R12: how ARP behaves with broadcast vs unicast frames and multiple interfaces. 

---

### 8.3 Routing to Another Subnet (Walkthrough)

Scenario: host A wants to send IP datagram to host B on a **different subnet**. 

Steps (assuming ARP tables exist):

1. A sees **destination IP B** not on local subnet → sends datagram to **default router R**.
2. A **encapsulates** IP datagram in Ethernet frame with:

   * MAC dest = router’s MAC, MAC src = A’s MAC.
3. Router R receives frame, strips Ethernet header, passes datagram up to IP.
4. R looks up B in routing table, picks outgoing interface.
5. R uses ARP (if needed) to get **B’s MAC** on next-hop subnet.
6. R encapsulates datagram in new Ethernet frame:

   * MAC dest = B’s MAC, MAC src = R’s MAC.
7. B receives frame, strips link header, passes IP datagram up.

Homework P14–P15: do a full IP+ARP walk for a three-subnet LAN with routers/switches and track each frame + MAC address used. 

---

## 9. Ethernet

### 9.1 Overview

* Dominant wired LAN technology.
* Evolved from **bus** topology with CSMA/CD to **switched full-duplex** topologies.
* Speeds: 10 Mbps → 100 Mbps → 1 G → 10 G → 40 G → 100 G+.

---

### 9.2 Ethernet Frame Format

Key fields: 

* **Preamble (8 bytes)**:

  * 7 bytes of `10101010` + 1 byte `10101011`
  * Used for clock synchronization.

* **Destination MAC (6 bytes)**

* **Source MAC (6 bytes)**

* **Type (2 bytes)**:

  * Tells which network-layer protocol: 0x0800 = IPv4, etc.

* **Payload**:

  * 46–1500 bytes (traditional Ethernet).

* **CRC (4 bytes)**:

  * 32-bit CRC for error detection.

**Unreliable, connectionless:**

* No link-layer ACK/NAK.
* Dropped frames are silently lost at link layer; recovered only if upper layers (e.g., TCP) retransmit.

---

### 9.3 From Hubs to Switches

Old-style **hub**:

* Electrical multi-port repeater.
* One big collision domain, CSMA/CD necessary.

Modern **switch**:

* Link-layer device.
* **Store-and-forward** frames.
* Each port typically a separate full-duplex link → **no collisions**.
* Implements **self-learning** and selective forwarding.

---

## 10. Ethernet Switches & Self-Learning

Each switch maintains a **forwarding table**:

* Entries: (MAC address, outgoing interface, timestamp). 

### 10.1 Learning

When a frame arrives on interface `i` from source MAC `S`:

* Switch records `(S → i)` in its table, with fresh timestamp.

### 10.2 Filtering & Forwarding

When frame arrives with destination MAC `D`:

1. If D is in table and mapped to interface `j`:

   * If `j == i`: **drop** frame (same segment; no need to send back).
   * Else: **forward** only on `j` (unicast).
2. If D not in table:

   * **Flood**: send on all interfaces **except** the one it arrived on.

Consequences:

* No configuration needed: switches are **plug-and-play**.
* Switches can be **cascaded**; self-learning works across networks.

Homework P16–P26: step though switch table evolution, interface-by-interface, as different hosts send frames. 

---

### 10.3 Switches vs Routers

* **Switch (L2)**:

  * Looks at **MAC** addresses.
  * Learns forwarding table via **data plane** behavior (no routing protocol).
  * Typically no IP or routing.

* **Router (L3)**:

  * Looks at **IP** addresses.
  * Computes forwarding table via **routing protocols** (LS/DV/BGP).

---

## 11. VLANs (Virtual LANs)

Motivation:

* Large LAN with a single broadcast domain → **scalability & security issues**.
* Want **logical separation** (e.g., CS vs EE dept) **without** separate physical switches. 

### 11.1 Port-based VLANs

* Switch ports assigned to VLAN IDs via configuration.
* Frames **in VLAN X** can only reach ports in VLAN X.
* Hosts can move physically but still be logically in same VLAN by reconfiguring port membership.

### 11.2 VLAN Trunks & 802.1Q

VLANs across multiple switches need **trunk links**:

* A single trunk carries traffic for multiple VLANs.
* Frames on trunk use **802.1Q tag**:

  * Inserts 4-byte VLAN header:

    * Tag Protocol Identifier (TPID = 0x8100).
    * Tag Control Information (includes 12-bit VLAN ID, 3-bit priority).
  * CRC is recomputed.

Homework R15–R16 & P28: max number of VLANs (2^12 = 4096), number of trunk ports to interconnect N switches, and an IP+ARP walk across VLANs. 

---

## 12. Link Virtualization: MPLS

**MPLS (Multiprotocol Label Switching)**:

* Originally a “link-layer” service between IP routers.
* Adds a **fixed-length label** between link and network layers (shim header).
* MPLS-capable routers (Label Switch Routers, LSRs) forward based on **label**, not IP dest. 

Key ideas:

* **Label-switched path (LSP)**:

  * Pre-established path through MPLS network.
* **Forwarding based on labels**:

  * Ingress LSR **pushes** label on packet.
  * Intermediate LSRs **swap** label (according to MPLS forwarding table).
  * Egress LSR **pops** label and forwards by IP.

Why bother?

* Faster lookups (fixed label instead of longest-prefix match).
* **Traffic engineering**:

  * Route traffic with same IP destination via **different paths** based on source or flow.
  * Precompute **backup paths** for fast reroute.

Homework P29–P30: design MPLS tables for specific desired paths A/D across a small network. 

---

## 13. Datacenter Networks

Modern datacenters: tens to hundreds of thousands of servers in racks. 

### 13.1 Topology

* **Racks of servers**:

  * Each rack: ~20–40 servers.
  * Each server connects to **Top-of-Rack (ToR)** switch at 1–10 Gbps.
* ToRs connect up to **aggregation (tier-2)** and then possibly **core (tier-1)** switches.
* Often use: **fat-tree**, Clos, or other richly-connected topologies:

  * Many **parallel paths** between racks (multi-path routing).
  * High **bisection bandwidth**.

Homework P32–P33: compute max per-flow rate under given traffic patterns in tree vs more connected topology; reason about rack over-subscription and probabilistic sharing. 

### 13.2 Challenges

* Multiple applications, load-balanced across many hosts.
* Avoiding:

  * Network hotspots,
  * Head-of-line blocking,
  * Incast congestion.

### 13.3 Protocol Innovations (data center specific)

* Link layer: **RoCE (RDMA over Converged Ethernet)** for low-latency, kernel-bypass.
* Transport: **DCTCP, DCQCN**, using ECN for fine-grained congestion control.
* Control & routing:

  * Heavy use of **SDN controllers**.
  * Application-aware **load balancers** act as “application-layer routers”.
* Placement:

  * Co-locate services and data in same or nearby racks to minimize cross-rack traffic.

---

## 14. “Day in the Life of a Web Request” (Link-Layer View)

Putting everything together (Ch. 1–6):

From plugging in laptop → viewing `www.google.com`:

1. **DHCP** over Ethernet:

   * Use broadcast at L2 → find DHCP server → obtain IP, mask, default gateway, DNS address.
2. **ARP**:

   * To send to DNS or default gateway, resolve **MAC** addresses via ARP requests (broadcast) and replies (unicast).
3. **DNS**:

   * Frame carries UDP segment to DNS server; frames hop via switches & routers.
4. **TCP**:

   * 3-way handshake with web server.
5. **HTTP**:

   * Request/response.
6. Along the way:

   * Ethernet & WiFi frames, switches, VLANs, possibly MPLS, data-center fabrics.

Homework P31 is exactly the “big synthesis” question (you already saw a variant in Chapter 4/5). 

