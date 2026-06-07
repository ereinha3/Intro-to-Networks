1. F (flipped)
2. T
3. F
4. T
5. F
6. T
7. T X
8. T
9. T
10. F
11. T
12. F
13. T
14. T
15. T
16. C
17. B X
18. C
19. D X
20. B
21. A X
22. D
23. C
24. C
25. B
26. Q
	1. 1. (a) & (b) : $$ \begin{matrix}  
1 & 0 & 1 & 1 & | & 1\\  
0 & 0 & 0 & 1 & | & 1\\ 
1 & 1 & 0 & 0 & | & 0\\ 
0 & 1 & 1 & 0 & | & 0\\ 
- & - & - & - & | & \\ 
0 & 0 & 0 & 0 &  & 0 \\ 
\end{matrix}  
$$
	1.  New matrix: $$ \begin{matrix}  
1 & 0 & 1 & 1 & | & 1\\  
0 & 0 & 1 & 1 & | & 1\\ 
1 & 1 & 0 & 0 & | & 0\\ 
0 & 1 & 1 & 0 & | & 0\\ 
- & - & - & - & | & \\ 
0 & 0 & 0 & 0 &  & 0 \\ 
\end{matrix}  
$$
		Row 2 parity is now incorrect and Col 3 parity is now incorrect so Row 2 Col 3 must be flipped bit.

1. 27.
	1. |R| = |G| - 1 = 3
	2. D = 1011 (11); G = 1101 (13); D * 2^{3} = 1011000; $$ \require{enclose}  
\begin{array}{rll}  
11 \phantom{000}&& \\[-3pt]  
1101 \enclose{longdiv}{1011000} \\[-3pt]  
\underline{1101\phantom{000}} && \\[-3pt]  
01100\phantom{00} && \\[-3pt]  
\underline{1101\phantom{00}} && \\[-3pt]  
000100 && \\[-3pt]  
\end{array}  
$$ so R = 100
	3. <1011, 100> is final sequence
2. (28)
	1. $P_1 = 20 * 0.95^{19} * 0.05 = 0.37735360253$ 
	2. ^^
	3. ~38% of the time, a frame will be successful per slot
3. (29)
	1. Time to send Q = Q / R = 10,000 / 10,000,000 = 0.1ms
		1. $B = \frac{R}{\frac{\frac{Q}{R} + d_{poll}}{\frac{Q}{R}}}$
		2. $B = \frac{R}{1 + \frac{R*d_{poll}}{Q}}$
		3. $B = \frac{R * Q}{Q + R * d_{poll}}$
	2. 5Mbps
4. (30)
	1. A will send out an ARP query and to R2. 
	2. R2 responds and R1 will already have MAC - IP forwarding given the ARP query from A so the response will return to A.
	3. Then A sends to IP. First hop mac is R1:R1:R1:R1:R1:R1, next hop max is R2:R2:R2:R2:R2:R2 then last hop to dest is BB:BB:BB:BB:BB:BB. 
	4. R2 will know IP - MAC map because B responded to the ARP query for its address and can successfully route the traffic to the corresponding MAC given the IP.
5. (31)
	1. A to B: 
		1. A sends frame to switch, switch doesn't know where B is so its floods, gets B and C's macs. Then sends packet to B, holding it all the while. 
		2. MAC table contain A, B, and C now.
	2. B to A: 
		1. B sends frame to switch, unicast
		2. MAC tables stays the same
	3. C to A:
		1. C sends frame to switch, unicast
		2. MAC table stays the same
6. 32
	1. H1 sends to S1. S1 tags this package with the appropriate tag. S1 grabs tag and sees H3 in S2's ARP table. Sends to S2. S2 untags the package and confirms that it can go to VLAN 10. Forwards package to H3/
	2. Same exact thing but switch the VLANs.