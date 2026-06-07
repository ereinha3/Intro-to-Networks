
### True / False (1–15)

1. **True.**
2. **True.**
3. **False.** DV nodes do *not* learn the full topology; they only know distance estimates via neighbors.
4. **True.** Naive Dijkstra is (O(n^2)); with heaps it can be improved. 
5. **True.** This is exactly the Bellman-Ford form. 
6. **True.** Under mild conditions, DV converges. 
7. **False.** Count-to-infinity is associated with **increasing** link costs (bad news propagating slowly). 
8. **True.** Poisoned reverse advertises very high cost back on the link used, to break simple two-node loops.
9. **True.** That’s the standard definition of intra-/inter-AS. 
10. **False.** OSPF is **link-state**, RIP is **distance-vector**. 
11. **True.** BGP is a path-vector protocol with AS-PATH and other attributes. 
12. **False.** Shortest AS-PATH is *one* criterion; policies (local pref, etc.) can override it.
13. **True.** Hot-potato: choose egress with minimal intra-AS cost. 
14. **True.** That’s the SDN model: logically centralized controller + southbound API like OpenFlow. 
15. **True.** ICMP is carried in IP and used for errors + diagnostics (e.g., ping, traceroute). 

---

### Multiple Choice (16–25)

16. **C.** LS: flood link-state info; each router runs Dijkstra with full topology.
17. **B.** DV uses neighbor distance vectors + Bellman-Ford.
18. **C.** LS can still have temporary loops/oscillations; no absolute guarantee during convergence.
19. **D.** BGP is the inter-AS routing protocol.
20. **B.** OSPF is LS, floods LSAs, uses Dijkstra.
21. **D.** RESOLVE is not a BGP message type (real ones: OPEN, UPDATE, KEEPALIVE, NOTIFICATION).
22. **A.** AS-PATH and NEXT-HOP are key BGP path attributes.
23. **B.** eBGP: between ASes; iBGP: within an AS to propagate external routes.
24. **B.** SDN separates control/data planes for programmability and easier management.
25. **C.** SNMP ↔ MIB variables; NETCONF/YANG ↔ richer, structured config/state & transactions.

---

### Short / Free Response (26–32)

#### 26. Dijkstra on small graph

Edges:

* a–b:3, a–c:1, b–c:7, b–d:5, c–d:2, c–e:7, d–e:3

Let’s track (N') and distances (D(\cdot)) from (a).

* **Initialization:**

  * (N' = {a})
  * (D(a)=0)
  * Neighbors of a:

    * (D(b)=3) (via a)
    * (D(c)=1) (via a)
  * Others: (D(d)=\infty), (D(e)=\infty)

* **Step 1:** add closest node not in (N'): (c) (cost 1)

  * (N' = {a,c})

  * Update neighbors of c:

    * For d: (D(d) = \min(\infty, D(c)+c(c,d)) = \min(\infty,1+2)=3)
    * For e: (D(e) = \min(\infty,1+7)=8)
    * For b: (D(b)) vs (D(c)+7 = 1+7=8) → keep 3 (via a).

  * Now: (D(b)=3,\ D(c)=1,\ D(d)=3,\ D(e)=8)

* **Step 2:** next smallest among {b(3), d(3), e(8)} → tie, choose e.g. **b**:

  * (N' = {a,c,b})

  * Update neighbors of b:

    * d: (\min(3, D(b)+5=3+5=8) = 3) (no change)
    * c: (\min(1, 3+7=10)=1) (no change)

  * Distances unchanged.

* **Step 3:** pick next: **d** (3)

  * (N' = {a,c,b,d})

  * Update neighbors of d:

    * e: (\min(8, D(d)+3=3+3=6) = 6) → update
    * b, c already better.

  * Now: (D(e)=6).

* **Step 4:** pick **e** (6)

  * (N' = {a,c,b,d,e}) done.

**(b) Final shortest-path costs and paths from a:**

* (a \to a): cost 0, path: a
* (a \to c): cost 1, path: a–c
* (a \to b): cost 3, path: a–b
* (a \to d): cost 3, path: a–c–d (1+2)
* (a \to e): cost 6, path: a–c–d–e (1+2+3)

(Other paths with same cost are acceptable if consistent.)

---

#### 27. Single DV update

Link costs: (c(x,y)=4), (c(y,z)=1), (c(x,z)=7).

(a) **Initial DV at y:**

* By definition, (D_y(y)=0).
* Direct neighbor costs:

  * (D_y(x)=4) (direct link)
  * (D_y(z)=1) (direct link)

So: ((D_y(x), D_y(y), D_y(z)) = (4, 0, 1)).

---

(b) After one round, x receives y’s DV and z’s DV. Initially:

* (D_x(x)=0)
* (D_x(y)=4) (direct)
* (D_x(z)=7) (direct)

Using Bellman-Ford for destination z at node x:

[
D_x(z) = \min\big( c(x,z) + D_z(z),\ c(x,y) + D_y(z) \big)
]

* Direct via z: (c(x,z)+D_z(z) = 7 + 0 = 7)
* Via y: (c(x,y)+D_y(z) = 4 + 1 = 5)

So:

[
D_x(z) = \boxed{5}
]

---

(c) After this update, x prefers the path:

* (x \to y \to z), with cost (4+1=5).

---

#### 28. Count-to-infinity & poisoned reverse

(a) **Count-to-infinity problem:**

* Occurs in **distance-vector** routing when a link cost (or path) to a destination **increases** or a link fails.
* Routers may have outdated information and keep telling each other there is a “good” route through each other; they repeatedly increase their distance estimates to that destination step by step (e.g., 4, 5, 6, 7, …), slowly “counting to infinity” instead of quickly realizing the destination is unreachable or expensive.

It is associated with **“bad news” (increased cost / failure)**, not with decreased costs.

---

(b) **Poisoned reverse:**

* If a router uses neighbor N to reach destination D, it advertises to N that its distance to D is **infinite** (or very large).
* That way, N will not try to route to D via this router, preventing simple **two-node loops** (A ⇄ B).
* However, poisoned reverse does **not** prevent longer loops involving **three or more routers**, so it only mitigates some count-to-infinity scenarios, not all.

---

#### 29. LS vs DV comparison

1. **Information stored:**

   * **LS:** Each router stores the **full topology** (graph: nodes + links + link costs) and runs Dijkstra locally.
   * **DV:** Each router stores **distance vectors**: its current best distance to every destination, plus often next-hop info; it does *not* know the full topology.

2. **Message complexity:**

   * **LS:** Routers flood **link-state advertisements** (LSAs) to all routers in the AS. Message complexity is roughly (O(n^2)) in a network of (n) routers.
   * **DV:** Routers periodically or event-driven exchange distance vectors only with **neighbors**; message complexity depends on convergence behavior.

3. **Convergence behavior and problems:**

   * **LS:** Convergence is typically fast and predictable but can have transient **oscillations** if link costs depend on traffic. 
   * **DV:** Convergence can be slow; can suffer from **routing loops** and the **count-to-infinity** problem (bad news travels slowly).

4. **Robustness to misbehavior:**

   * **LS:** A single misbehaving router can flood incorrect **link-state** info, but each router still computes its own forwarding table; error is somewhat localized to the bogus LSAs.
   * **DV:** A misbehaving router can advertise artificially low **distance vectors** to many destinations; since other routers directly use these values in their own tables, errors can propagate widely (e.g., black-holing traffic).

---

#### 30. Intra-AS vs Inter-AS (OSPF & BGP)

(a) **Roles:**

* **OSPF (intra-AS):**

  * Runs among routers *inside* the ISP’s AS.
  * Routers flood LSAs and compute shortest paths to all internal subnets.
  * Determines how packets move **within** the ISP (e.g., between POPs, internal routers).

* **BGP (inter-AS):**

  * Runs between **gateway routers** of this ISP and neighboring ASes (eBGP), and internally between this ISP’s BGP-speaking routers (iBGP).
  * Exchanges reachability to external prefixes (customer networks, other ISPs).
  * Determines which **external** paths the ISP uses to reach the rest of the Internet and how it advertises its own prefixes.

---

(b) **Why separate intra-/inter-AS protocols?**

* **Policy:** Inter-AS routing is heavily policy-driven (business relationships, peering agreements, traffic engineering). Intra-AS routing mainly concerns performance and reliability.
* **Scale:** A single global routing protocol would have to handle the full Internet; splitting into intra-AS and inter-AS makes tables and updates manageable.
* **Autonomy:** Each AS wants autonomy to choose its own internal routing protocol (OSPF, IS-IS, etc.) without affecting other ASes.

---

#### 31. BGP route selection & policy

Routes to prefix X learned by AS1:

* Route 1: AS1 ← AS2 ← AS3 ← X  (AS-PATH: AS1-AS2-AS3)
* Route 2: AS1 ← AS3 ← X          (AS-PATH: AS1-AS3)

(a) With higher local preference for **AS3**:

* Step 1: Compare **local preference**: route via AS3 has higher local pref → chosen.
* Step 2: AS-PATH length only used if local pref ties; here it doesn’t even need to be considered.

So AS1 chooses **Route 2 (via AS3)**.

---

(b) If local preference is now higher for **AS2**:

* Step 1: Compare local preference: route via AS2 (AS1–AS2–AS3–X) now wins.
* Step 2: Even though its AS-PATH is longer, BGP prioritizes **local preference** over AS-PATH length.

So AS1 now chooses **Route 1 (via AS2)**.

This shows BGP does **not** always pick the shortest AS-PATH; **policy wins**.

---

#### 32. SDN vs traditional control + OpenFlow

(a) **Traditional per-router control plane vs SDN:**

* **Traditional:**

  * Each router runs distributed routing protocols (e.g., OSPF, BGP).
  * Forwarding table is computed locally based on protocol messages.
  * Control logic is distributed and embedded in each router.

* **SDN (logically centralized):**

  * A logically central **controller** maintains a global network view.
  * It computes forwarding behavior and installs rules into switches.
  * Switches have simple data planes; control logic resides in the controller.

---

(b) **OpenFlow / flow tables:**

* A **switch’s flow table** contains entries with:

  * Match fields (on packet header bits: src/dst IP, TCP port, VLAN ID, etc.)
  * Actions (e.g., forward out port X, drop, modify header, send to controller)
  * Counters (stats about packets/bytes matched).

* The **controller** uses the **southbound API** (e.g., OpenFlow protocol) to:

  * Add, delete, or modify flow entries (via “modify-state” / “flow-mod” style messages).
  * Handle “packet-in” messages from switches (e.g., first packet of new flow), decide what rule to install, and send “packet-out”/flow-mod messages back.

---

(c) **One advantage & one challenge:**

* **Advantage:**

  * Easier, **centralized network management** & flexible traffic engineering—operators can program routing and policies at a high level, and the controller computes & installs the appropriate rules.

* **Challenge:**

  * Building a **scalable, fault-tolerant, secure** logically centralized controller is hard; the controller becomes a critical distributed system whose failure or compromise can impact the entire network.

---

When you’re ready, try answering these like you did for Chapters 1 & 6, then send me your answers and we’ll do another detailed “what went right / what went wrong” pass.
