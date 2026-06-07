Here we go—Chapter 5 practice set in the **same style** as before:

* **1–15:** True / False
* **16–25:** Multiple choice
* **26–32:** Short / free response
* **Answer key is at the very bottom.** Don’t peek until you’re ready 😈

(Questions cover: link-state vs distance-vector, Dijkstra, Bellman-Ford/DV, count-to-infinity, LS vs DV comparison, intra- vs inter-AS, OSPF, BGP, SDN, ICMP, SNMP/NETCONF/YANG, etc., matching your slides and HW. )

---

## True / False (1–15)

**1.** In the traditional per-router control plane, each router runs the routing algorithms locally and computes its own forwarding table, based on information exchanged with other routers.

---

**2.** In a link-state routing algorithm, each router maintains a complete map of the network topology and link costs, and runs a shortest-path algorithm such as Dijkstra.

---

**3.** In a distance-vector algorithm, each router eventually learns the full network topology (i.e., which nodes are connected by links) and their exact costs.

---

**4.** Dijkstra’s link-state algorithm, as presented in class, has time complexity (O(n^2)) in a naive implementation, where (n) is the number of routers.

---

**5.** In the Bellman-Ford equation, the distance from node (x) to destination (y) satisfies
[
d_x(y) = \min_{v \in \text{neighbors}(x)} { c(x,v) + d_v(y) }.
]

---

**6.** In the distance-vector algorithm, routers periodically exchange their entire distance vectors with neighbors; under mild conditions, the distance estimates converge to least-cost paths.

---

**7.** The count-to-infinity problem in distance-vector routing occurs when link costs **decrease**, causing routers to gradually increase their distance estimates to a destination.

---

**8.** Poisoned reverse is a technique used with distance-vector routing to help mitigate certain routing-loop scenarios by advertising large costs back on the link used to reach a destination.

---

**9.** Intra-AS routing refers to routing **within** an Autonomous System, while inter-AS routing refers to routing **between** Autonomous Systems.

---

**10.** OSPF is a distance-vector protocol, while RIP is a link-state protocol.

---

**11.** BGP is a path-vector protocol that advertises reachability for IP prefixes along with an AS-PATH attribute describing which ASes must be traversed.

---

**12.** In BGP, routers always choose the route with the smallest AS-PATH length, regardless of any other policy or local preference.

---

**13.** Hot-potato routing is a BGP-related behavior where an AS chooses the egress point (gateway) that has the **lowest intra-AS cost**, effectively “getting rid of” the traffic as soon as possible.

---

**14.** In a logically centralized SDN control plane, a (logically) central controller computes forwarding rules and installs them in switches via a southbound API such as OpenFlow.

---

**15.** ICMP messages are carried inside IP datagrams and can be used for error reporting (e.g., destination unreachable) and diagnostics (e.g., ping, traceroute).

---

## Multiple Choice (16–25)

**16.** Which of the following best describes a **link-state** routing algorithm?

A. Routers know only their neighbors’ distance vectors and iteratively update their own.
B. Routers periodically broadcast their distances to all destinations to their neighbors only.
C. Routers flood link-state information to all routers; each router locally computes shortest paths.
D. Routers compute routes using only local information and no message exchange.

---

**17.** Which statement about **distance-vector** routing is **correct**?

A. Each router knows the full network graph and runs Dijkstra’s algorithm.
B. Routers exchange their distance vectors with neighbors and use the Bellman-Ford equation to update.
C. It is immune to routing loops and count-to-infinity problems.
D. It requires each router to send LSAs (link-state advertisements) to all routers in the AS.

---

**18.** Which of the following is **not** an advantage of link-state (LS) routing compared to distance-vector (DV)?

A. Faster and more predictable convergence in many networks.
B. Easier to incorporate arbitrary link metrics (bandwidth, delay, etc.).
C. Guaranteed absence of routing loops during convergence.
D. Each router has a global view of the topology.

---

**19.** Which of the following correctly pairs the protocol and its typical role?

A. OSPF – inter-AS routing between ISPs.
B. BGP – intra-AS routing within an ISP.
C. RIP – path-vector inter-AS routing in the global Internet.
D. BGP – inter-AS routing between ASes (e.g., ISPs, large networks).

---

**20.** In OSPF, which of the following is **true**?

A. OSPF is a distance-vector protocol that uses periodic distance-vector exchanges.
B. OSPF is a link-state protocol that floods LSAs within an area and uses Dijkstra to compute routes.
C. OSPF operates only at the application layer.
D. OSPF is used exclusively for inter-AS routing.

---

**21.** Which of the following is **not** a BGP message type?

A. OPEN
B. UPDATE
C. KEEPALIVE
D. RESOLVE

---

**22.** Which pair is correctly matched as a BGP **path attribute**?

A. AS-PATH and NEXT-HOP
B. TTL and AS-PATH
C. NEXT-HOP and UDP port
D. Router-ID and subnet mask

---

**23.** Which of the following best describes the relationship between **eBGP** and **iBGP**?

A. eBGP is used within an AS; iBGP is used between ASes.
B. eBGP is used between ASes; iBGP is used within an AS to propagate external route information.
C. eBGP and iBGP are unrelated and never used together.
D. iBGP is used only by end hosts, not routers.

---

**24.** Which of the following is a key motivation for **Software-Defined Networking (SDN)**?

A. To eliminate the need for routing protocols entirely.
B. To separate the data plane and control plane, enabling easier network management and programmability.
C. To force all routers to use the same proprietary OS.
D. To replace IP with a completely new network-layer protocol.

---

**25.** Which statement about **SNMP vs NETCONF/YANG** is most accurate?

A. SNMP is primarily for configuration, while NETCONF/YANG is only for statistics.
B. Both are low-level device driver APIs used on routers’ internal buses.
C. SNMP focuses on querying/setting MIB variables; NETCONF/YANG provides more structured, transaction-oriented configuration and state management.
D. Neither SNMP nor NETCONF/YANG can modify device configurations.

---

## Short / Free Response (26–32)

### 26. Dijkstra on a small graph

Consider the following undirected network with link costs:

* (a)–(b): 3
* (a)–(c): 1
* (b)–(c): 7
* (b)–(d): 5
* (c)–(d): 2
* (c)–(e): 7
* (d)–(e): 3

(a) Run **Dijkstra’s algorithm** from source (a). For each step, list the set (N') (nodes for which the shortest path is known) and the current distance estimates (D(\cdot)) for the remaining nodes. (You can present this in a small table.)

(b) At the end, give the **shortest-path cost** from (a) to each node and one corresponding shortest path to each.

---

### 27. Single DV update using Bellman-Ford

Consider three nodes (x), (y), and (z) with the following **link costs**:

* (c(x,y) = 4)
* (c(y,z) = 1)
* (c(x,z) = 7)

Initially, each node only knows the cost to its direct neighbors.

(a) Write the **initial distance vector** at node (y): distances (D_y(x)), (D_y(y)), (D_y(z)).

(b) After one round of distance-vector exchange, node (y) sends its distance vector to (x) and (z), and they send theirs to (y). Using the Bellman-Ford equation, compute the updated distance vector at node (x), focusing on the distance to destination (z), i.e., (D_x(z)).

(c) Which path does (x) use to reach (z) after this update?

---

### 28. Count-to-infinity concept

(a) Briefly explain the **count-to-infinity problem** in distance-vector routing. In your explanation, mention whether it is associated with **increasing** or **decreasing** link costs.

(b) Why does **poisoned reverse** help prevent some (but not all) count-to-infinity scenarios?

---

### 29. LS vs DV comparison

Compare **link-state (LS)** and **distance-vector (DV)** routing along the following dimensions:

1. **Information each router stores** (global topology vs neighbor distances)
2. **Message complexity** (what is flooded/exchanged)
3. **Convergence behavior and problems** (e.g., loops, count-to-infinity, oscillations)
4. **Robustness to a misbehaving/malicious router**

Give 1–3 sentences per bullet.

---

### 30. Intra-AS vs Inter-AS routing (OSPF & BGP)

A large ISP runs OSPF internally and uses BGP to connect to other ISPs.

(a) Explain the roles of **OSPF** and **BGP** in this ISP’s network. Who talks to whom with each protocol?

(b) Why is it useful to have separate **intra-AS** (OSPF) and **inter-AS** (BGP) routing protocols instead of a single global routing protocol?

---

### 31. BGP route selection & policy

Consider AS1, AS2, and AS3. AS1 learns the following two routes to prefix (X):

* Route 1: AS1 ← AS2 ← AS3 ← X
* Route 2: AS1 ← AS3 ← X

Assume:

* Both routes are learned via eBGP at AS1’s gateway routers.
* Local preference is **higher** for routes learned from AS3 than from AS2.
* If local preference ties, AS1 prefers **shorter AS-PATH**.
* If AS-PATH length ties, you may ignore further tiebreakers for this problem.

(a) Which route will AS1 choose to reach prefix (X)? Briefly justify based on BGP route selection steps.

(b) Suppose now that AS1 sets local preference **higher** for routes via AS2 than via AS3 (e.g., business relationship changes). Which route is chosen then, and why?

---

### 32. SDN vs Traditional per-router control + OpenFlow

(a) Briefly describe the difference between a **traditional, distributed per-router control plane** and a **logically centralized SDN control plane**.

(b) In an SDN architecture using OpenFlow:

* What is stored in a **switch’s flow table**?
* How does the controller install forwarding behavior in the switches? (Mention the role of the southbound API / OpenFlow messages.)

(c) Mention **one advantage** and **one challenge** of using SDN in a large network.

---

