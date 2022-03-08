import os
import socket


# host ot listen on
HOST = '192.168.141.10'

def main():
    # create socket  and bin to public interface
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind(('Host',0))
    # include the IP in the header
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL,1)

    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    #read one packet
    print(sniffer.recv(65565))

    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


if __name__ == '__main__'
    main()

