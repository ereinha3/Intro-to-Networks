# Chapter 3 – Transport Layer (Detailed Notes)

## 1. Role of the Transport Layer

### 1.1 Logical Communication Between Processes

* **Network layer:** logical communication **between hosts**
* **Transport layer:** logical communication **between application processes**

Key responsibilities:

* Segmentation & reassembly
* Multiplexing/demultiplexing
* Reliable data transfer (if provided)
* Flow control
* Congestion control

Transport protocols run **only at end systems**; routers do not implement transport logic.

---

## 2. Multiplexing & Demultiplexing

### 2.1 What They Mean

* **Multiplexing (sender):** take data from multiple sockets → add transport header → hand to IP
* **Demultiplexing (receiver):** use header fields → deliver segment to correct socket

---

### 2.2 Connectionless Demultiplexing (UDP)

* Identified by:

  * **Destination port only**

All UDP datagrams with:

* Same destination port → same socket
* Source IP/port may differ

**Implication:** one UDP socket can serve **many clients simultaneously**.

---

### 2.3 Connection‑Oriented Demultiplexing (TCP)

Each TCP socket identified by a **4‑tuple**:

(source IP, source port, destination IP, destination port)

* Server can maintain **many simultaneous sockets** on the **same server port (e.g., 80)**
* Each client connection is identified uniquely by the 4‑tuple

---

## 3. UDP — User Datagram Protocol

### 3.1 UDP Service Model

* Connectionless
* Unreliable
* Unordered
* No congestion control
* No flow control
* No retransmissions

Used when:

* Low latency is critical
* Some data loss is acceptable

Examples:

* DNS
* Streaming media
* VoIP
* Games
* QUIC / HTTP‑3

---

### 3.2 UDP Segment Format

| Field            | Size     |
| ---------------- | -------- |
| Source Port      | 16 bits  |
| Destination Port | 16 bits  |
| Length           | 16 bits  |
| Checksum         | 16 bits  |
| Data             | Variable |

---

### 3.3 UDP Checksum (Internet Checksum)

Goal: detect bit errors

Algorithm:

1. Treat all 16‑bit words as integers
2. Compute **one’s complement sum**
3. Take one’s complement of the result → checksum
4. Receiver recomputes and checks for all‑ones result

⚠️ Detects many but **not all** errors.

---

## 4. Principles of Reliable Data Transfer (rdt)

Reliable data transfer must handle:

* Bit errors
* Packet loss
* Duplicate packets
* Reordering

We model protocols using **Finite State Machines (FSMs)**.

---

### 4.1 rdt1.0 — Perfect Channel

Assumptions:

* No loss
* No corruption

Operation:

* Sender sends packet
* Receiver delivers packet

No ACKs required.

---

### 4.2 rdt2.0 — Bit Errors

Adds:

* Checksum
* ACK / NAK

Sender behavior:

* Send packet
* If NAK → retransmit
* If ACK → send next

⚠️ **Fatal flaw:** corrupted ACK/NAK causes ambiguity.

---

### 4.3 rdt2.1 — Sequence Numbers

Fix for corrupted ACKs:

* Add **sequence numbers (0,1)**
* Detect duplicates
* Receiver discards duplicate packets

---

### 4.4 rdt2.2 — NAK‑free Protocol

* Uses only **ACKs**
* Duplicate ACK functions as NAK

TCP uses this strategy.

---

### 4.5 rdt3.0 — Packet Loss + Errors

Adds:

* **Timers**
* Retransmission on timeout

Sender:

* Start timer when packet sent
* If timeout → retransmit
* If ACK received → move forward

Still **stop‑and‑wait** → poor utilization.

---

## 5. Pipelined Reliable Protocols

### 5.1 Motivation

Stop‑and‑wait utilization:

U = (L/R) / (RTT + L/R)

Very inefficient for long‑delay links.

---

## 6. Go‑Back‑N (GBN)

### Sender

* Window size = N
* Sequence numbers modulo k
* **Single timer for oldest unACKed** packet
* On timeout: retransmit **all packets in window**

### Receiver

* Only accepts next expected sequence number
* Discards out‑of‑order packets
* Sends **cumulative ACK**

---

## 7. Selective Repeat (SR)

### Sender

* Maintains **timer per packet**
* Retransmits only timed‑out packets

### Receiver

* Buffers out‑of‑order packets
* ACKs each packet individually

### Critical Rule

To avoid ambiguity:

**Window size ≤ (Sequence Space) / 2**

---

## 8. TCP Overview

TCP provides:

* Reliable
* In‑order
* Byte‑stream service
* Full duplex
* Flow control
* Congestion control

Connection‑oriented via **3‑way handshake**.

---

## 9. TCP Segment Structure

Key fields:

* Sequence Number
* Acknowledgment Number
* Window Size (rwnd)
* Flags: SYN, ACK, FIN
* Checksum
* Data

---

## 10. TCP Sequence Numbers & ACKs

* Sequence number = **byte number** of first byte in segment
* ACK number = **next expected byte**
* ACKs are **cumulative**

---

## 11. TCP RTT Estimation & Timeout

### Estimated RTT (EWMA)

EstimatedRTT = (1 − α)·EstimatedRTT + α·SampleRTT

Typical α = 0.125

---

### Deviation

DevRTT = (1 − β)·DevRTT + β·|SampleRTT − EstimatedRTT|

TimeoutInterval = EstimatedRTT + 4·DevRTT

---

## 12. TCP Fast Retransmit

* Triggered by **3 duplicate ACKs**
* Retransmit **without waiting for timeout**

---

## 13. TCP Flow Control

Goal: protect **receiver buffer**

Receiver advertises:

* **rwnd (receive window)**

Sender ensures:

In‑flight data ≤ rwnd

Prevents buffer overflow.

---

## 14. TCP Connection Management

### 3‑Way Handshake

1. Client → SYN(x)
2. Server → SYN(y), ACK(x+1)
3. Client → ACK(y+1)

Establishes:

* Initial sequence numbers
* Agreement to communicate

---

### Connection Teardown

* FIN from one side
* ACK from other
* FIN back
* Final ACK

Both sides close independently.

---

## 15. Congestion Control: Core Concept

Congestion:

> Too many senders transmitting too fast for routers to handle

Effects:

* Large queuing delays
* Packet loss
* Wasted retransmissions

Distinct from flow control.

---

## 16. TCP Congestion Control: AIMD

### Additive Increase

cwnd increases **linearly** every RTT

### Multiplicative Decrease

On loss:

* cwnd ← cwnd / 2  (Reno)
* cwnd ← 1 MSS     (Tahoe)

Creates **sawtooth behavior**.

---

## 17. TCP Slow Start

Initial phase:

* cwnd starts at 1 MSS
* cwnd **doubles every RTT**

Exponentially ramps up throughput.

---

### Transition to Congestion Avoidance

Threshold = **ssthresh**

* When cwnd ≥ ssthresh → switch to additive increase
* On loss: ssthresh = cwnd / 2

---

## 18. TCP Fairness

If K TCP flows share bottleneck R:

Each should get ≈ R/K throughput

⚠️ Fairness can be broken by:

* Parallel TCP connections
* UDP‑based streaming

---

## 19. Alternative Congestion Control

### Delay‑Based (BBR)

* Uses RTT increase instead of packet loss
* Keeps pipe “just full enough”
* Deployed by Google

---

### Explicit Congestion Notification (ECN)

* Routers mark packets instead of dropping
* TCP adjusts cwnd without loss

---

## 20. QUIC (HTTP‑3 Transport)

* Runs over UDP
* Implements:

  * Reliability
  * Congestion control
  * Encryption

### Key Advantages:

* 1‑RTT handshake
* No head‑of‑line (HOL) blocking
* Multiple streams per connection

---

## 21. TCP Throughput Model

Average throughput:

Throughput ≈ (3/4 · W) / RTT

Where:

* W = window size at loss

Large BDP (bandwidth‑delay product) requires:

* Very large window
* Very low loss rate

---

## 22. Final Chapter 3 Takeaways

* UDP = fast but unreliable
* TCP = reliable, flow‑controlled, congestion‑controlled
* rdt protocols show how reliability is built from scratch
* GBN & SR trade complexity for performance
* AIMD enforces stability and fairness
* QUIC modernizes transport for web traffic

