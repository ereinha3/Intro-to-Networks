# Chapter 4 – Network Layer: Data Plane (Cheat Sheet)

## 1. Big Picture

* **Network layer functions**

  * **Forwarding (data plane):** move each incoming packet to the correct output link on a *single router*.
  * **Routing (control plane):** compute end-to-end paths through the network.
* **Two control-plane styles**

  * **Per-router control plane:** each router runs routing algorithms, exchanges messages.
  * **SDN control plane:** remote controller computes forwarding rules; switches become simple “match+action” boxes.

---

## 2. Network Service Models

* Network layer may offer (in principle):

  * Guaranteed delivery / delay, in-order delivery, bandwidth guarantees, etc.
* **Internet**: **best-effort** service

  * No guarantees on delay, loss, bandwidth, or ordering.
  * Simplicity + overprovisioning + app-layer smarts (CDNs, TCP congestion control) made this model win.

---

## 3. What’s Inside a Router

### 3.1 High-Level Architecture

* **Input ports**

  * Physical layer: receive bits.
  * Link layer: decapsulate link frame.
  * **Lookup / forwarding:** use forwarding table to pick output port (destination-based), or general **match+action**.
  * Possibly input queuing.
* **Switching fabric**

  * Transfers packets from input ports to output ports.
* **Output ports**

  * Queues, buffer management, packet scheduling.
  * Link + physical layer to send bits.

---

## 4. Forwarding & Longest-Prefix Matching

* **Traditional forwarding:** match **destination IP prefix** → output port.
* **Forwarding table entry:** `(prefix, mask) → output interface`.
* **Longest-prefix rule:** among all matching prefixes, choose the one with the **most bits** in common with the destination.

  * Enables **route aggregation**: e.g., one route for 200.23.16.0/20 instead of 8 /23s.
* Implemented efficiently with **TCAMs** (content-addressable memories).

---

## 5. Switching Fabrics

Three classic designs:

1. **Memory-based**

   * First-gen routers: CPU copies packet from input to memory → output.
   * Limited by **memory bandwidth** (two memory accesses per packet).

2. **Bus-based**

   * All ports share a single bus.
   * Only **one packet at a time** on the bus.
   * Switching speed limited by **bus rate**.

3. **Interconnection networks (crossbar / Clos)**

   * Multiple simultaneous input→output transfers as long as they don’t conflict.
   * High throughput via parallelism, often used in high-end core routers.

**Switching rate**: ideally `N × R` for `N` ports each at rate `R`.

---

## 6. Input & Output Queuing

### 6.1 Input Port Queuing

* Occurs if **switch fabric** can’t move packets as fast as inputs.
* **Head-of-Line (HOL) blocking**:

  * Packet at the front of an input queue waits for a busy output.
  * Packets behind it (destined to *other* outputs) are blocked.

### 6.2 Output Port Queuing

* Occurs when arrival rate from fabric **> link rate**.
* Results: queueing delay, buffer overflow → **packet loss**.

### 6.3 How Much Buffering?

* Rule of thumb (**RFC 3439**):
  `B ≈ RTT × C`

  * `B` = buffer size, `RTT` = typical round-trip time, `C` = link capacity.
* Too much buffering → bufferbloat (huge delays).

---

## 7. Buffer Management & Packet Scheduling

### 7.1 Buffer Management

* **Tail drop:** drop arrival when buffer full (simple, but causes global synchronization).
* **Priority-based drop:** drop low-priority packets first.
* **Marking (ECN, RED):** routers mark packets instead of dropping to signal early congestion.

### 7.2 Scheduling Disciplines

All are applied at the **output port** when choosing the next packet to transmit:

1. **FIFO / FCFS**

   * Serve packets strictly in arrival order.

2. **Priority Scheduling**

   * Queues by class (e.g., real-time vs best-effort).
   * Always serve highest non-empty priority queue; FIFO *within* each class.

3. **Round Robin (RR)**

   * Traffic classified into per-class queues.
   * Server repeatedly cycles through queues; sends **one packet per class** (if available) each round.

4. **Weighted Fair Queuing (WFQ)**

   * Generalized RR.
   * Each class `i` has weight `w_i`; gets proportion `w_i / Σ w_j` of link bandwidth.
   * Emulates a fluid fair-share system; in practice approximated by serving classes according to weights (e.g., 1,2,3 pattern).

Homework problems P5–P6 make you compute departure times and delays for FIFO, priority, RR, and WFQ and compare **average delays**. 

---

## 8. IP: The Internet Protocol

### 8.1 IP Datagram Format (IPv4, key fields)

* **Version, header length**
* **Type of Service (DSCP/ECN)**
* **Total length**
* **Identification, flags, fragment offset** (used for fragmentation)
* **TTL (Time To Live)**
* **Protocol** (e.g., 6 = TCP, 17 = UDP)
* **Header checksum**
* **Source IP, Destination IP**
* **Options** (rarely used)

---

## 9. IP Fragmentation

* Links have MTU (max frame size). Large IP datagram must be **fragmented** if larger than link MTU.
* Fragment fields:

  * Same **Identification** for all fragments of original datagram.
  * **Fragment offset** measured in **8-byte units**.
  * **MF (More Fragments)** flag: set for all but last fragment.
* Reassembly happens **only at destination host**, not at routers.

Example: 4000-byte datagram over MTU 1500 → multiple fragments (each ≤ 1500 including headers). 

---

## 10. IP Addressing & Subnets

### 10.1 Interfaces and Subnets

* **Interface:** a host/router’s attachment point to a physical link.
* Each interface has an **IP address**.
* Subnet: a set of interfaces that can reach each other **without passing through a router**.

### 10.2 CIDR – Classless Inter-Domain Routing

* Address notation: `a.b.c.d/x`

  * `x` = number of bits in subnet (network) prefix.
* Example: `128.119.40.128/26` means:

  * First 26 bits = network part.
  * 2^(32−26) = 64 addresses in subnet.

Homework has many subnetting + longest-prefix-matching problems: P9–P15. 

### 10.3 Hierarchical Addressing & Aggregation

* ISP gets a larger block, e.g., `200.23.16.0/20`.
* It slices this into smaller blocks for customers (e.g., eight /23s).
* Exterior routers can advertise just the **aggregated prefix** to simplify routing tables.

### 10.4 Getting Addresses

* **Host**: static config or **DHCP**.
* **Network**: ISP or RIR/ICANN allocation.

---

## 11. DHCP – Dynamic Host Configuration Protocol

Goal: automatically assign IP configuration when a host joins a network.

**4-step “DORA” exchange (over UDP broadcast):**

1. **Discover** – client → broadcast query “any DHCP server?”
2. **Offer** – server → proposed IP + options.
3. **Request** – client → “I’d like that address.”
4. **ACK** – server → confirms lease.

DHCP also supplies:

* Default gateway (router address)
* DNS server address
* Subnet mask, lease time, etc.

---

## 12. NAT – Network Address Translation

### 12.1 Basic Idea

* Entire home/office uses **one public IPv4 address**.
* Internal hosts use **private addresses** (e.g., 10.0.0.0/8, 192.168.0.0/16).
* NAT router rewrites (IP, port) pairs and maintains a **translation table**.

**Outgoing:**

* `(internal_IP, internal_port)` → `(NAT_IP, NAT_port)` in table.
* Packet sent with NAT_IP, NAT_port as source.

**Incoming:**

* NAT looks up `(NAT_IP, NAT_port)` in table and maps back to internal host.

### 12.2 Pros

* Conserves IPv4 addresses.
* Internal hosts are not directly reachable from outside → some security.
* Can change ISP or internal numbering without renumbering everything.

### 12.3 Cons

* Violates strict “end-to-end” principle.
* Complicates P2P / inbound connections (NAT traversal).
* Routers now manipulate **transport-layer ports**.

Homework: NAT table entries and tricks like inferring number of behind-NAT hosts using IP ID fields; P18–P20. 

---

## 13. IPv6

### 13.1 Motivation

* IPv4 address exhaustion.
* Cleaner header for faster processing.
* Support for QoS / flow labeling.

### 13.2 IPv6 Datagram Format (key differences)

* **128-bit addresses**.
* Fixed **40-byte header**:

  * Version, Traffic Class, **Flow Label**
  * Payload length
  * Next header (like Protocol in IPv4)
  * Hop limit (like TTL)
  * Source & Destination addresses
* **Missing vs IPv4:**

  * No header checksum (routers don’t recompute).
  * No fragmentation/reassembly in routers (done by endpoints).
  * No “options” field: moved to extension headers.

### 13.3 Transition (Dual Stack & Tunneling)

* Not all routers can be upgraded at once → mixed IPv4 + IPv6.
* **Tunneling**:

  * IPv6 packet carried as payload of an IPv4 packet across an IPv4 region (“IPv6-in-IPv4”).

---

## 14. Generalized Forwarding & SDN

### 14.1 Match+Action Model

* Each switch/router uses a **flow table** of rules:

  * **Match:** pattern over header fields (L2, L3, L4).
  * **Action:** forward on port(s), drop, modify header, or send to controller.
  * **Priority:** resolve overlapping rules.
  * **Counters:** track bytes/packets.

This generalizes:

* Router: match on dest IP prefix → forward.
* Switch: match on dest MAC → forward or flood.
* Firewall: match on IP + ports → permit/deny.
* NAT: match on IP + ports → rewrite fields.

### 14.2 OpenFlow

* Standard southbound API between SDN controller and switches.
* Controller installs flow table entries:

  * Example actions:

    * Forward to port X
    * Drop
    * Rewrite header fields
    * Encapsulate and send packet to controller

Homework problems P21–P24 use the classic **3-switch, 6-host** OpenFlow network to have you design flow tables implementing specific forwarding behaviors and firewall rules. 

---

## 15. Middleboxes & Internet Architecture

* **Middleboxes:** anything on the path doing more than basic IP forwarding:

  * NATs, firewalls, IDS/IPS, load balancers, WAN optimizers, caches, etc.
* Trend:

  * Away from proprietary appliances → **white-box** hardware + software network functions (NFV).
  * Programmable via SDN, match+action APIs.

### 15.1 IP Hourglass & End-to-End Principle

* **IP as “thin waist”**: many link technologies below, many apps above.
* Original design philosophy:

  * **Goal:** connectivity
  * **Tool:** IP
  * **Intelligence:** at the endpoints (end-to-end argument)
* Middleboxes + NAT + SDN introduce more logic in the network, which has benefits (flexibility, security) but also tensions with the original end-to-end ideal.

