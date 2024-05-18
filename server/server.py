import socket
import threading
from colorama import init, Fore, Style

init()

class ServerApp:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 12345

        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(Fore.GREEN + f"Server läuft und wartet auf Verbindungen auf {self.host}:{self.port}" + Style.RESET_ALL)

        self.clients = []

        self.server_thread = threading.Thread(target=self.accept_connections)
        self.server_thread.daemon = True
        self.server_thread.start()

    def accept_connections(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(Fore.CYAN + f"Verbindung von {addr} erhalten" + Style.RESET_ALL)
            self.clients.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.daemon = True
            client_thread.start()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if data:
                    print(Fore.YELLOW + f"Empfangene Nachricht vom Client: {data}" + Style.RESET_ALL)
                else:
                    break
            except:
                break

    def send_command_to_clients(self, command):
        print(Fore.BLUE + f"Sende Befehl an alle Clients: {command}" + Style.RESET_ALL)
        for client_socket in self.clients:
            try:
                client_socket.send(command.encode())
            except:
                self.clients.remove(client_socket)

if __name__ == "__main__":
    server_app = ServerApp()
    while True:
        command = input(Fore.MAGENTA + "Geben Sie einen Befehl ein (oder 'exit' zum Beenden): " + Style.RESET_ALL)
        if command == "exit":
            break
        server_app.send_command_to_clients(command)
