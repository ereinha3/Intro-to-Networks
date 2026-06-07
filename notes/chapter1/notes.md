# Chapter 1 – Internet Fundamentals 

## 1. What Is the Internet?

### 1.1 The Internet as a “Network of Networks”

The Internet is not a single network. It is a **massively interconnected collection of independent networks**, called **Autonomous Systems (AS)**, typically operated by:

* Access ISPs (home, mobile, enterprise)
* Regional ISPs
* Tier-1 global ISPs
* Content provider networks (Google, Netflix, Facebook, etc.)
* Datacenter networks

Every device connects into an **access network**, and access networks interconnect through ISP networks. No central authority controls the full Internet topology.

---

### 1.2 The Internet as a “Service Platform”

From the application perspective, the Internet is a **programmable communication service** that provides:

* Process-to-process communication
* Reliability (TCP)
* Best-effort delivery (UDP)
* Security overlays (TLS)

Applications such as:

* Web (HTTP)
* Streaming video
* Email
* Multiplayer games
* Cloud computing
* Social media

are all built **on top of these communication services**, not directly on physical hardware.

---

## 2. What Is a Protocol?

A **protocol** defines:

1. **Message format**
2. **Message ordering**
3. **Actions taken upon sending or receiving messages**

### 2.1 Human vs Network Protocols

Human protocol example:

* “What time is it?” → “2 PM” → acknowledgment

Network protocol example:

* SYN → SYN-ACK → ACK (TCP handshake)

Protocols eliminate ambiguity and enable automation.

---

## 3. Network Edge

### 3.1 Hosts

Hosts include:

* Clients (browsers, phones, laptops)
* Servers (web servers, cloud servers, mail servers)

Servers are commonly deployed inside **datacenters**.

---

### 3.2 Access Networks

Access networks connect hosts to the first router.

#### (A) Cable (HFC – Hybrid Fiber Coax)

* Shared medium
* Downstream: ~40 Mbps – 1.2 Gbps
* Upstream: ~30–100 Mbps
* Uses **Frequency Division Multiplexing (FDM)**

#### (B) DSL

* Uses telephone lines
* Dedicated per home
* Central Office + DSLAM
* Downstream: 24–52 Mbps
* Upstream: 3.5–16 Mbps

#### (C) Wireless (WiFi, 4G/5G)

* Shared medium
* WiFi: ~11–100s Mbps
* Cellular: ~10s Mbps

#### (D) Enterprise Networks

* Ethernet + WiFi
* Switches and routers
* High throughput (1–10+ Gbps)

---

## 4. Physical Media

### 4.1 Guided Media

| Medium        | Properties                           |
| ------------- | ------------------------------------ |
| Twisted Pair  | Low cost, moderate bandwidth         |
| Coaxial Cable | Broadband, shared                    |
| Fiber Optic   | Very high bandwidth, low attenuation |

### 4.2 Unguided Media

* Radio
* Satellite
* Microwave

Issues:

* Interference
* Reflection
* Obstruction
* Half-duplex behavior

---

## 5. Network Core

### 5.1 Packet Switching

Data is broken into **packets**.
Each packet:

* Routed independently
* Uses store-and-forward switching
* Shares link bandwidth

#### Transmission Delay:

( d_{trans} = L/R )

* L = packet length (bits)
* R = transmission rate (bps)

Store & forward implies **entire packet must arrive** at router before forwarding.

---

### 5.2 Queueing and Packet Loss

Packets queue when:
( La > R )

* a = arrival rate
* L = packet size

Traffic intensity:
( \rho = La/R )

If ( \rho > 1 ), queue grows without bound → loss occurs.

---

### 5.3 Circuit Switching

Resources reserved end-to-end.

Techniques:

* **FDM**: Fixed frequency slots
* **TDM**: Fixed time slots

Properties:

* Guaranteed bandwidth
* Idle capacity wasted if unused

---

## 6. Internet Structure

Hierarchical design:

* Tier-1 ISPs
* Regional ISPs
* Access ISPs
* Content Provider Networks

Economic policies guide interconnections.

---

## 7. Network Delay

Total nodal delay:

( d_{nodal} = d_{proc} + d_{queue} + d_{trans} + d_{prop} )

| Delay Type   | Cause             |
| ------------ | ----------------- |
| Processing   | Header checks     |
| Queueing     | Congestion        |
| Transmission | Bit pushing       |
| Propagation  | Physical distance |

Propagation:
( d_{prop} = d/s )

---

## 8. Traceroute & ICMP

Traceroute works by:

* Sending packets with increasing TTL
* Routers return ICMP Time Exceeded messages
* RTT measured per hop

`* * *` appears when responses are blocked or lost.

---

## 9. Throughput

Throughput = **actual achieved data rate**.

Bottleneck rule:

End-to-end throughput = **minimum link rate along path**

---

## 10. Network Security Basics

### 10.1 Malware

* Virus – user-executed
* Worm – autonomously spreading
* Spyware – surveillance

### 10.2 Botnets & DDoS

Large numbers of compromised hosts flood targets.

### 10.3 Packet Sniffing

Promiscuous NICs capture all traffic.

### 10.4 IP Spoofing

Fake source IP for attacks.

---

## 11. Protocol Layering

### 11.1 Internet Protocol Stack

| Layer       | Purpose              |
| ----------- | -------------------- |
| Application | Network apps         |
| Transport   | End-to-end delivery  |
| Network     | Routing (IP)         |
| Link        | Local frame delivery |
| Physical    | Bit transmission     |

---

### 11.2 Encapsulation

Message → Segment → Datagram → Frame → Bits

Each layer wraps the previous payload.

---

## 12. Why Layering?

* Modular design
* Easier upgrades
* Fault isolation
* Vendor interoperability

---

## 13. OSI Model vs Internet Model

| OSI                                        | Internet |
| ------------------------------------------ | -------- |
| 7 layers                                   | 5 layers |
| Presentation + Session missing in Internet |          |

Those services moved to applications.

---

## 14. Internet History Timeline

* 1961 – Queueing theory
* 1969 – ARPANET
* 1983 – TCP/IP
* 1988 – Congestion control
* 1991 – Commercial Internet
* 2000s – Web, P2P
* 2010s – Cloud, Mobile

---

## 15. Key Exam Takeaways

* Internet = packet-switched network of networks
* Packet switching ≠ circuit switching
* Queueing dominates delay under congestion
* Throughput limited by bottleneck link
* Layering enables scale and evolution
* Security was retrofitted

