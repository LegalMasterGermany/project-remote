import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'  
port = 12345

client_socket.connect((host, port))

message = "Hallo vom Client!"
client_socket.send(message.encode())

data = client_socket.recv(1024).decode()
print(f"Antwort vom Server: {data}")

client_socket.close()
