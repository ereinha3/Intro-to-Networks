1. T
2. T
3. F
4. T
5. T
6. T
7. F
8. T
9. T
10. F
11. T
12. F
13. T
14. T
15. T
16. C
17. B
18. B X
19. D
20. A X
21. A X
22. A
23. B
24. B
25. C
26. Q
$$
\begin{matrix}
& a & b & c & d & e \\
a & 0 & 3 & 1 & 0 & 0 \\
b &  & 0 & 7 & 5 & 0 \\
c &  &  & 0 & 2 & 7 \\
d &  &  &  & 0 & 3 \\
e &  &  &  &  & 0 \\
\end{matrix}
$$

| Node Set        | D(b), p(b) | D(c), p(c) | D(d), p(d) | D(e), p(e) |
| --------------- | ---------- | ---------- | ---------- | ---------- |
| {a}             | 3, a       | 1, a       | $\infty$   | $\infty$   |
| {a, c}          | 3, a       | 1, a       | 3, c       | 8, c       |
| {a, c, b}       | 3, a       | 1, a       | 3, c       | 8, c       |
| {a, c, b, d}    | 3, a       | 1, a       | 3, c       | 8, c       |
| {a, c, b, d, e} | 3, a       | 1, a       | 3, c       | 8, c       |

27. Q
	1. $D_y(x) = 4$; $D_y(y) = 0$; $D_y(z) = 1$
	2. Becomes 5 as $D_x(y) + D_y(z) = 4 + 1 < 7$
	3. x -> y -> z
28. This happens with increasing costs. Lets have routers A, B, and C. Imagine these are in a straight line with A - B - C. Lets say they all start at cost 1. Now lets say in one timestep, B - C goes under load and the cost updates to 4. However, if A, which had cost 2 to C going through B, broadcasts before it recieves the update from B, then B thinks it can now get to C in length 3 which is better than its current length of 4. Then this cycle will continue and the number will keep getting higher. Poison reverse solves this occurence by forcing a max hop count.
29. Q

|                                   | Link State                                                                                | Distance Vector                                                                                     |
| --------------------------------- | ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Information each router stores    | Global Topology                                                                           | Local links and estimates to distant nodes                                                          |
| Message complexity                | Links are broadcasted to every node. Floods network with every link distance.             | Periodically push updated estimates. Re-broadcast on any changes.                                   |
| Convergence behavior and problems | Both have oscillations and count to infinity                                              | <-                                                                                                  |
| Robustness                        | More robust, full network topology so a bad link will be resolved after a single attempt. | Malfunctioning router can broadcast low links and this will propagate throughout the whole network. |
|                                   |                                                                                           |                                                                                                     |
30. Q
	1. Comparison
		1. OSPF
			1. This is responsible for computing routes between all routers within the AS. Uses distance vectors and dictates where to send traffic inside.
		2. BGP
			1. eBGP: communicates reachability and preferences
			2. iBGP: propagates external reachability internally
	2. IntraAS allows for complete control over ones own topology. Feasible to do link-state within. BGP establishes standards for communicating between and lets internal routing protocol be abstracted.
31. Q
	1. Route 2: shorter AS_PATH
	2. Route 1: exit to AS2 preferred
32. Q
	1. Explain
		1. Traditional: IDK
		2. Distributed: LS or DV. Routers determine their own forwarding tables by communicating with other routers.
		3. SDN: Central organizer that pushes preferences and forwarding tables to routers to abide by. Routers can override this but central organizer is responsible for all computation typically.
	2. Advantage: more control over network. Can have more complicated and dynamic routing. Dedicated box to handle all computation so routers just forward and update forwarding tables
	3. Disadvantage: central organizer goes down, entire network goes down.