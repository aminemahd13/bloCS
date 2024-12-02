import socket
import json
import threading
from classes.class_entities import Entities
from classes.class_background import Background
import utils.key_handler as key
import logging


class GameClient:
    def __init__(self, host="127.0.0.1", port=55000):
        self.host = host
        self.port = port
        self.socket = None
        self.player_id = None
        self.running = False
        self.entities = Entities()
        self.background = Background()
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('GameClient')

    def connect_to_server(self, player_name, height, width):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.running = True
            self.handle_connection(player_name, height, width)
        except Exception as e:
            self.logger.error(f"Error connecting to server: {e}")
            self.running = False

    def handle_connection(self, player_name, height, width):
        # Initial connection request
        player_request = {
            "name": player_name,
            "height": height,
            "width": width
        }
        json_data = json.dumps(player_request)
        self.socket.send(json_data.encode())
        
        data = self.socket.recv(4096)
        self.player_id = json.loads(data.decode())
        
        self.entities.add_player(self.player_id , height , width , player_name)
        
        # Start receive thread
        receive_thread = threading.Thread(target=self.receive_data)
        receive_thread.daemon = True
        receive_thread.start()
        
        send_thread = threading.Thread(target=self.send_data)
        send_thread.daemon = True
        send_thread.start()

    def send_data(self):
        while self.running:
            try:
                data = {
                    "right" : key.right(),
                    "left" : key.left(),
                    "up" : key.up(),
                    "echap" : key.close(),
                    "click" : None
                }
                json_data = json.dumps(data)
                self.socket.send(json_data.encode())
            except Exception as e:
                self.logger.error(f"Error sending data: {e}")
                self.running = False

    def receive_data(self):
        while self.running:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break
                json_data = json.loads(data.decode())
                self.handle_server_message(json_data)
            except Exception as e:
                self.logger.error(f"Error receiving data: {e}")
                self.running = False
                break

    def handle_server_message(self, data):
        # Handle different types of server messages
        # Example:
        # if "player_id" in data:
        #     self.player_id = data["player_id"]
        self.entities.recup_data(data)
        if not data["Player"][self.player_id]["running"]:
            self.running = False

    def disconnect(self):
        self.running = False
        if self.socket:
            try:
                self.socket.close()
                self.logger.info("Disconnected from server")
            except Exception as e:
                self.logger.error(f"Error disconnecting: {e}")

    def update(self):
        # Game update logic here
        self.background.render(self.entities.players_dict[self.player_id])
        self.entities.render(self.player_id , self.background)