from ssl import SOL_SOCKET
import paramiko
import os
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath('__file__'))
HOSTKEY =  paramiko.RSAKey(filename=os.path.join(CWD,'test-key.txt'))

class Server(paramiko.ServerInterface):
    def _init_(self):
        self.event = paramiko.Event()


    def check_chan_request(self, kind, chanid):
        self.kind = kind
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if(username == 'nataraj') and (password == 'password'):
            return paramiko.AUTH_successful

if __name__ == '__main__':
    server = '192.168.1.4'
    ssh_port  = '2222'
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print ('[+] Listening for connection')
        client, addr = sock.accept()
    except Exception as e:
        print ('[+] Listening failed', str(e))
        sys.exit()
    else:
        print('[+] got a connection..', client, addr)


    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(HOSTKEY)
    server = Server
    bhSession.start_server(server=server)

    chan = bhSession.accept(20)
    if chan is 'None':
        print("No channel")
        sys.exit()
    print('[+] Authendicated')
    print(chan.recv(1024))
    chan.send('Welcome to bh_ssh')

    while True:
        try:
            command = input(" Enter the command")
            if command != 'exit':
                chan.send(command)
                r = chan.recv(8196)
                print(r.decode())
            else:
                chan.send('exit')
                print('exiting')
                bhSession.close()
                break
        except KeyboardInterrupt():
            bhSession.close()
            



