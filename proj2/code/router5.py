import socket
import sys
import traceback
from threading import Thread
from pathlib import Path

from .config import HOST, PORT_R5, INPUT_DIR

# ---------- Helpers ----------

def read_csv(filename):
    table_path = INPUT_DIR / filename if not Path(filename).is_absolute() else Path(filename)
    table_file = open(table_path, "r")
    table = table_file.readlines()
    table_list = []
    for line in table:
        line = line.strip()
        if line == "":
            continue
        parts = [p.strip() for p in line.split(",")]
        table_list.append(parts)
    table_file.close()
    return table_list


def find_default_gateway(table):
    for row in table:
        if row[0] == "0.0.0.0":
            return row[3]
    return None


def ip_to_bin(ip):
    ip_octets = ip.split(".")
    ip_bin_string = ""
    for octet in ip_octets:
        int_octet = int(octet)
        bin_octet_string = bin(int_octet)[2:]
        while len(bin_octet_string) < 8:
            bin_octet_string = "0" + bin_octet_string
        ip_bin_string += bin_octet_string
    ip_int = int(ip_bin_string, 2)
    return bin(ip_int)


def bit_not(n, numbits=32):
    return (1 << numbits) - 1 - n


def find_ip_range(network_dst, netmask):
    network_int = int(network_dst, 2)
    netmask_int = int(netmask, 2)
    bitwise_and = network_int & netmask_int
    compliment = bit_not(netmask_int)
    min_ip = bitwise_and
    max_ip = min_ip + compliment
    return [min_ip, max_ip]


def generate_forwarding_table_with_range(table):
    new_table = []
    for row in table:
        if row[0] != "0.0.0.0":
            network_dst_bin = ip_to_bin(row[0])
            netmask_bin = ip_to_bin(row[1])
            ip_range = find_ip_range(network_dst_bin, netmask_bin)
            new_row = [row[0], row[1], row[2], row[3], ip_range[0], ip_range[1]]
            new_table.append(new_row)
    return new_table


def write_to_file(path, packet_to_write, send_to_router=None):
    out_file = open(path, "a")
    if send_to_router is None:
        out_file.write(packet_to_write + "\n")
    else:
        out_file.write(packet_to_write + " " + "to Router " + send_to_router + "\n")
    out_file.close()


def receive_packet(connection, max_buffer_size):
    recieved_packet = connection.recv(max_buffer_size)
    if not recieved_packet:
        return []
    if len(recieved_packet) > max_buffer_size:
        print("The packets are bigger than expected")
    decoded_packet = recieved_packet.decode()
    print("Router 5 recieved packet", decoded_packet)
    write_to_file("./output/recieved_by_router5.txt", decoded_packet)
    packet = decoded_packet.strip().split(",") if decoded_packet.strip() != "" else []
    return packet


# ---------- Server / main logic ----------

def start_server():
    host = HOST
    port = PORT_R5
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Router 5 socket created")
    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()
    soc.listen(5)
    print("Router 5 listening on", port)

    forwarding_table = read_csv("router_5_table.csv")
    default_gateway_port = find_default_gateway(forwarding_table)
    forwarding_table_with_range = generate_forwarding_table_with_range(forwarding_table)

    while True:
        connection, address = soc.accept()
        ip, port_str = str(address[0]), str(address[1])
        print("Router 5 connected with " + ip + ":" + port_str)
        try:
            t = Thread(
                target=processing_thread,
                args=(connection, ip, port_str,
                      forwarding_table_with_range, default_gateway_port),
            )
            t.start()
        except:
            print("Thread did not start.")
            traceback.print_exc()


def processing_thread(connection, ip, port,
                      forwarding_table_with_range, default_gateway_port,
                      max_buffer_size=5120):

    while True:
        packet = receive_packet(connection, max_buffer_size)
        if not packet:
            break

        sourceIP = packet[0]
        destinationIP = packet[1]
        payload = packet[2]
        ttl = int(packet[3])

        destinationIP_bin = ip_to_bin(destinationIP)
        destinationIP_int = int(destinationIP_bin, 2)

        send_interface = None
        is_last_hop = False
        for row in forwarding_table_with_range:
            min_ip = row[4]
            max_ip = row[5]
            if destinationIP_int >= min_ip and destinationIP_int <= max_ip:
                iface = row[3]
                if iface == HOST:
                    is_last_hop = True
                else:
                    send_interface = iface  # PORT_R4 for link to Router 4
                break

        if send_interface is None and not is_last_hop:
            send_interface = default_gateway_port  # here default is local (HOST)
            if send_interface == HOST:
                is_last_hop = True

        if is_last_hop:
            if ttl > 0:
                print("Router 5 OUT:", payload)
                write_to_file("./output/out_router5.txt", payload)
            else:
                packet_with_zero = ",".join([sourceIP, destinationIP, payload, "0"])
                print("Router 5 DISCARD:", packet_with_zero)
                write_to_file("./output/discarded_by_router5.txt", packet_with_zero)
            continue

        new_ttl = ttl - 1
        if new_ttl <= 0:
            packet_with_zero = ",".join([sourceIP, destinationIP, payload, "0"])
            print("Router 5 DISCARD:", packet_with_zero)
            write_to_file("./output/discarded_by_router5.txt", packet_with_zero)
            continue

        new_packet = ",".join([sourceIP, destinationIP, payload, str(new_ttl)])

        if send_interface in ("e", str(PORT_R5)):
            print("Router 5 forwarding", new_packet, "to Router 4")
            write_to_file("./output/sent_by_router5.txt", new_packet, "4")
            connection.send(new_packet.encode())   # only neighbor is PORT_R4
        else:
            print("Router 5 DISCARD:", new_packet)
            write_to_file("./output/discarded_by_router5.txt", new_packet)

    connection.close()


if __name__ == "__main__":
    start_server()

