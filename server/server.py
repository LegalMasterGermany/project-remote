import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'  
port = 12345

server_socket.bind((host, port))

server_socket.listen(5)
print(f"Server läuft und wartet auf Verbindungen auf {host}:{port}")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Verbindung von {addr} erhalten")

    data = client_socket.recv(1024).decode()
    print(f"Empfangene Nachricht vom Client: {data}")

    response = "Hallo vom Server!"
    client_socket.send(response.encode())

    client_socket.close()