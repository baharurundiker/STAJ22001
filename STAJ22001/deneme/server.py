import socket
import subprocess

host = '127.0.0.1'
port = 3456

# Sunucu soketi oluşturuluyor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Sunucu IP adresi ve port numarasına bağlanıyor
server_socket.bind((host, port))

# Sunucu, bağlantıları dinlemeye başlıyor
server_socket.listen()

print(f"Sunucu {host}:{port} adresinde dinleniyor...")

while True:
    # İstemci bağlantısını kabul et
    conn, addr = server_socket.accept()
    print("Bağlanan istemci: " + str(addr))

    while True:
        # İstemciden gelen veriyi al
        data = conn.recv(1024).decode()
        if not data:
            print("Bağlantı kapatıldı.")
            break

        # Mesajın komut olup olmadığını belirle
        if data.startswith("CMD:"):
            # Komut çalıştırma
            command = data[4:]  # 'CMD:' öneki çıkarılıyor
            print(f"Çalıştırılacak komut: {command}")
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            response_data = result.stdout + result.stderr
        else:
            # Mesaj yazdırma
            print("Gelen Mesaj: " + data)
            response_data = "Mesaj alındı"

        # Yanıtı bytes formatına dönüştür
        if isinstance(response_data, str):
            response_data = response_data.encode()

        conn.send(response_data)

    # Bağlantıyı kapat
    conn.close()
