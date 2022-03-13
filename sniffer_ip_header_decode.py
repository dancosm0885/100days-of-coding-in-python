import socket
import ipaddress
import sys
import struct
import os


class IP:

    def __init__(self, buff=None):
        header = struct.unpack('<BBBHHHBBH4s4s', buff)
        self.ver = header[0] >> 4
        self.ihl = header[0] & 0xF
        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_num = [6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]

        # human readable IP addresses
        self.src_ipaddress = ipaddress.ip_address(self.src)
        self.dst_ipaddress = ipaddress.ip_address(self.dst)

        # map protocol to assign to their constant number
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}

        try:
            self.protocol = self.protocol_map[int(self.protocol_num)]
        except Exception as e:
            print("%s No protocol for %s" % (e, self.protocol_num))
        self.protocol = str(self.protocol_num)


    def sniff(host):
        if os.name == 'nt':
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP

        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        sniffer.bind((host, 0))

        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

            try:
                while True:
                    # read a packet
                    raw_buff = sniffer.recvfrom(65535)[0]
                    # create an ip header to  read  first 20  bytes
                    ip_header = IP(raw_buff[0:20])
                    # print the detected ip address to host
                    print("protocol: %s %s -> %s" % (
                    ip_header.protocol, ip_header.src_ipaddress, ip_header.dst_ipaddress))
            except KeyboardInterrupt:
                # if  windows off the promiscuous mode
                if os.name == 'nt':
                    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
                sys.exit()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = '192.168.10.141'
    sniff(host)
