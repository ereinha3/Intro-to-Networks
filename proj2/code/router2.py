import socket
import sys
import traceback
import time
from threading import Thread
from pathlib import Path

from .config import HOST, PORT_R2, PORT_R3, PORT_R4, INPUT_DIR


# Helper Functions

# The purpose of this function is to set up a socket connection.
def create_socket(host, port, retries=None, delay=0.5):
    attempt = 0
    while True:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            soc.connect((host, port))
            return soc
        except OSError as exc:
            soc.close()
            attempt += 1
            if retries is not None and attempt >= retries:
                print(f"Connection Error to {port}: {exc}")
                sys.exit()
            print(f"Waiting for router on port {port} (attempt {attempt}): {exc}")
            time.sleep(delay)


# The purpose of this function is to read in a CSV file.
def read_csv(filename):
    # 1. Open the file for reading.
    table_path = INPUT_DIR / filename if not Path(filename).is_absolute() else Path(filename)
    table_file = open(table_path, "r")
    # 2. Store each line.
    table = table_file.readlines()
    # 3. Create an empty list to store each processed row.
    table_list = []
    # 4. For each line in the file:
    for line in table:
        line = line.strip()
        if line == "":
            continue
        # 5. split it by the delimiter,
        parts = line.split(",")
        # 6. remove any leading or trailing spaces in each element, and
        parts = [p.strip() for p in parts]
        # 7. append the resulting list to table_list.
        table_list.append(parts)
    # 8. Close the file and return table_list.
    table_file.close()
    return table_list


# The purpose of this function is to find the default port
# when no match is found in the forwarding table for a packet's destination IP.
def find_default_gateway(table):
    # 1. Traverse the table, row by row,
    for row in table:
        # 2. and if the network destination of that row matches 0.0.0.0,
        if row[0] == "0.0.0.0":
            # 3. then return the interface of that row.
            return row[3]
    return None


# The purpose of this function is to generate a forwarding table that includes the IP range for a given interface.
# In other words, this table will help the router answer the question:
# Given this packet's destination IP, which interface (i.e., port) should I send it out on?
def generate_forwarding_table_with_range(table):
    # 1. Create an empty list to store the new forwarding table.
    new_table = []
    # 2. Traverse the old forwarding table, row by row,
    for row in table:
        # 3. and process each network destination other than 0.0.0.0
        # (0.0.0.0 is only useful for finding the default port).
        if row[0] != "0.0.0.0":
            # 4. Store the network destination and netmask.
            network_dst_string = row[0]
            netmask_string = row[1]
            # 5. Convert both strings into their binary representations.
            network_dst_bin = ip_to_bin(network_dst_string)
            netmask_bin = ip_to_bin(netmask_string)
            # 6. Find the IP range.
            ip_range = find_ip_range(network_dst_bin, netmask_bin)
            # 7. Build the new row.
            new_row = [
                row[0],
                row[1],
                row[2],
                row[3],
                ip_range[0],
                ip_range[1],
            ]
            # 8. Append the new row to new_table.
            new_table.append(new_row)
    # 9. Return new_table.
    return new_table


# The purpose of this function is to convert a string IP to its binary representation.
def ip_to_bin(ip):
    # 1. Split the IP into octets.
    ip_octets = ip.split(".")
    # 2. Create an empty string to store each binary octet.
    ip_bin_string = ""
    # 3. Traverse the IP, octet by octet,
    for octet in ip_octets:
        # 4. and convert the octet to an int,
        int_octet = int(octet)
        # 5. convert the decimal int to binary,
        bin_octet = bin(int_octet)
        # 6. convert the binary to string and remove the "0b" at the beginning of the string,
        bin_octet_string = bin_octet[2:]
        # 7. while the sting representation of the binary is not 8 chars long,
        # then add 0s to the beginning of the string until it is 8 chars long
        # (needs to be an octet because we're working with IP addresses).
        while len(bin_octet_string) < 8:
            bin_octet_string = "0" + bin_octet_string
        # 8. Finally, append the octet to ip_bin_string.
        ip_bin_string = ip_bin_string + bin_octet_string
    # 9. Once the entire string version of the binary IP is created, convert it into an actual binary int.
    ip_int = int(ip_bin_string, 2)
    # 10. Return the binary representation of this int.
    return bin(ip_int)


# The purpose of this function is to find the range of IPs inside a given a destination IP address/subnet mask pair.
def find_ip_range(network_dst, netmask):
    network_int = int(network_dst, 2)
    netmask_int = int(netmask, 2)
    # 1. Perform a bitwise AND on the network destination and netmask
    # to get the minimum IP address in the range.
    bitwise_and = network_int & netmask_int
    # 2. Perform a bitwise NOT on the netmask
    # to get the number of total IPs in this range.
    compliment = bit_not(netmask_int)
    min_ip = bitwise_and
    # 3. Add the total number of IPs to the minimum IP
    # to get the maximum IP address in the range.
    max_ip = min_ip + compliment
    # 4. Return a list containing the minimum and maximum IP in the range.
    return [min_ip, max_ip]


# The purpose of this function is to perform a bitwise NOT on an unsigned integer.
def bit_not(n, numbits=32):
    return (1 << numbits) - 1 - n


# The purpose of this function is to receive and process an incoming packet.
def receive_packet(connection, max_buffer_size):
    # 1. Receive the packet from the socket.
    recieved_packet = connection.recv(max_buffer_size)
    # If the connection is closed or we get an empty message, return [].
    if not recieved_packet:
        return []
    # 2. If the packet size is larger than the max_buffer_size, print a debugging message
    if len(recieved_packet) > max_buffer_size:
        print("The packets are bigger than expected")
    # 3. Decode the packet into a string.
    decoded_packet = recieved_packet.decode()
    # 3. Append the packet to recieved_by_router2.txt.
    print("recieved packet", decoded_packet)
    write_to_file("./output/recieved_by_router2.txt", decoded_packet)
    # 4. Split the packet by the delimiter.
    packet = decoded_packet.strip().split(",") if decoded_packet.strip() != "" else []
    # 5. Return the list representation of the packet.
    return packet


# The purpose of this function is to write packets/payload to file.
def write_to_file(path, packet_to_write, send_to_router=None):
    # 1. Open the output file for appending.
    out_file = open(path, "a")
    # 2. If this router is not sending, then just append the packet to the output file.
    if send_to_router is None:
        out_file.write(packet_to_write + "\n")
    # 3. Else if this router is sending, then append the intended recipient, along with the packet, to the output file.
    else:
        out_file.write(packet_to_write + " " + "to Router " + send_to_router + "\n")
    # 4. Close the output file.
    out_file.close()


# The purpose of this function is to
# (a) create a server socket,
# (b) listen on a specific port,
# (c) receive and process incoming packets,
# (d) forward them on, if needed.
def start_server():
    # 1. Create a socket.
    host = HOST
    port = PORT_R2
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created")
    # 2. Try binding the socket to the appropriate host and receiving port (based on the network topology diagram).
    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()
    # 3. Set the socket to listen.
    soc.listen(5)
    print("Socket now listening")

    # 4. Read in and store the forwarding table.
    forwarding_table = read_csv("router_2_table.csv")
    # 5. Store the default gateway port.
    default_gateway_port = find_default_gateway(forwarding_table)
    # 6. Generate a new forwarding table that includes the IP ranges for matching against destination IPS.
    forwarding_table_with_range = generate_forwarding_table_with_range(forwarding_table)

    # 7. Continuously process incoming packets.
    while True:
        # 8. Accept the connection.
        connection, address = soc.accept()
        ip, port_str = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port_str)
        # 9. Start a new thread for receiving and processing the incoming packets.
        try:
            t = Thread(
                target=processing_thread,
                args=(connection, ip, port_str, forwarding_table_with_range, default_gateway_port),
            )
            t.start()
        except:
            print("Thread did not start.")
            traceback.print_exc()


# The purpose of this function is to receive and process incoming packets.
def processing_thread(connection, ip, port, forwarding_table_with_range, default_gateway_port, max_buffer_size=5120):
    # 1. Connect to the appropriate sending ports (based on the network topology diagram).
    host = HOST
    soc_to_r3 = create_socket(host, PORT_R3)
    soc_to_r4 = create_socket(host, PORT_R4)

    # 2. Continuously process incoming packets
    while True:
        # 3. Receive the incoming packet, process it, and store its list representation
        packet = receive_packet(connection, max_buffer_size)

        # 4. If the packet is empty (Router 1 has finished sending all packets), break out of the processing loop
        if not packet:
            break

        # 5. Store the source IP, destination IP, payload, and TTL.
        sourceIP = packet[0]
        destinationIP = packet[1]
        payload = packet[2]
        ttl = int(packet[3])

        # 6. Convert the destination IP into an integer for comparison purposes.
        destinationIP_bin = ip_to_bin(destinationIP)
        destinationIP_int = int(destinationIP_bin, 2)

        # 7. Find the appropriate sending port to forward this packet to.
        send_interface = None
        is_last_hop = False
        for row in forwarding_table_with_range:
            min_ip = row[4]
            max_ip = row[5]
            if destinationIP_int >= min_ip and destinationIP_int <= max_ip:
                iface = row[3]
                if iface == "127.0.0.1":
                    is_last_hop = True
                else:
                    send_interface = iface  # PORT_R3 or PORT_R4 here
                break

        # 8. If no port is found, then set the sending port to the default port.
        if send_interface is None and not is_last_hop:
            send_interface = default_gateway_port
            if send_interface in (HOST, "127.0.0.1"):
                is_last_hop = True

        if is_last_hop:
            if ttl > 0:
                print("OUT:", payload)
                write_to_file("./output/out_router2.txt", payload)
            else:
                packet_with_zero = ",".join([sourceIP, destinationIP, payload, "0"])
                print("DISCARD:", packet_with_zero)
                write_to_file("./output/discarded_by_router2.txt", packet_with_zero)
            continue

        new_ttl = ttl - 1
        if new_ttl <= 0:
            packet_with_zero = ",".join([sourceIP, destinationIP, payload, "0"])
            print("DISCARD:", packet_with_zero)
            write_to_file("./output/discarded_by_router2.txt", packet_with_zero)
            continue

        new_packet = ",".join([sourceIP, destinationIP, payload, str(new_ttl)])

        # 9. Forward the packet or discard if no route is available.
        if send_interface == str(PORT_R3):
            print("sending packet", new_packet, "to Router 3")
            write_to_file("./output/sent_by_router2.txt", new_packet, "3")
            soc_to_r3.send(new_packet.encode())
        elif send_interface == str(PORT_R4):
            print("sending packet", new_packet, "to Router 4")
            write_to_file("./output/sent_by_router2.txt", new_packet, "4")
            soc_to_r4.send(new_packet.encode())
        else:
            print("DISCARD:", new_packet)
            write_to_file("./output/discarded_by_router2.txt", new_packet)

    # close connections used by this thread
    connection.close()
    soc_to_r3.close()
    soc_to_r4.close()


# Main Program

# 1. Start the server.
start_server()

