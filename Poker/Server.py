import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

class Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.run = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def terminalListener(self):
        while self.run:
            cmd = input("Server command> ").strip()
            if cmd == "exit":
                print("Shutting down server...")
                self.run = False
                self.server_socket.close()
                break
            else:
                print(f"[Terminal] You typed: {cmd}")

    def handle_client(self, conn, addr):
        print(f"Started thread for {addr}")
        with conn:
            while self.run:
                if not self.serverLogic(conn, addr):
                    print(f"Client {addr} disconnected.")
                    break
        print(f"Connection closed for {addr}")

    def runServer(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        threading.Thread(target=self.terminalListener, daemon=True).start()

        while self.run:
            try:
                conn, addr = self.server_socket.accept()
                print(f"Connected by {addr}")
                # Start new thread to handle this client
                threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()
            except Exception as e:
                if self.run:
                    print(f"Error: {e}")
                break

        self.server_socket.close()
        print("Server shutdown complete.")

    def serverLogic(self, conn, addr):
        message = self.get(conn)
        if message == "":
            return False
        print(f"Received from {addr}: {message}")
        response = "Message received: " + message
        self.send(conn, response)
        return True

    def get(self, conn) -> str:
        try:
            data = conn.recv(1024)
            if not data:
                return ""
            return data.decode()
        except Exception as e:
            print(f"Get error: {e}")
            return ""

    def send(self, conn, message: str):
        try:
            conn.sendall(message.encode())
        except Exception as e:
            print(f"Send error: {e}")

if __name__ == "__main__":
    server = Server(HOST, PORT)
    server.runServer()
