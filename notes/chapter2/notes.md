# Chapter 2 – Application Layer (Detailed Notes)

## 1. Principles of Network Applications

### 1.1 What Is a Network Application?

A network application is a **distributed system** consisting of programs running on **different end systems** that communicate over the network using **application-layer protocols**.

Key idea:

> **Application logic runs only at the network edge (hosts), not in the network core (routers/switches).**

This enables:

* Rapid application development
* No changes required to routers
* Scalability of innovation

---

## 2. Application Architectures

### 2.1 Client–Server Architecture

**Server:**

* Always-on
* Permanent IP address
* Usually located in a data center

**Clients:**

* Intermittently connected
* Dynamic IP addresses
* Do not communicate with each other

Examples:

* Web (HTTP)
* Email (IMAP, FTP)
* Cloud services

**Advantages:**

* Centralized management
* Easier security

**Disadvantages:**

* Scalability limits
* Single point of failure

---

### 2.2 Peer-to-Peer (P2P) Architecture

* No always-on central server
* Peers communicate directly
* Each peer both **requests and provides services**
* Peers frequently join and leave ("churn")

Examples:

* BitTorrent
* P2P streaming
* Skype (early)

**Key property: Self-scalability**

> As peers increase, total system capacity increases.

**Disadvantages:**

* Hard to manage
* Security challenges
* NAT/firewall issues

---

## 3. Processes, Sockets, and Addressing

### 3.1 Process Communication

* A **process** is a running program
* Processes on the **same host** use OS IPC
* Processes on **different hosts** exchange **messages over the network**

Definitions:

* **Client process:** initiates communication
* **Server process:** waits for requests

---

### 3.2 Sockets

A **socket** is the API between:

* The application process
* The transport-layer protocol (TCP or UDP)

> A socket is like a "door" between the app and the transport layer.

Two sockets per connection:

* One at the sender
* One at the receiver

---

### 3.3 Addressing Processes

A process is uniquely identified by:

**(IP address, Port number)**

Examples:

* HTTP server: Port 80
* HTTPS: Port 443
* SMTP: Port 25

Why both are required:

* One host can run many applications

---

## 4. Application-Layer Protocol Definition

An application-layer protocol defines:

1. **Message types** (request, response)
2. **Message syntax** (fields & formats)
3. **Message semantics** (meaning of fields)
4. **Rules** for sending and responding

Types:

* **Open protocols:** HTTP, SMTP, DNS (RFC-defined)
* **Proprietary protocols:** Skype, Discord

---

## 5. Transport Services & Application Requirements

### 5.1 Application Requirements

| Requirement    | Meaning                    |
| -------------- | -------------------------- |
| Data integrity | 100% reliable delivery     |
| Timing         | Low delay required         |
| Throughput     | Minimum bandwidth needed   |
| Security       | Encryption, authentication |

---

### 5.2 TCP vs UDP

#### TCP Services

* Reliable
* In-order
* Flow control
* Congestion control
* Connection-oriented

#### UDP Services

* Unreliable
* No ordering
* No congestion control
* No connection setup

**Why UDP exists:**

* Low latency
* No retransmission delays
* Useful for streaming, gaming, DNS

---

## 6. Transport Layer Security (TLS)

* Provides:

  * Encryption
  * Data integrity
  * Authentication
* Implemented in application layer
* Runs on top of TCP

---

# HTTP (Web Protocol)

## 7. Structure of the Web

A web page consists of:

* A **base HTML file**
* Referenced objects (images, videos, CSS, JS)

Each object has a separate URL.

---

## 8. HTTP Overview

* Application-layer protocol
* Client/server
* Runs over TCP
* Stateless by default

---

## 9. Non-Persistent vs Persistent HTTP

### Non-Persistent

* One TCP connection per object
* **2 RTTs per object**

**Total delay:**

**2RTT + file transmission time**

---

### Persistent (HTTP/1.1)

* Single TCP connection
* Multiple objects transmitted
* Pipelining possible

**Advantages:**

* Fewer RTTs
* Less OS overhead

---

## 10. HTTP Messages

### HTTP Request Structure

* Request line: METHOD URL VERSION
* Header lines
* Optional body

Methods:

* GET
* POST
* HEAD
* PUT

---

### HTTP Response Structure

* Status line
* Header fields
* Entity body

Common status codes:

* 200 OK
* 301 Moved Permanently
* 400 Bad Request
* 404 Not Found
* 505 Version Not Supported

---

## 11. Cookies (State over Stateless HTTP)

Cookies enable:

* Login sessions
* Shopping carts
* Recommendations

4 parts:

1. Set-Cookie header
2. Cookie request header
3. Browser cookie file
4. Server database

Privacy issue: third-party tracking

---

## 12. Web Caching (Proxy Servers)

* Cache stores copies of frequently accessed objects
* Acts as both server and client

Benefits:

* Reduces access link load
* Improves response time
* Cheaper than upgrading bandwidth

---

### Cache Performance Formula

Let:

* ( \Delta = F/R )
* ( b ) = request rate

Access delay:

[ \frac{\Delta}{1 - \Delta b} ]

Average delay with cache hit rate H:

[ (1-H) \cdot d_{origin} + H \cdot d_{cache} ]

---

## 13. Conditional GET

* Prevents sending object if unchanged
* Uses:

  * If-Modified-Since
  * 304 Not Modified

---

# Email Protocols

## 14. SMTP (Sending Mail)

* TCP-based
* Port 25
* Push protocol
* 7-bit ASCII
* Persistent connections

Phases:

1. Handshake
2. Transfer
3. Closure

---

## 15. Mail Format

* Header: To, From, Subject
* Blank line
* Body

Header is **inside the message body**, different from SMTP commands

---

## 16. Mail Access Protocols

* **IMAP:** Server-side storage, folders
* **POP:** Download then delete
* **HTTP:** Web-based email (Gmail, Yahoo)

---

# DNS – Domain Name System

## 17. DNS Purpose

Maps:

* Hostname → IP address
* Mail server resolution
* Load balancing

---

## 18. Hierarchical DNS Structure

1. Root servers
2. TLD servers (.com, .edu, etc.)
3. Authoritative servers
4. Local DNS servers

---

## 19. DNS Query Types

### Iterative

* Server returns next server to ask

### Recursive

* Server resolves entire chain

---

## 20. DNS Caching

* Cached via TTL
* Improves speed
* Can become stale

---

## 21. DNS Resource Records

Format:

(name, value, type, TTL)

Types:

* A: hostname → IP
* NS: domain → name server
* CNAME: alias
* MX: mail server

---

# P2P File Distribution

## 22. Client–Server vs P2P File Distribution

### Client–Server Distribution Time

[ D_{CS} = \max \left( \frac{NF}{u_s}, \frac{F}{d_{min}} \right) ]

---

### P2P Distribution Time

[ D_{P2P} = \max \left( \frac{F}{u_s}, \frac{F}{d_{min}}, \frac{NF}{u_s + \sum u_i} \right) ]

---

## 23. BitTorrent

* File divided into chunks
* Tracker coordinates peers
* **Rarest-first chunk selection**
* **Tit-for-tat upload policy**

Optimistic unchoking improves partner discovery

---

# Video Streaming + CDNs

## 24. Streaming Challenges

* Variable bandwidth
* Jitter
* Packet loss

---

## 25. DASH (Adaptive Streaming)

* Video split into chunks
* Chunks encoded at multiple rates
* Client selects rate dynamically

---

## 26. Content Distribution Networks (CDNs)

* Geo-distributed servers
* Redirect users to nearest copy

Benefits:

* Low latency
* High throughput
* Scalability

---

# Socket Programming

## 27. UDP Socket Programming

* No handshake
* sendto(), recvfrom()
* Unreliable

---

## 28. TCP Socket Programming

* connect(), accept()
* Reliable byte stream
* New socket per client

---

# 29. Key Exam Takeaways

* HTTP is stateless
* DNS is hierarchical
* SMTP pushes, HTTP pulls
* P2P scales better than client-server
* DASH adapts bitrate dynamically
* CDNs bring content closer
* TCP = reliable, UDP = fast

