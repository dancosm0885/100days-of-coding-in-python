from http import client
from sys import stderr, stdout
from django.forms import PasswordInput
from matplotlib.pyplot import connect, getp
import paramiko

def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port = port, username=user, password=passwd)  
    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readline() + stderr.readline()

    if output:
        print('--Output--')
        for line in output:
            print(line.stripe())

if __name__ == '__main__':
    import getpass
    # User = getpass.getuser()
    user = input('Enter Username: ')
    password = getpass.getpass()

    ip  =  input('Enter server IP: ') or '192.168.1.4'
    port = input('Enter port or <CR>') or '2222'
    cmd = input('Enter commad or <CR>') or 'id'
    ssh_command(ip, port, user, password, cmd)
    
