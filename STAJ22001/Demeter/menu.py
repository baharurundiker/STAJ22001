import subprocess

# Renk kodları
GREEN = "\033[92m"
RESET = "\033[0m"

def banner():
    # Banner için renk değişikliği yok, orijinal kalıyor
    subprocess.run("figlet -f mono9 -c 'Demeter' | lolcat", shell=True)

def run_tool(tool_name):
    try:
        subprocess.run(["python3", tool_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"{GREEN}Aracı çalıştırırken bir hata oluştu: {e}{RESET}")

def show_menu():
    """Kullanıcıya menü seçeneklerini gösterir ve seçim yapmasını sağlar."""
    while True:
        print(GREEN + "\n" + "-"*40)
        print("         Araçlar Menüsü".center(40))
        print("-"*40)
        print("1. Port Tarayıcı")
        print("2. ARP Zehirleyici")
        print("3. DHCP Açlık Saldırısı")
        print("4. MAC Adresi Değiştiricisi")
        print("5. Dosya Şifreleme/Çözme")
        print("6. Host Keşfi")
        print("7. Çıkış")
        print("-"*40 + RESET)

        choice = input(GREEN + "Bir seçenek girin (1-7): " + RESET)

        if choice == '1':
            run_tool("port_scan.py")
        elif choice == '2':
            run_tool("arp_poisoning.py")
        elif choice == '3':
            run_tool("dhcp_exhaustion.py")
        elif choice == '4':
            run_tool("mc_changer.py")
        elif choice == '5':
            run_tool("encryption.py")
        elif choice == '6':
            run_tool("host_discovery_arp.py")
        elif choice == '7':
            print(GREEN + "Çıkış yapılıyor..." + RESET)
            break
        else:
            print(GREEN + "Geçersiz seçenek. Lütfen tekrar deneyin." + RESET)

if __name__ == "__main__":
    banner()
    show_menu()
