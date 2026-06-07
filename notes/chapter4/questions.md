## True / False (1–15)

**1.** In the router architecture studied in class, the **data plane** is responsible for moving packets from input ports to output ports at high speed, while the **control plane** is responsible for computing and installing the forwarding/flow tables.

---

**2.** In “switching via memory,” early routers copied each packet from an input port into CPU memory and then back out to an output port, which limited the overall switching rate by the memory bandwidth.

---

**3.** In a **bus-based switching fabric**, at most one packet can traverse the bus at any instant, so the switching bandwidth is limited by the bus speed even if there are many input and output ports.

---

**4.** A crossbar (interconnection-network) switching fabric can, in principle, transfer multiple packets in parallel in a single time slot, as long as no two packets contend for the same output port.

---

**5.** Head-of-the-line (HOL) blocking occurs at an input queue when the packet at the front of the queue is prevented from moving forward (e.g., due to output contention), thereby blocking later packets in the queue that might otherwise be able to move.

---

**6.** Output port buffering is needed when packets arrive from the switching fabric faster than the output line rate, potentially causing queueing delay and loss due to buffer overflow.

---

**7.** FIFO (FCFS) scheduling guarantees each flow a minimum fraction of link bandwidth, regardless of the behavior of other flows.

---

**8.** In **priority scheduling**, packets are classified into priority classes, and the scheduler always serves the highest-priority non-empty queue, using FIFO within each class.

---

**9.** In **round-robin (RR) scheduling**, the server visits each non-empty class queue in turn, sending at most one packet per visit per class.

---

**10.** In **Weighted Fair Queueing (WFQ)**, each class (i) is assigned a weight (w_i) and, over time, receives a fraction of the link bandwidth proportional to its weight.

---

**11.** IPv4 addresses are 32 bits, while IPv6 addresses are 64 bits long.

---

**12.** In CIDR notation, the prefix length `/x` indicates how many **high-order** bits of the address form the network (subnet) part.

---

**13.** DHCP can provide more than just an IP address to a host; it can also provide the default gateway, DNS server(s), and subnet mask.

---

**14.** In a NAT setup, all internal hosts share one public IP address as seen from the outside, with the NAT device using TCP/UDP port numbers to demultiplex flows.

---

**15.** In OpenFlow-style generalized forwarding, flow-table entries match over possibly many header fields and specify actions such as forward out a port, drop, modify header fields, or send to the controller.

---

## Multiple Choice (16–25)

**16.** Which statement about **HOL blocking** is most accurate?

A. It occurs only in output queues.  
B. It occurs when input queues are too small relative to RTT.  
C. It occurs when a packet at the head of an input queue cannot be transferred (e.g., its output is busy), blocking packets behind it that might otherwise go.  
D. It occurs only when packets have variable length.

---

**17.** Which of the following buffer sizing rules was mentioned as an RFC “rule of thumb” for backbone routers?

A. Average buffering equal to link capacity only.  
B. Buffering equal to twice the link capacity.  
C. Average buffering equal to link capacity × a typical RTT (e.g., 250 ms).  
D. Buffering is unnecessary if WFQ is used.

---

**18.** Which scheduling discipline best matches: “each class gets a fraction (w_i / \sum_j w_j) of the link bandwidth”?

A. FIFO  
B. Priority  
C. Round Robin  
D. Weighted Fair Queueing (WFQ)

---

**19.** Which of the following is **not** a valid private IPv4 address block?

A. 10.0.0.0/8  
B. 172.16.0.0/12  
C. 192.168.0.0/16  
D. 11.0.0.0/8

---

**20.** Which statement about **CIDR** and route aggregation is correct?

A. CIDR forces all networks to have /24 prefixes.  
B. CIDR allows ISPs to advertise a single aggregated prefix for many customer networks, reducing routing table size.  
C. CIDR eliminates the need for BGP.  
D. CIDR is only used with IPv6.

---

**21.** Which of the following best describes **DHCP**?

A. A routing protocol that advertises subnets to other routers.  
B. A host configuration protocol that allows a host to dynamically obtain an IP address and related parameters from a server.  
C. A protocol used for address translation at a NAT.  
D. A protocol used to map IP addresses to MAC addresses on a LAN.

---

**22.** Which statement about **NAT** is **false**?

A. NAT modifies IP address and port fields in datagrams as they cross the NAT boundary.  
B. NAT maintains a translation table mapping internal (IP,port) to external (IP,port) pairs.  
C. NAT makes internal hosts directly reachable with their private IP addresses from anywhere on the Internet.  
D. NAT can allow many internal hosts to share one external IPv4 address.

---

**23.** Which of the following is **not** a change introduced in IPv6 relative to IPv4?

A. Expansion of address size from 32 bits to 128 bits.  
B. Removal of header checksum to speed up processing.  
C. Support for fragmentation by routers along the path.  
D. Simpler, fixed-length base header.

---

**24.** Which description best matches **tunneling** in the context of IPv6 transition?

A. Encapsulating IPv6 datagrams inside IPv4 datagrams when traversing an IPv4 network.  
B. Compressing IPv6 headers to fit in IPv4 headers.  
C. Running IPv4 over a physical serial cable.  
D. Using DHCP to assign IPv6 addresses to IPv4 hosts.

---

**25.** Which of the following is least aligned with the OpenFlow “match + action” abstraction?

A. Match on destination IP prefix, action: forward to output port 3.  
B. Match on TCP destination port 22, action: drop.  
C. Match on source IP, action: rewrite source IP and port (NAT).  
D. Match on process ID inside the payload, action: forward to a specific port.

---

## Free Response (26–32)

### 26. Input queuing delay vs switching fabric

A router has (N) input ports and (N) output ports. All packets have the same length and take time (D) to transmit on any link. Assume that in one “slot” of duration (D), at most **one** packet can cross the **memory** or **bus** fabric, but multiple packets can cross the **crossbar**, subject to output-port contention.

Now suppose that in a particular slot, **each** input port receives exactly one packet, and each packet is destined to a **different** output port.

(a) For **switching via memory**, what is the maximum time a packet might spend waiting in its input queue (i.e., maximum input queuing delay), in terms of (N) and (D)? Explain briefly.

(b) Answer the same question for **switching via a bus**.

(c) Answer the same question for a **crossbar** fabric, given the assumptions above.

---

### 27. WFQ weights and service sequences

A buffer implements **Weighted Fair Queueing (WFQ)** for **three classes** with weights:

- Class 1: (w_1 = 0.5)
    
- Class 2: (w_2 = 0.25)
    
- Class 3: (w_3 = 0.25)
    

Assume all packets are the same size and that the scheduler operates in discrete “service opportunities” (slots), sending at most one packet in each slot.

(a) Suppose all three classes always have packets waiting. Give an **example** of a repeating service sequence (like `1,2,1,3,...`) that approximates the WFQ shares over time.

(b) Suppose now that **class 3 has no packets** (its queue is empty), while classes 1 and 2 always have packets. Give an example of a repeating service sequence between classes 1 and 2 that respects the intended relative weights.

(You don’t need to be perfectly exact—just approximate the fractions correctly.)

---

### 28. Longest-prefix forwarding ranges (8-bit addresses)

Consider an 8-bit destination address space (addresses 0–255). A router uses **longest prefix matching** with this table:

|Prefix|Interface|
|---|---|
|00|0|
|010|1|
|011|2|
|1|3|

(a) For each interface (0–3), give the **range of destination addresses** (in decimal) that will be forwarded out that interface, assuming longest prefix matching.

(b) For each interface, state how many addresses are in its range.

---

### 29. Subnetting with CIDR

You are given a block of addresses: **192.168.16.0/24**. You must create **three subnets** with these minimum host requirements:

- Subnet A: at least 100 hosts
    
- Subnet B: at least 50 hosts
    
- Subnet C: at least 20 hosts
    

(a) For each subnet (A, B, C), choose a prefix **192.168.16.x/y** that satisfies the minimum host requirement (assume you can reuse remaining space arbitrarily). Try to minimize wasted addresses.

(b) For each subnet, specify the **usable host address range** (lowest and highest usable addresses).

---

### 30. NAT translation table

A home network uses private addresses 10.0.0.0/24 and has a single public address **138.76.29.7** on the NAT router’s WAN interface. Hosts:

- Host A: 10.0.0.1
    
- Host B: 10.0.0.2
    

The following **outgoing TCP connections** exist (all to external web servers on port 80):

1. A → 128.119.40.86:80, with source port 5001 at A
    
2. A → 64.12.10.5:80, with source port 5002 at A
    
3. B → 128.119.40.86:80, with source port 5001 at B
    

Assume the NAT chooses distinct external (WAN-side) source ports for each mapping: 30000, 30001, 30002, in that order.

(a) Fill in the NAT translation table with entries of the form:  
`(inside IP, inside port, outside IP, outside port) <-> (NAT IP, NAT port)`.

(b) Show the **source IP and port** that a server on the Internet would see for each of the three connections.

---

### 31. IPv4 fragmentation

An IPv4 host wants to send a **4000-byte** datagram (including the 20-byte IPv4 header) over a link with **MTU = 1500 bytes**.

(a) How many fragments will be produced?

(b) For each fragment, give:

- Total length (header + data)
    
- Data payload size
    
- Fragment offset field value (in 8-byte units)
    
- MF (More Fragments) flag (1 or 0)
    

Assume no options, 20-byte header on each fragment.

---

### 32. OpenFlow flow table design

Consider the OpenFlow network like the one in your slides (hosts h1–h6 and switches s1–s3). Focus on switch **s2**, which has:

- Port 1 connected toward h5/h6 (via some path)
    
- Port 2 connected toward h1/h2 (via some path)
    
- Ports 3 and 4 directly connected to h3 and h4, respectively
    

IP addresses:

- h1: 10.1.0.1
    
- h2: 10.1.0.2
    
- h3: 10.2.0.3
    
- h4: 10.2.0.4
    
- h5: 10.3.0.5
    
- h6: 10.3.0.6
    

Desired behavior at s2:

- Any packet arriving on **port 1** from h5/h6 destined to h1 or h2 should be forwarded out **port 2**.
    
- Any packet arriving on **port 2** from h1/h2 destined to h5 or h6 should be forwarded out **port 1**.
    
- Any packet destined to h3 or h4 should be delivered to the correct directly-attached host (ports 3 and 4).
    
- h3 and h4 should be able to send packets to each other via s2.
    

Specify a set of **flow-table entries** for s2 that implements this behavior. For each entry, indicate:

- Match (on input port and/or destination IP)
    
- Action (output port)
    

You can ignore priorities and counters.

---
