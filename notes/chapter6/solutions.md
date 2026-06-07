
### True / False (1–15)

1. **False.** Link layer = single link between neighbors; network layer = host-to-host across the Internet.
    
2. **True.** Some L2 protocols add local reliability.
    
3. **False.** Single-bit parity can **detect** any odd number of bit errors but **cannot locate/correct** which bit flipped.
    
4. **True.** 2D parity can detect and correct any **single-bit** error (row+column intersection).
    
5. **False.** CRCs are generally **stronger** than the Internet checksum.
    
6. **True.** Slotted ALOHA restricts transmissions to boundaries.
    
7. **False.** Pure ALOHA has **lower** max efficiency (~1/(2e)) than slotted (~1/e).
    
8. **True.** That is exactly the CSMA/CD collision behavior.
    
9. **True.** With full-duplex switch links, no shared medium → collisions essentially disappear.
    
10. **False.** MAC addresses are **flat**, not hierarchical; IP addresses are hierarchical.
    
11. **True.** ARP request = broadcast; reply = unicast.
    
12. **False.** Hubs just repeat bits; switches learn MACs and forward selectively.
    
13. **True.** VLANs carve one physical switch into multiple logical L2 networks.
    
14. **True.** MPLS forwards on labels and is used heavily for TE and fast forwarding.
    
15. **True.** That’s the standard ToR/aggregation/core hierarchy.
    

---

### Multiple Choice (16–25)

16. **C.** End-to-end congestion control is a transport/network responsibility (e.g., TCP), not link-layer.
    
17. **D.** Ethernet uses a CRC in the frame trailer.
    
18. **C.**  
    [  
    P(\text{success}) = N p (1-p)^{N-1} = 10 \cdot 0.1 \cdot 0.9^9 \approx 0.3874  
    ]  
    Option C.
    
19. **C.** Time-slot scheduling is ALOHA-like, not CSMA/CD.
    
20. **B.** Switches maintain a MAC table and selectively forward; hubs flood always.
    
21. **B.** ARP maps IP → MAC on the same LAN.
    
22. **D.** Destination IP address is not in the Ethernet header; that’s inside the payload.
    
23. **C.** 12 bits → (2^{12} = 4096) possible VLAN IDs.
    
24. **C.** MPLS is used for label-switched paths and TE.
    
25. **B.** DC fabrics (fat-trees/Clos) provide many parallel paths.
    

---

### Short / Free-Response (26–32) – Sketch Solutions

**26. 2D Parity**

(a) For each row, choose parity bit to make **total 1s even**.  
Let’s count quickly:

- Row 1: `1 0 1 1` → three 1s → need parity `1` to make 4 (even).
    
- Row 2: `0 0 0 1` → one 1 → parity `1` to make 2.
    
- Row 3: `1 1 0 0` → two 1s → parity `0` to keep it even.
    
- Row 4: `0 1 1 0` → two 1s → parity `0`.
    

So rows become:

- Row 1: 1 0 1 1 **1**
    
- Row 2: 0 0 0 1 **1**
    
- Row 3: 1 1 0 0 **0**
    
- Row 4: 0 1 1 0 **0**
    

(b) Now treat the **5th column** (row parities) as part of data and compute **column parities** (one extra row):

Compute column sums (over 4 rows above) and add a parity bit row to make each column even. You’ll get a final (5×5) block where each row and column has even parity.

(c) When one bit flips (row 2, col 3), the parity for row 2 becomes **odd**, and the parity for column 3 becomes **odd**. The receiver finds **the row and column with wrong parity**; their intersection pinpoints the corrupted bit, which can then be flipped back to correct the error.

---

**27. CRC**

Given (D = 1011), (G = 1101).  
Degree of (G) is 3 → (r = 3) redundant bits → **(a)** answer: 3 bits.

(b) Append 3 zeros to D: `1011 000`. Divide `1011000` by `1101` (mod 2). Doing the XOR “long division” yields remainder:

[  
R = \boxed{100}  
]

(c) Final transmitted sequence is `<D, R> =` **`1011 100`**.

---

**28. Slotted ALOHA throughput**

N = 20, p = 0.05.

(a) Probability exactly one node transmits:

[  
P_{\text{success}} = N p (1-p)^{N-1} = 20 \cdot 0.05 \cdot (0.95)^{19}  
]

(b) Numerically:

[  
(0.95)^{19} \approx 0.377,\quad  
P_{\text{success}} \approx 20 \cdot 0.05 \cdot 0.377 \approx 0.377  
]

(roughly 0.38)

(c) Interpretation: about **0.38 successful frames per slot** on average; this is the throughput in “frames/slot.”

---

**29. Polling throughput**

(a) One **polling cycle**: each of N nodes can send up to Q bits once per cycle. So **bits per cycle**:

[  
B_{\text{cycle}} = N Q  
]

Time per cycle:

- Data transmission per node: (Q/R) seconds
    
- Overhead per node: (d_{\text{poll}})  
    Total per cycle:
    

[  
T_{\text{cycle}} = N \left(\frac{Q}{R} + d_{\text{poll}}\right)  
]

Aggregate throughput:

[  
\text{Throughput} = \frac{B_{\text{cycle}}}{T_{\text{cycle}}}  
= \frac{NQ}{N\left(\frac{Q}{R} + d_{\text{poll}}\right)}  
= \boxed{\frac{Q}{\frac{Q}{R} + d_{\text{poll}}}}  
]

Note N cancels.

(b) Plug in Q = 10,000 bits; R = 10 Mbps = (10^7) bps; (d_{\text{poll}} = 0.1\ \text{ms} = 10^{-4}) s:

[  
\frac{Q}{Q/R + d_{\text{poll}}}  
= \frac{10^4}{10^4 / 10^7 + 10^{-4}}  
= \frac{10^4}{10^{-3} + 10^{-4}}  
= \frac{10^4}{1.1 \times 10^{-3}}  
\approx 9.09 \times 10^6\ \text{bps}  
]

So ≈ **9.09 Mbps**.

---

**30. ARP and router forwarding**

High-level sequence:

1. A wants to send to IP 10.0.2.20 (B). It sees (via subnet mask) that 10.0.2.20 is **not on its local subnet**, so it will send the IP datagram to its default gateway **10.0.1.1** (R’s R1 interface).
    
2. A checks its ARP table for 10.0.1.1. No entry ⇒ it broadcasts ARP request on LAN 1:
    
    - Ethernet src MAC: A
        
    - Ethernet dest MAC: FF:FF:FF:FF:FF:FF (broadcast)
        
    - ARP payload: “Who has 10.0.1.1? Tell 10.0.1.10 (A).”
        
3. Router R1 receives the broadcast (others may ignore). R1 replies with an ARP response:
    
    - Ethernet src MAC: R1
        
    - Ethernet dest MAC: A
        
    - ARP payload: “10.0.1.1 is at R1:R1:R1:R1:R1:R1.”
        
4. A updates its ARP table: `10.0.1.1 → R1’s MAC`.
    
5. A now sends the TCP/IP packet to B:
    
    - IP src = 10.0.1.10, IP dest = 10.0.2.20
        
    - Ethernet src MAC = A, Ethernet dest MAC = R1 (gateway).
        
6. Router R1 receives the frame, strips the Ethernet header, consults its IP routing table and decides to forward toward 10.0.2.0/24 via interface R2.
    
7. R1 now needs the MAC of 10.0.2.20 on LAN 2. If not known, R1 sends an ARP request on LAN 2:
    
    - Ethernet dest MAC = broadcast, src MAC = R2
        
    - ARP payload: “Who has 10.0.2.20? Tell 10.0.2.1.”
        
8. B receives this ARP request and replies with its MAC (BB:BB:...). R2 learns `10.0.2.20 → BB:…`.
    
9. R1 encapsulates the IP datagram again in an Ethernet frame on LAN 2:
    
    - Ethernet src MAC = R2, dest MAC = B
        
    - IP header unchanged (10.0.1.10 → 10.0.2.20).
        
10. B receives frame, strips Ethernet header, passes IP datagram up to TCP and so on.
    

---

**31. Switch learning**

Initial MAC table: empty.

1. **A → B**
    
    - Frame arrives on port 1 with src = A, dest = B.
        
    - Switch learns: `A → port 1`.
        
    - Table: `{A:1}`
        
    - Since B not yet in table, switch **floods** out ports 2 and 3. B receives the frame; C discards (wrong dest).
        
2. **B → A**
    
    - Frame arrives on port 2 with src = B, dest = A.
        
    - Switch learns: `B → port 2`.
        
    - Table: `{A:1, B:2}`
        
    - A is known on port 1, so switch forwards **unicast** only on port 1.
        
3. **C → A**
    
    - Frame arrives on port 3 with src = C, dest = A.
        
    - Switch learns: `C → port 3`.
        
    - Table: `{A:1, B:2, C:3}`
        
    - A is known on port 1, so switch forwards **unicast** on port 1 only.
        

So: first unknown dest ⇒ flood; as table fills, forwarding becomes unicast.

---

**32. VLAN trunking**

Trunk S1–S2 carries VLAN 10 and 20 with 802.1Q tags.

(a) **H1 (VLAN 10) → H3 (VLAN 10)**

- On S1, H1’s frame on port 1 is **untagged** (access port in VLAN 10).
    
- When S1 sends the frame over the trunk link to S2, it **inserts a VLAN 10 tag** (802.1Q header) into the Ethernet frame.
    
- S2 receives the tagged frame on the trunk, sees VLAN ID 10, and knows it belongs to VLAN 10. S2 then forwards it out its **VLAN 10 access port** (port 1) toward H3.
    
- On that access port, S2 **removes the tag** (H3 sees a regular untagged Ethernet frame).
    

(b) **H2 (VLAN 20) → H4 (VLAN 20)**

- Similarly, H2’s frame on S1 port 2 is untagged but associated with VLAN 20.
    
- When sent over the trunk, S1 adds an 802.1Q tag with VLAN ID 20.
    
- S2 receives the frame, recognizes VLAN 20, and forwards it out its VLAN 20 access port (port 2) to H4, stripping the tag before delivery.
    

**Isolation:**

- Frames from VLAN 10 hosts (H1, H3) carry VLAN ID 10 on the trunk and are never delivered to VLAN 20 access ports.
    
- Likewise, VLAN 20 traffic (H2, H4) is kept separate.
    
- Without a **router** (L3 device that routes between VLAN 10 and VLAN 20 networks), H1 cannot send IP traffic to H4, since L2 forwarding alone respects VLAN boundaries.
    
