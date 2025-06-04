import socket
import threading
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Core.Core import Core

HOST = '127.0.0.1'
PORT = 65432

class Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.run = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.players = {}  # player_id -> player dict
        self.lock = threading.Lock()
        self.game_started = False

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
            player_info = self.get(conn)
            if player_info == "":
                print(f"Client {addr} disconnected before sending player info.")
                return

            try:
                player_id_str, player_nick, player_points_str = player_info.split(';')
                player_id = int(player_id_str)
                player_points = int(player_points_str)

                with self.lock:
                    if player_id in self.players:
                        # Reconnecting player
                        print(f"Player {player_id} reconnected from {addr}")
                        self.players[player_id]["addr"] = addr
                        self.players[player_id]["conn"] = conn
                        self.players[player_id]["connected"] = True
                    else:
                        # New player
                        self.players[player_id] = {
                            "id": player_id,
                            "nick": player_nick,
                            "points": player_points,
                            "addr": addr,
                            "conn": conn,
                            "connected": True,
                            "ready": False
                        }
                        print(f"Registered new player {player_nick} (ID: {player_id}) from {addr}")
                self.send(conn, "Player registered successfully.")
            except Exception as e:
                print(f"Failed to parse player info from {addr}: {e}")
                self.send(conn, "Invalid player info format. Closing connection.")
                return

            while self.run:
                if not self.serverLogic(conn, player_id):
                    print(f"Client {addr} (player {player_id}) disconnected.")
                    break

        # Mark player as disconnected
        with self.lock:
            if player_id in self.players:
                self.players[player_id]["connected"] = False
                self.players[player_id]["conn"] = None
                self.players[player_id]["addr"] = None
                print(f"Marked player {player_id} as disconnected.")

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
                threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()
            except Exception as e:
                if self.run:
                    print(f"Error: {e}")
                break

        self.server_socket.close()
        print("Server shutdown complete.")

    def serverLogic(self, conn, player_id):
        message = self.get(conn)
        if message == "":
            return False

        with self.lock:
            player = self.players.get(player_id)

        if(message == "ready"):
            player['ready'] = True
            print(f"Player {player['id']} is ready")
            self.send(conn, "Marked as Ready")
        elif(message == "unready"):
            player['ready'] = False
            print(f"Player {player['id']} is unready")
            self.send(conn, "Marked as Unready")
        else: self.send(conn, "No allowed command")

        
        if len(self.players) >= 2 and not self.game_started:
            all_ready = True
            active_players = [p for p in self.players.values() if p['connected']]
            
            # Check if all connected players are ready
            for p in active_players:
                if not p['ready']:
                    all_ready = False
                    break

            if all_ready and len(active_players) >= 2:
                self.game_started = True
                self.game_load = True

        if self.game_started:
            if self.game_load:
                self.game_load = False
                print("Game starting...")
                players = [p["nick"] for p in active_players]
                core = Core(players, 3)
                print("Game Started")
                

        return True

    def playGame(self):
        pass

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
            if conn:
                conn.sendall(message.encode())
        except Exception as e:
            print(f"Send error: {e}")

if __name__ == "__main__":
    server = Server(HOST, PORT)
    server.runServer()
