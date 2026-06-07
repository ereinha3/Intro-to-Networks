Answer Key

(Don’t scroll here until you’ve tried the problems!)

---

## True / False

1. **T**
    
2. **T**
    
3. **T**
    
4. **T**
    
5. **T**
    
6. **T**
    
7. **F** – FIFO does _not_ guarantee each flow a minimum bandwidth share.
    
8. **T**
    
9. **T**
    
10. **T**
    
11. **F** – IPv6 addresses are 128 bits, not 64.
    
12. **T**
    
13. **T**
    
14. **T**
    
15. **T**
    

---

## Multiple Choice

16. **C**
    
17. **C** – Buffer ≈ RTT × link capacity.
    
18. **D** – WFQ.
    
19. **D** – 11.0.0.0/8 is not a reserved private block.
    
20. **B**
    
21. **B** – Dynamic host configuration.
    
22. **C** – NAT _prevents_ direct reachability with private addresses.
    
23. **C** – In IPv6, routers don’t fragment; only source host.
    
24. **A** – IPv6-in-IPv4 tunneling.
    
25. **D** – Matching on “process ID in payload” isn’t part of header-field match.
    

---

## Free Response

### 26. Input queuing vs fabric

We assume in each slot of length (D), **one** packet can traverse the memory/bus fabric, and multiple can traverse the crossbar.

There are (N) packets (one at each input), all to **different outputs**.

(a) **Memory switching**

Only one packet can be transferred per slot. Worst case, a packet is served **last** among the (N) packets.

- First packet begins crossing immediately → 0 input wait.
    
- Last (Nth) packet waits for the first (N-1) transfers.
    

[  
\boxed{\text{Max input queuing delay} = (N-1) D}  
]

(b) **Bus switching**

Same limitation: only one packet can use the bus per slot. So the same reasoning applies:

[  
\boxed{\text{Max input queuing delay} = (N-1) D}  
]

(c) **Crossbar switching**

Crossbar can transfer multiple packets in parallel so long as they go to distinct outputs. That’s exactly our scenario: each packet has a different output. All (N) packets can be switched in the **same** slot.

[  
\boxed{\text{Max input queuing delay} = 0}  
]

(They may incur transmission time (D) on the output link, but no **queueing delay** at the input.)

---

### 27. WFQ sequences

Weights:

- (w_1 = 0.5), (w_2 = 0.25), (w_3 = 0.25).
    
- Ratios: (w_1 : w_2 : w_3 = 2 : 1 : 1).
    

(a) All three classes active

We want class 1 to get about **half** the slots, classes 2 and 3 each about **one-quarter**. One simple repeating pattern of length 4:

[  
\boxed{\text{Sequence: } 1,2,1,3, 1,2,1,3, \dots}  
]

Over 4 slots, class counts: 1 appears 2×, 2 appears 1×, 3 appears 1× → 2:1:1.

(b) Only classes 1 & 2 active (class 3 empty)

Original weights: 0.5 and 0.25. Their **relative** weights among active classes are:

[  
w_1 : w_2 = 0.5 : 0.25 = 2 : 1  
]

So class 1 should get about **2/3** of the slots, class 2 about **1/3**. A simple pattern:

[  
\boxed{\text{Sequence: } 1,1,2, 1,1,2, \dots}  
]

which gives 2 slots to class 1, 1 slot to class 2 per 3-slot cycle.

---

### 28. Longest-prefix ranges (8-bit addresses)

We have 8-bit addresses (0–255). Prefixes:

- `00` (2 bits) → interface 0
    
- `010` (3 bits) → interface 1
    
- `011` (3 bits) → interface 2
    
- `1` (1 bit) → interface 3
    

We must apply **longest prefix matching**.

Let’s map prefixes to ranges:

- `00xxxxxx` → binary `00000000` to `00111111` → decimal 0 to 63.
    
    - No longer prefix begins with `00`, so all those go to **interface 0**.
        
- `010xxxxx` → binary `01000000` to `01011111` → decimal 64 to 95.
    
    - Goes to **interface 1**.
        
- `011xxxxx` → binary `01100000` to `01111111` → decimal 96 to 127.
    
    - Goes to **interface 2**.
        
- `1xxxxxxx` → binary `10000000` to `11111111` → decimal 128 to 255.
    
    - No longer prefix that starts with `1`, so all 128–255 go to **interface 3**.
        

(a) Ranges:

- Interface 0: 0–63
    
- Interface 1: 64–95
    
- Interface 2: 96–127
    
- Interface 3: 128–255
    

(b) Counts (each block size = (2^{\text{remaining bits}})):

- Interface 0: 2 bits fixed (`00`), so (2^{6} = 64) addresses.
    
- Interface 1: 3 bits fixed (`010`), so (2^{5} = 32) addresses.
    
- Interface 2: 3 bits fixed (`011`), so (2^{5} = 32).
    
- Interface 3: 1 bit fixed (`1`), so (2^{7} = 128).
    

---

### 29. Subnetting 192.168.16.0/24

We need:

- A: ≥100 hosts
    
- B: ≥50 hosts
    
- C: ≥20 hosts
    

Recall: a subnet with prefix /y has (2^{32-y}) addresses, of which **2** are reserved (network & broadcast), so hosts = (2^{32-y} - 2).

1. For ≥100 hosts:
    

- /25 → 128 addresses, 126 usable hosts → OK
    
- /26 → 64 addresses, 62 hosts → too small
    

So Subnet A should be a **/25**.

2. For ≥50 hosts:
    

- /26 → 64 addresses, 62 hosts → OK
    
- /27 → 32 addresses, 30 hosts → too small
    

So Subnet B should be a **/26**.

3. For ≥20 hosts:
    

- /27 → 32 addresses, 30 hosts → OK
    

So Subnet C can be **/27**.

We can carve 192.168.16.0/24 sequentially:

- The /24 covers addresses 192.168.16.0–192.168.16.255.
    

(a) One reasonable assignment:

- **Subnet A:** 192.168.16.0/25
    
    - Covers .0–.127
        
- **Subnet B:** 192.168.16.128/26
    
    - Covers .128–.191
        
- **Subnet C:** 192.168.16.192/27
    
    - Covers .192–.223
        

(Leaving .224–.255 unused or for another small subnet.)

(b) Usable host ranges:

- Subnet A /25:
    
    - Network: 192.168.16.0
        
    - Broadcast: 192.168.16.127
        
    - **Usable hosts:** (\boxed{192.168.16.1 - 192.168.16.126})
        
- Subnet B /26:
    
    - Network: 192.168.16.128
        
    - Broadcast: 192.168.16.191
        
    - **Usable hosts:** (\boxed{192.168.16.129 - 192.168.16.190})
        
- Subnet C /27:
    
    - Network: 192.168.16.192
        
    - Broadcast: 192.168.16.223
        
    - **Usable hosts:** (\boxed{192.168.16.193 - 192.168.16.222})
        

---

### 30. NAT translation table

Connections and chosen external ports:

1. A(10.0.0.1:5001) → 128.119.40.86:80 → NAT port 30000
    
2. A(10.0.0.1:5002) → 64.12.10.5:80 → NAT port 30001
    
3. B(10.0.0.2:5001) → 128.119.40.86:80 → NAT port 30002
    

(a) NAT table (one possible formatting):

1. - Inside: (10.0.0.1, 5001, 128.119.40.86, 80)
        
    - Outside: (138.76.29.7, 30000)
        
2. - Inside: (10.0.0.1, 5002, 64.12.10.5, 80)
        
    - Outside: (138.76.29.7, 30001)
        
3. - Inside: (10.0.0.2, 5001, 128.119.40.86, 80)
        
    - Outside: (138.76.29.7, 30002)
        

(b) What remote servers see as **source (IP,port)**:

1. 138.76.29.7:30000
    
2. 138.76.29.7:30001
    
3. 138.76.29.7:30002
    

Each distinct (public IP,port) pair maps back to a unique internal socket.

---

### 31. IPv4 fragmentation: 4000 bytes, MTU 1500

- Original datagram total length: 4000 bytes
    
- IPv4 header: 20 bytes
    
- Original data payload: 4000 − 20 = 3980 bytes
    
- MTU: 1500 bytes → max data per fragment = 1500 − 20 = 1480 bytes
    
- Fragment data sizes must be multiples of 8 bytes (except possibly last fragment, but 1480 is multiple of 8: 1480/8 = 185).
    

Compute number of full-size fragments:

[  
\left\lfloor \frac{3980}{1480} \right\rfloor = 2 \text{ full fragments}  
]  
Data used: 2 × 1480 = 2960 bytes  
Remaining data: 3980 − 2960 = 1020 bytes

1020 is also divisible by 8 (1020/8 = 127.5 → oops, not integer). So we need to be more careful:

Typical textbooks use 4000-byte example with 1480-byte fragments; let’s recompute carefully:

3980 / 8 = 497.5 → the total data is _not_ a multiple of 8; that’s fine: only the **offset** needs to be in multiples of 8, not the size. Fragment data sizes just need to be multiples of 8 _except possibly the last fragment_ (which can be shorter). We'll use:

- Fragment 1 data: 1480
    
- Fragment 2 data: 1480
    
- Remaining: 3980 − 2960 = 1020 (allowed for last fragment, MF=0)
    

So:

(a) **Number of fragments: 3**

(b) Fragment details:

Let the original identification field be some constant (same for all fragments).

- **Fragment 1**
    
    - Total length: 20 + 1480 = **1500**
        
    - Data size: 1480 bytes
        
    - Offset: 0 (first byte of original data → offset 0)
        
    - MF = 1 (more fragments follow)
        
- **Fragment 2**
    
    - Data begins after first 1480 bytes → offset = 1480 / 8 = 185
        
    - Data size: 1480 bytes
        
    - Total length: 1500
        
    - Offset: **185**
        
    - MF = 1
        
- **Fragment 3**
    
    - Data begins after 1480 + 1480 = 2960 bytes → offset = 2960 / 8 = 370
        
    - Data size: remaining 3980 − 2960 = **1020** bytes
        
    - Total length: 20 + 1020 = **1040**
        
    - Offset: **370**
        
    - MF = 0 (last fragment)
        

---

### 32. OpenFlow rules at s2

We want:

- Port 1 ↔ Port 2 forwarding between (h5,h6) and (h1,h2)
    
- Local delivery for h3/h4 on ports 3 & 4
    
- h3 ↔ h4 via s2
    

A simple set of rules (not the only valid answer):

1. **Traffic from h5/h6 to h1/h2 (arriving on port 1):**
    
    - Match:
        
        - `in_port = 1`
            
        - `dst_ip = 10.1.0.1` OR `10.1.0.2`
            
    - Action: `output:2`
        
    
    (Can be two separate rules: one for 10.1.0.1, one for 10.1.0.2.)
    
2. **Traffic from h1/h2 to h5/h6 (arriving on port 2):**
    
    - Match:
        
        - `in_port = 2`
            
        - `dst_ip = 10.3.0.5` OR `10.3.0.6`
            
    - Action: `output:1`
        
3. **Local delivery to h3 (directly attached on port 3):**
    
    - Match: `dst_ip = 10.2.0.3`
        
    - Action: `output:3`
        
4. **Local delivery to h4 (directly attached on port 4):**
    
    - Match: `dst_ip = 10.2.0.4`
        
    - Action: `output:4`
        
5. **h3 → h4:**
    
    - Packets from h3 arrive on `in_port = 3`, `src_ip = 10.2.0.3`, `dst_ip = 10.2.0.4`.
        
    - Already handled by rule 4 (match on dst_ip 10.2.0.4 → output:4).
        
6. **h4 → h3:**
    
    - Packets from h4 arrive on `in_port = 4`, `dst_ip = 10.2.0.3`.
        
    - Already handled by rule 3 (dst_ip 10.2.0.3 → output:3).
        

So one possible concise rule set for s2:

1. `match: in_port=1, dst_ip=10.1.0.1 → actions: output:2`
    
2. `match: in_port=1, dst_ip=10.1.0.2 → actions: output:2`
    
3. `match: in_port=2, dst_ip=10.3.0.5 → actions: output:1`
    
4. `match: in_port=2, dst_ip=10.3.0.6 → actions: output:1`
    
5. `match: dst_ip=10.2.0.3 → actions: output:3`
    
6. `match: dst_ip=10.2.0.4 → actions: output:4`
    

(Implicitly, packets h3→h4 and h4→h3 are covered by 5 & 6.)

---

When you’ve tried these, send me your answers like you did for Ch. 5 and 6 and we’ll do the “what went right / what went wrong” breakdown again.