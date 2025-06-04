import socket

HOST = '127.0.0.1'
PORT = 65432

PLAYER_ID = int(input("Player id: "))
PLAYER_NICK = input("Player nick: ")
PLAYER_POINTS = int(input("Player Points: "))

class Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.run = True

    def runClient(self, id : int, nick : str, points : int):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            self.server = server
            self.server.connect((self.host, self.port))
            print("Connected to server.")
            self.send(str(id)+";"+nick+";"+str(points))
            while self.run:
                self.clientLogic()

    def clientLogic(self):
      message = input("Enter message to send to server (or 'exit' to quit): ")
      if message.lower() == 'exit':
          print("Closing connection.")
          self.run = False
      else:
        self.send(message)
        print("Server respond: ", self.get())

    def get(self) -> str:
        data = self.server.recv(1024)
        response = data.decode()
        print("Received from server:", response)
        return response

    def send(self, message):
        self.server.sendall(message.encode())

client = Client(HOST, PORT)
client.runClient(PLAYER_ID, PLAYER_NICK, PLAYER_POINTS)
