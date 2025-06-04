import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 65432

class Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.run = True
        self.conn = None
        self.addr = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def runServer(self):
        self.server_socket.settimeout(1.0)  # Check every 1 second
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        threading.Thread(target=self.terminalListener, daemon=True).start()

        while self.run:
            try:
                conn, addr = self.server_socket.accept()
                self.conn, self.addr = conn, addr
                print(f"Connected by {addr}")
                conn.settimeout(1.0)  # Also add timeout for recv
                with conn:
                    while self.run:
                        try:
                            data = conn.recv(1024)
                            if not data:
                                print(f"Client {addr} disconnected.")
                                break
                            message = data.decode()
                            print("Received from client:", message)
                            response = self.serverLogic(message)
                            conn.sendall(response.encode())
                        except socket.timeout:
                            continue
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error: {e}")
                break

        self.server_socket.close()
        print("Server shutdown complete.")


    def terminalListener(self):
        """Continuously listen for terminal input without stopping the server."""
        while self.run:
            user_input = input("Server command> ").strip()
            if user_input == "exit":
                print("Shutting down server...")
                self.run = False
                break
            else:
                print(f"[Terminal] You typed: {user_input}")
                # You could handle other commands here too

    def serverLogic(self, message: str) -> str:
        return "Message received: " + message

    def send(self, message: str):
        if self.conn:
            self.conn.sendall(message.encode())

    def get(self) -> str:
        if self.conn:
            data = self.conn.recv(1024)
            return data.decode()
        return ""

# Run server
if __name__ == "__main__":
    server = Server(HOST, PORT)
    server.runServer()
