import socket
import json
import threading
from classes.class_entities import Entities
from classes.class_background import Background
from utils.verif import verif_data_received, verif_request_received
import utils.key_handler as key
import logging
from utils.send_dict import send_dict
from utils.recv_dict import recv_dict

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
        self.logger.debug("Initialized GameClient")

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('GameClient')

    def connect_to_server(self, player_name, height, width):
        try:
            self.logger.debug(f"Attempting to connect to {self.host}:{self.port}")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.logger.info(f"Connected to server at {self.host}:{self.port}")
            self.running = True
            self.handle_connection(player_name, height, width)
        except Exception as e:
            self.logger.error(f"Error connecting to server: {e}")
            self.running = False

    def handle_connection(self, player_name, height, width):
        # Initial connection request
        player_request = {
            "name": player_name,
            "height_screen": height,      # Changed from "height" to "height_screen"
            "width_screen": width         # Changed from "width" to "width_screen"
        }
        self.logger.debug(f"Sending player request: {player_request}")
        send_dict(self.socket, player_request)
        
        data_dict = recv_dict(self.socket)
        self.logger.debug(f"Received response: {data_dict}")
        if verif_request_received(data_dict):
            if data_dict["player_id"] is not None:
                self.player_id = data_dict["player_id"]
                self.logger.info(f"Assigned player ID: {self.player_id}")
                self.entities.add_player(self.player_id, height, width, player_name)
                
                # Receive game map
                game_map = recv_dict(self.socket)
                self.background.update_map(game_map)
                self.logger.debug(f"Received game map: {game_map}")
                
                # Start receive thread
                receive_thread = threading.Thread(target=self.receive_data)
                receive_thread.daemon = True
                receive_thread.start()
                self.logger.debug("Started receive thread")
                
                send_thread = threading.Thread(target=self.send_data)
                send_thread.daemon = True
                send_thread.start()
                self.logger.debug("Started send thread")
                
                self.running = True
            else:
                self.logger.warning("Player ID is None, connection refused by server")
                self.running = False
        else:
            self.logger.warning("Failed to verify server response")
            self.running = False

    def send_data(self):
        while self.running:
            try:
                # Get the player's current position
                player = self.entities.players_dict.get(self.player_id)
                if player:
                    position = {"x": player.x, "y": player.y}
                else:
                    position = {"x": 0, "y": 0}
                
                data = {
                    "right": key.right(),
                    "left": key.left(),
                    "up": key.up(),
                    "echap": key.close(),
                    "click": None,
                    "position": position  # Include position
                }
                json_data = json.dumps(data)
                self.socket.send(json_data.encode())
                self.logger.debug(f"Sending data: {data}")
                send_dict(self.socket, data)
                self.logger.debug("Data sent successfully")
                self.logger.info(f"Sent data: {json_data}")
            except Exception as e:
                self.logger.error(f"Error sending data: {e}")
                self.running = False

    def receive_data(self):
        while self.running:
            try:
                data_dict = recv_dict(self.socket)
                self.logger.debug(f"Received data: {data_dict}")
                if not data_dict:
                    self.logger.info("No data received. Server may have closed the connection.")
                    break
                self.logger.info(f"Received data: {data_dict}")
                if "map" in data_dict:
                    self.background.update_map(data_dict["map"])
                    self.logger.debug("Updated game map from server")
                else:
                    self.handle_server_message(data_dict)
            except Exception as e:
                self.logger.error(f"Error receiving data: {e}")
                self.running = False
                break

    def handle_server_message(self, data):
        if verif_data_received(data):
            self.entities.recup_data(data)
            self.logger.debug(f"Updated entities with data: {data}")
            if not data["Player"][self.player_id]["running"]:
                self.logger.info("Server indicated the game is no longer running")
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
        if self.player_id in self.entities.players_dict:
            self.logger.debug("Updating background and entities")
            self.background.render(self.entities.players_dict[self.player_id])
            self.entities.render(self.player_id, self.background)