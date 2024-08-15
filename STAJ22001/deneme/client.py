import socket

host = '127.0.0.1'
port = 3456

# İstemci soketi oluşturuluyor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Sunucuya bağlan
client_socket.connect((host, port))

while True:
    # Kullanıcıdan veri al
    message = input("Mesaj veya Komut Girin (komutlar için 'CMD:' öneki kullanın, çıkmak için 'quit' yazın): ")
    if message.lower().strip() == "quit":
        break

    # Veriyi sunucuya gönder
    client_socket.send(message.encode())

    # Sunucudan yanıt al
    data = client_socket.recv(1024).decode()
    print("Sunucudan Yanıt: " + str(data))

# Bağlantıyı kapat
client_socket.close()
