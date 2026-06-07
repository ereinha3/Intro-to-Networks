# Chapter 5 – Network Layer: Control Plane (Cheat Sheet)

## 1. Control Plane vs Data Plane

* **Data plane (Chapter 4):**

  * Per-router: forwards individual packets based on local forwarding table.
  * Operations: lookup, switching, queuing, scheduling.

* **Control plane (Chapter 5):**

  * Decides **where** packets should go (the paths).
  * Two styles:

    1. **Per-router control plane (traditional):**

       * Each router runs routing algorithms (LS, DV, OSPF, BGP).
    2. **Logically centralized (SDN):**

       * A (logically) central controller computes forwarding rules; switches just do match+action.

---

## 2. Routing Fundamentals

* **Goal:** find “good” paths from sources to destinations in a graph with link costs.
* Graph model:

  * Nodes = routers, edges = links, cost `c(a,b)` for each link `(a,b)`.
* “Good” can mean: least cost, lowest delay, least congestion, policy-compliant, etc.

---

## 3. Link-State Routing: Dijkstra’s Algorithm

### 3.1 Global Information

* Every router learns:

  * Full network topology
  * All link costs
* Done via **link-state broadcast**:

  * Each router floods its local link info to all other routers in the AS.
  * All routers end up with the same map.

---

### 3.2 Dijkstra’s Algorithm (Link-State)

Compute least-cost paths from a source node `u` to all others.

**Variables:**

* `N'`: set of nodes for which shortest path is known.
* `D(v)`: current best estimate of cost from `u` to `v`.
* `p(v)`: predecessor of `v` along current best path.

**Pseudo-code (from slides):** 

1. **Initialization**

   * `N' = {u}`
   * For all `v`:

     * If `v` adjacent to `u`, `D(v) = c(u,v)`
     * Else `D(v) = ∞`

2. **Loop**

   * Find `w ∉ N'` with **minimum** `D(w)`.
   * Add `w` to `N'`.
   * For each neighbor `v` of `w` not in `N'`:

     * `D(v) = min( D(v), D(w) + c(w,v) )`
   * Repeat until all nodes are in `N'`.

**Complexity:**

* Basic implementation: `O(n²)` for `n` nodes.
* With heaps: `O(n log n)`.

**Properties:**

* Centralized (each node runs it but needs global info).
* Converges in `n-1` iterations.
* Can have **oscillations** if link costs depend on traffic (dynamic metrics).

**Homework:**

* Problems P3–P4: run Dijkstra from multiple sources and show tables like in the book. 

---

## 4. Distance-Vector Routing: Bellman–Ford

### 4.1 Local Information & Bellman–Ford Equation

Each node knows:

* Costs to its immediate neighbors only.
* Receives neighbors’ distance vectors, then updates its own.

**Bellman–Ford equation:**

[
D_x(y) = \min_{v \in \text{neighbors}(x)} \big( c(x,v) + D_v(y) \big)
]

Where:

* `D_x(y)` = node x’s current estimate of least cost to destination y.
* `c(x,v)` = cost from x to neighbor v.
* `D_v(y)` = v’s advertised distance to y.

---

### 4.2 Distance-Vector (DV) Algorithm

* Each node keeps a **distance vector**: one entry per destination.

* **Iterative, asynchronous, distributed**:

  * Initially: node knows distances only to neighbors.
  * From time to time:

    1. Node receives DV from neighbors.
    2. Uses Bellman–Ford to update its own DV.
    3. If any entry changed → sends new DV to neighbors.

* Convergence:

  * Under mild conditions, `D_x(y)` values **monotonically decrease** and eventually stabilize. (You prove this in P10.) 

* **Synchronous version (P6):**

  * All nodes exchange DVs in lockstep iterations.
  * Maximum # iterations to converge ≤ **diameter of the network** (max hop distance between any two nodes).

    * Intuition: “wave of knowledge” propagates one hop per iteration.

---

### 4.3 “Good News Travels Fast, Bad News Travels Slow”

* If link cost **decreases**:

  * New, cheaper paths appear.
  * Nodes update quickly (few iterations) and advertise smaller costs.
  * **No count-to-infinity problem** when costs decrease (P9).

* If link cost **increases** or link fails:

  * Nodes can mistakenly route to each other (“you’re cheaper”, “no, you are…”) → **count-to-infinity**.
  * Costs slowly increase step-by-step until they reach the correct value (or some maximum).

**Classic example:** 2-node loop between y and z after link to x becomes very expensive → they bounce false low-cost estimates back and forth. 

---

### 4.4 Count-to-Infinity & Poisoned Reverse

* Count-to-infinity: DV keeps increasing gradually toward the real (large) cost, causing long convergence times.
* **Poisoned reverse:**

  * If x routes to z via y, then x tells y that its cost to z is **∞**.
  * Prevents simple 2-node loops.
  * But does **not** prevent larger loops (3+ nodes) → still possible count-to-infinity (P11).

---

### 4.5 DV vs LS: Comparison

**Message complexity**

* LS (Dijkstra): each router floods link state → `O(n²)` messages total.
* DV: only neighbor exchanges; complexity depends on convergence speed.

**Convergence**

* LS: guaranteed in `O(n²)` time; may have transient oscillations with dynamic metrics.
* DV: speed varies; may have:

  * Routing loops
  * Count-to-infinity

**Robustness**

* LS:

  * Malfunctioning router can advertise incorrect link costs.
  * Each router’s **own** table unaffected directly, but all compute routes from same info; misinfo stays local to that node’s advertised state.
* DV:

  * Malicious router can claim “I have extremely low cost to everything” → **black hole**.
  * Bad info propagates through neighbors’ tables.

---

## 5. Hierarchical Routing & Autonomous Systems (AS)

The real Internet doesn’t run one flat routing protocol:

* **Scale:** billions of destinations, millions of routes.
* **Administrative autonomy:** each network wants control over its own policies.

**Solution:** group routers into **Autonomous Systems (AS)**:

* Each AS is a network under a single administrative control.
* Routing split into:

  1. **Intra-AS (intra-domain) routing:** within an AS.
  2. **Inter-AS (inter-domain) routing:** between ASes.

**Gateway routers:**

* Routers at the edge of an AS.
* Have links to other ASes.
* Participate in **both** intra-AS and inter-AS routing.

---

## 6. Intra-AS Routing (Interior Gateway Protocols)

Common intra-AS protocols:

* **RIP (Routing Information Protocol):**

  * Classic distance vector.
  * Hop count metric.
  * Updates every 30 seconds.

* **EIGRP:**

  * Cisco’s advanced DV protocol (now open spec).
  * More complex metric, faster convergence.

* **OSPF (Open Shortest Path First):**

  * Link-state protocol.
  * Floods LSAs (link-state advertisements) inside AS.
  * Each router runs Dijkstra to compute forwarding table.
  * Supports multiple metrics (bandwidth, delay, etc.).
  * Security: OSPF messages can be authenticated.

* **IS-IS:**

  * ISO standard, similar to OSPF in spirit.

---

### 6.1 Hierarchical OSPF

OSPF networks often split into:

* **Backbone area (Area 0):**

  * Connects all other areas.
* **Local areas (Area 1, 2, …):**

  * Internal routers only know full topology of their own area.
  * For other areas they just know “how to get to area border routers”.

Benefits:

* Limits link-state flooding scope.
* Scales to large ASes.

---

## 7. Inter-AS Routing: BGP – The Glue of the Internet

### 7.1 Basic Role

**BGP (Border Gateway Protocol):**

* De-facto inter-domain routing protocol.
* A **path-vector** protocol:

  * Routers exchange **paths** (AS sequences) to IP prefixes.
* Main tasks:

  1. **eBGP:** get reachability from neighboring ASes.
  2. **iBGP:** propagate reachability inside an AS.
  3. Apply **policy** to choose routes.

---

### 7.2 BGP Sessions & Messages

* **Peers** (BGP routers) maintain a TCP connection for BGP.
* Message types:

  * **OPEN** – start session, authenticate.
  * **UPDATE** – advertise or withdraw routes.
  * **KEEPALIVE** – keep session alive, ack OPEN.
  * **NOTIFICATION** – report errors / close.

---

### 7.3 BGP Route = Prefix + Attributes

A BGP advertisement contains:

* **Prefix:** destination network block (e.g., 12.34.0.0/16).
* **Attributes:**

  * **AS-PATH:** list of ASes the route has traversed.
  * **NEXT-HOP:** IP of the next-hop router in neighboring AS.
  * Local preference, MED, etc. (policy knobs).

**Loop detection:**

* Router discards routes whose AS-PATH already contains its own AS (P12).

---

### 7.4 Route Selection (Very Important)

When multiple routes exist to a prefix, a BGP router applies:

1. Highest **local preference** (policy).
2. Shortest **AS-PATH**.
3. Closest **NEXT-HOP** (lowest cost via intra-AS metric) → **hot potato routing**.
4. Other tie-breakers.

**Key point:**
BGP **does NOT always choose shortest AS-PATH** – local preference and policy can override. (P13 asks you to argue this.) 

---

### 7.5 Example: ASes, eBGP, iBGP (P14–P15)

* Each AS runs its own intra-domain protocol (e.g., OSPF, RIP).
* Gateways exchange prefixes via eBGP.
* Gateways flood those routes to internal routers via iBGP.
* Internal routers then use **intra-AS routing** to reach the chosen gateway.
* Hot-potato: an internal router typically chooses the **closest gateway** for a given prefix.

Homework P14–P15 walk through which router learns prefix x via OSPF, RIP, eBGP, iBGP, and which internal interface gets chosen for forwarding. 

---

### 7.6 Policy via Advertisements

ISPs use BGP policy to:

* Avoid carrying **transit traffic** for free (only route to/from customers).
* Prefer certain peering points (e.g., east vs west coast, P16).
* Control load-balancing, backup paths, and business relationships.

Mechanisms:

* **Filter** which routes to advertise to which neighbors.
* Manipulate attributes (AS-PATH prepending, local pref) to influence where traffic enters.

---

## 8. SDN Control Plane (Logically Centralized)

### 8.1 Traditional vs SDN

* Traditional:

  * Every router runs LS/DV, BGP, etc.
  * Hard to implement complex, dynamic traffic engineering.

* **SDN:**

  * Data-plane: dumb, fast switches.
  * Control-plane: **SDN controller**:

    * Maintains global view of network state.
    * Computes forwarding rules.
    * Programs switches via a southbound API (e.g., OpenFlow).
  * Network-control “apps” sit above the controller (traffic engineering, access control, load-balancing, etc.).

---

### 8.2 OpenFlow & Flow Tables

**Flow table entries** (generalized forwarding):

* Match: conditions over header fields (L2–L4 and more).
* Action: forward, drop, rewrite header, send to controller, etc.
* Priority, counters.

**Message types:**

* Controller → switch:

  * **modify-state:** add/delete/modify flow entries.
  * **packet-out:** send a specific packet out a port.
  * Feature/config requests.
* Switch → controller:

  * **packet-in:** “I don’t know what to do with this packet”.
  * **flow-removed, port-status**, etc.

Controllers like **OpenDaylight (ODL)** and **ONOS** provide:

* Northbound APIs for apps.
* Distributed state management and reliability. 

---

## 9. ICMP – Internet Control Message Protocol

* **Purpose:** network-level signaling between hosts and routers.
* Carried inside IP datagrams.

Common message types: 

* Type 0: Echo reply (ping response)
* Type 8: Echo request (ping)
* Type 3: Destination unreachable (various codes: network, host, port, protocol)
* Type 11: Time exceeded (TTL expired)

**Traceroute:**

* Sends UDP packets with increasing TTL (1, 2, 3, …).
* When TTL expires at router k, router sends back ICMP Time Exceeded (type 11).
* Source records RTT for each hop.
* Eventually destination sends port unreachable (type 3 code 3) → traceroute stops.

---

## 10. Network Management: SNMP, NETCONF, YANG

### 10.1 Big Picture

Network = huge, messy, distributed system. Need ways to:

* Monitor devices and links.
* Configure them consistently.
* React to failures and performance issues.

---

### 10.2 SNMP & MIB

**SNMP (Simple Network Management Protocol):**

* Manager–agent model:

  * **Managing server**: runs NMS (network management system).
  * **Managed devices**: routers, switches, hosts with an SNMP agent.
* **MIB (Management Information Base):**

  * Hierarchical database of variables (counters, config values, statuses).
  * 400+ standardized modules; many vendor-specific.

Message modes:

* **Request/response:**

  * Manager sends `GET`, `GET-NEXT`, `SET` → agent replies.
* **Traps/notifications:**

  * Agent asynchronously sends events (e.g., link down).

---

### 10.3 NETCONF & YANG (Modern Management)

**NETCONF:**

* RPC-style protocol for **configuration** and **state retrieval**.
* Runs over secure transport (often SSH/TLS).
* Operations (subset):

  * `<get-config>` / `<get>` – read configs / state.
  * `<edit-config>` – change config; supports **atomic commit**.
  * `<lock>/<unlock>` – avoid conflicting changes.
  * `<create-subscription>` – subscribe to notifications.

**YANG:**

* Data modeling language:

  * Specifies the **structure and types** of configuration and state data.
  * NETCONF uses YANG models to enforce correctness/constraints.

Idea:

* Move from per-device CLI scripts → **model-driven, multi-device, transactional config**.

