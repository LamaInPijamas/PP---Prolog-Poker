import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

class Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.run = True

    def runClient(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            print("Connected to server.")
            while self.run:
                message = input("Enter message to send to server (or 'exit' to quit): ")
                if message.lower() == 'exit':
                    print("Closing connection.")
                    self.run = False
                    break
                s.sendall(message.encode())
                data = s.recv(1024)
                print("Received from server:", data.decode())

    def clientLogic(self):
      pass

    def get(self) -> str:
        # Placeholder for advanced use
        pass

    def send(self):
        # Placeholder for advanced use
        pass

client = Client(HOST, PORT)
client.runClient()
