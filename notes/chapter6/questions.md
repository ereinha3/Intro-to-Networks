
## True / False (1–15)

**1.** The link layer is responsible for moving a datagram from one host to another across the entire Internet, while the network layer is responsible only for moving it over a single link.

---

**2.** Some link-layer protocols provide reliable delivery between adjacent nodes using ACK/NAK and retransmissions, even though the underlying network service (IP) is best-effort.

---

**3.** A single-bit parity scheme can detect any single-bit error in a block of bits, and it can also identify exactly which bit was corrupted.

---

**4.** Two-dimensional parity can both detect and correct any single-bit error in the block.

---

**5.** The Internet checksum used by UDP and TCP provides stronger error detection than a typical CRC (Cyclic Redundancy Check).

---

**6.** In Slotted ALOHA, time is divided into slots, and nodes are only allowed to start transmissions at slot boundaries.

---

**7.** In Pure (unslotted) ALOHA, the maximum channel efficiency is higher than in Slotted ALOHA because nodes can begin transmitting at any time.

---

**8.** In CSMA/CD, when a node detects a collision while transmitting, it immediately stops sending, sends a jam signal, and then backs off before trying again.

---

**9.** In modern switched Ethernet (full-duplex links to a switch), collisions are essentially eliminated, and CSMA/CD is no longer needed.

---

**10.** MAC (Ethernet) addresses are hierarchical and encode the subnet structure (i.e., which router or network you’re on), similar to how IP addresses encode network prefixes.

---

**11.** ARP queries are sent in Ethernet frames with a broadcast destination MAC address, while ARP replies are typically sent in frames with a unicast destination MAC address.

---

**12.** An Ethernet hub and a switch behave similarly: both broadcast each incoming frame out all ports except the one it arrived on, and neither learns anything about MAC addresses.

---

**13.** With VLANs, a single physical switch can be logically partitioned into multiple virtual switches, each with its own broadcast domain.

---

**14.** MPLS forwards packets based on fixed-length labels rather than destination IP prefixes, which can be useful for traffic engineering and faster lookups.

---

**15.** In a data center, servers are usually connected to a Top-of-Rack (ToR) switch, and traffic between racks must go through higher-level (aggregation / core) switches.

---

## Multiple Choice (16–25)

**16.** Which of the following is _not_ a typical link-layer service?

A. Framing  
B. Error detection  
C. Congestion control for end-to-end paths  
D. Medium access control on broadcast links

---

**17.** Which mechanism is **most commonly** used in Ethernet to detect errors in a frame?

A. Internet checksum  
B. Single-bit parity  
C. Two-dimensional parity  
D. Cyclic Redundancy Check (CRC)

---

**18.** Consider Slotted ALOHA with (N = 10) nodes. Each node attempts to transmit in a given time slot with probability (p = 0.1), independently. What is the probability that **some node** successfully transmits in that slot (i.e., exactly one node transmits)?

A. (0.1)  
B. (0.3487) (≈ (10 \cdot 0.1 \cdot 0.9^8))  
C. (0.3874) (≈ (10 \cdot 0.1 \cdot 0.9^9))  
D. (0.9^{10})

---

**19.** Which of the following is **not** a characteristic of CSMA/CD as used in classic bus Ethernet?

A. Stations sense the carrier (the medium) before transmitting.  
B. Stations detect collisions while transmitting.  
C. Stations scheduling access using time slots of equal length.  
D. After detecting a collision, stations back off a random time before retransmitting.

---

**20.** Which of the following is **true** about Ethernet switches (not hubs)?

A. They forward every incoming frame out all ports, except the incoming port.  
B. They maintain a MAC address table and selectively forward frames based on destination MAC.  
C. They always require manual configuration of MAC address tables.  
D. They operate at the network layer and make decisions based on IP addresses.

---

**21.** ARP (Address Resolution Protocol) is used to:

A. Map MAC addresses to IP addresses within the same LAN.  
B. Map IP addresses to MAC addresses within the same LAN.  
C. Map hostnames to IP addresses.  
D. Map port numbers to process IDs.

---

**22.** Which field is **not** part of a standard Ethernet frame header/trailer?

A. Destination MAC address  
B. Source MAC address  
C. Type/length field  
D. Destination IP address

---

**23.** IEEE 802.1Q VLAN tagging uses a 12-bit VLAN ID field. What is the **maximum number of distinct VLAN IDs** that can be represented?

A. 256  
B. 1024  
C. 4096  
D. 65,536

---

**24.** Which of the following best describes a key benefit of MPLS in ISP networks?

A. It encrypts packets end-to-end.  
B. It replaces IP addresses with MAC addresses.  
C. It enables label-switched paths that can be chosen for traffic engineering (e.g., policy-based routing for certain flows).  
D. It eliminates the need for routers and switches.

---

**25.** Which of the following is **typically true** in modern data center networks?

A. There is usually exactly one path between any two racks.  
B. The network is often built with many parallel paths (e.g., fat-tree/Clos) to increase bisection bandwidth.  
C. All inter-rack traffic must pass through the public Internet.  
D. Servers connect directly to core routers without any top-of-rack switches.

---

## Short / Free-Response (26–32)

**26. 2D Parity.**  
You are given the following 4×4 block of data bits (before parity), arranged as 4 rows of 4 bits:

Row 1: 1 0 1 1  
Row 2: 0 0 0 1  
Row 3: 1 1 0 0  
Row 4: 0 1 1 0

(a) Add **row parity bits** using **even parity** (one extra bit per row).  
(b) Then add **column parity bits** using even parity (one extra bit per column, plus one overall parity bit if needed).  
(c) Suppose during transmission, a single bit in row 2, column 3 is flipped. Explain how 2D parity allows the receiver to both **detect** and **locate** this bit error.

---

**27. CRC (short example).**  
Let the data bits be (D = 1011) and the generator (divisor) be (G = 1101).

(a) How many redundant bits (R) will be appended to the data?  
(b) Compute the remainder (R) when (D \cdot 2^r) (data with r zeros appended) is divided by (G) in modulo-2 arithmetic.  
(c) Write the final transmitted bit sequence (\langle D, R \rangle).

_(This is a toy-sized example so you can do the long division by hand.)_

---

**28. Slotted ALOHA throughput.**  
In Slotted ALOHA, suppose there are **N = 20** nodes and each transmits in a given slot with probability (p = 0.05), independently of others.

(a) Write an expression for the probability that **exactly one node** transmits in a slot (i.e., the slot is a “successful” slot).  
(b) Evaluate this expression numerically (to about 3 decimal places).  
(c) Interpret this value as the **throughput in successful frames per slot**.

---

**29. Polling throughput.**  
Consider a broadcast channel of rate (R = 10\ \text{Mbps}) shared by **N** nodes using polling. Between each node, there is a polling overhead (round-trip control message, etc.) that takes (d_{\text{poll}} = 0.1\ \text{ms}). Each node, when polled, may send up to **Q = 10{,}000** bits.

(a) Derive an expression for the **aggregate throughput** (in bps) of the system as a function of (Q), (R), and (d_{\text{poll}}).  
(b) Plug in the given values to compute the throughput numerically (in Mbps).

_(Hint: Carefully compute time per full polling cycle and number of bits sent per cycle.)_

---

**30. ARP and forwarding across a router.**  
Host A (IP 10.0.1.10, MAC AA:AA:AA:AA:AA:AA) is on LAN 1. Host B (IP 10.0.2.20, MAC BB:BB:BB:BB:BB:BB) is on LAN 2. The two LANs are connected by a router R, with:

- Interface R1 on LAN 1: IP 10.0.1.1, MAC R1:R1:R1:R1:R1:R1
    
- Interface R2 on LAN 2: IP 10.0.2.1, MAC R2:R2:R2:R2:R2:R2
    

Assume A’s ARP table initially has **no entries** for 10.0.1.1 or 10.0.2.20.

Describe, in proper order, the L2/L3 events and ARP interactions that occur when A sends a TCP segment to B for the first time (e.g., A wants to establish a TCP connection to B).

You should mention:

- How A decides which IP address to ARP for
    
- The ARP request/response on LAN 1
    
- The Ethernet frame’s source/destination MAC addresses on each hop
    
- How R forwards the IP datagram to B on LAN 2
    

(High-level bullet points are fine; you don’t need to mention TCP handshake details.)

---

**31. Switch learning behavior.**  
Consider a single Ethernet switch S with three ports. Hosts are connected as follows:

- Port 1: Host A (MAC A)
    
- Port 2: Host B (MAC B)
    
- Port 3: Host C (MAC C)
    

Assume S’s MAC address table is initially **empty**.

Events:

1. A sends a frame to B.
    
2. B replies with a frame to A.
    
3. C sends a frame to A.
    

For each event:

(a) State how S handles the frame (flood, unicast, or drop) and on which ports.  
(b) Show the contents of S’s MAC table **after** each event.

(Assume no entries time out during this sequence.)

---

**32. VLAN trunking scenario.**  
Two switches S1 and S2 are connected by a single **trunk link** that carries VLAN 10 and VLAN 20 using 802.1Q tagging. On S1:

- Port 1 (VLAN 10): Host H1 (MAC H1)
    
- Port 2 (VLAN 20): Host H2 (MAC H2)
    

On S2:

- Port 1 (VLAN 10): Host H3 (MAC H3)
    
- Port 2 (VLAN 20): Host H4 (MAC H4)
    

Describe what happens at the Ethernet/frame level when:

(a) H1 sends a frame to H3.  
(b) H2 sends a frame to H4.

For each, indicate:

- How the frame is tagged/untagged on each segment (host–switch and switch–switch)
    
- How VLAN isolation prevents H1 from directly sending to H4 (without a router).
    

---
