from scapy.all import *
from scapy.layers.l2 import Ether, ARP
import ipaddress
import warnings
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

while True:
    try:
        # Kullanıcıdan IP adresi aralığını alma
        ip_range = input("Taranacak IP aralığını girin (örneğin 192.168.116.1/24): ")

        # IP aralığının geçerliliğini kontrol etme
        ip_network = ipaddress.ip_network(ip_range, strict=False)
        break  # Geçerli bir IP aralığı ise döngüden çık

    except ValueError:
        print("Geçersiz IP aralığı! Lütfen geçerli bir IP aralığı girin.")

# Ethernet çerçevesi oluşturuluyor
eth = Ether()
eth.dst = "ff:ff:ff:ff:ff:ff"  # Yayın (broadcast) adresi

# ARP paketi oluşturuluyor
arp = ARP()
arp.pdst = str(ip_network)  # Kullanıcının girdiği IP aralığı

# Ethernet ve ARP paketleri birleştiriliyor
broadcast_pckt = eth / arp

# Paketi gönderip yanıtları bekliyoruz
ans, unans = srp(broadcast_pckt, timeout=5, verbose=False)

# Yanıtları işleme
print("#" * 50)
print("IP Adresi" + " " * 18 + "MAC Adresi")
print("-" * 50)

for snd, rcv in ans:
    print(rcv.psrc.ljust(20) + rcv.hwsrc)

# Yanıt vermeyen cihazlar
if unans:
    print("\nYanıt Vermeyen Cihazlar:")
    for pkt in unans:
        print(pkt[ARP].pdst)

print("-" * 50)
