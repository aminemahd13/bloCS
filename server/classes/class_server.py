import asyncio
import json
from uuid import uuid4
from classes.class_entities import Entities
from classes.class_background import Background
from utils.verif import verif_data_received, verif_client_request
from utils.send_dict import send_dict_async
from utils.recv_dict import recv_dict_async
import logging

class GameServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.players = {}
        self.sent_data = {
            "Player": {},
            "Mob": {}
        }
        self.entities = Entities()
        self.background = Background()
        self.running = True
        self.server = None
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.DEBUG,  # Changed to DEBUG for more detailed logs
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('GameServer')
        
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)
        logging.getLogger().addHandler(stream_handler)

    def play(self):
        self.entities.play(background=self.background)
        self.entities.move()
        self.sent_data = self.entities.crea_data()

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')
        self.logger.info(f"New connection from {addr}")

        player_id = None
        try:
            player_request = await recv_dict_async(reader)
            self.logger.debug(f"Received player request from {addr}: {player_request}")
            if player_request and verif_client_request(player_request):
                self.logger.info(f"Player request verified for {addr}")
                # Setup player
                player_id = str(uuid4())
                self.players[player_id] = (writer, asyncio.get_event_loop().time())
                self.entities.add_player(
                    player_request["name"],
                    player_id,
                    player_request["height_screen"],
                    player_request["width_screen"]
                )

                # Send confirmation
                confirmation = {"status": "accepted", "player_id": player_id}
                self.logger.debug(f"Sending confirmation to {addr}: {confirmation}")
                await send_dict_async(writer, confirmation)
                self.logger.info(f"Sent confirmation to {addr}: {confirmation}")

                # Send initial game state
                self.sent_data["Player"][player_id] = self.entities.players_dict[player_id].crea_data()
                initial_game_state = {
                    "map": self.background.dict_block,
                    "data": self.sent_data
                }
                self.logger.debug(f"Sending initial game state to {addr}: {initial_game_state}")
                await send_dict_async(writer, initial_game_state)
                self.logger.info(f"Sent initial game state to {addr}")

                # Main communication loop
                while True:
                    try:
                        data_dict = await asyncio.wait_for(recv_dict_async(reader), timeout=10.0)
                        self.logger.debug(f"Received data from {addr}: {data_dict}")
                        if not data_dict:
                            self.logger.info(f"Client disconnected: {addr}")
                            break
                        if verif_data_received(data_dict):
                            player = self.entities.players_dict[player_id]
                            player.dict_touches = data_dict
                            if "position" in data_dict:
                                player.x = data_dict["position"]["x"]
                                player.y = data_dict["position"]["y"]
                        
                        # Update and send game state
                        self.logger.debug("Updating game state")
                        self.play()  # Update game state
                        self.logger.debug("Game state updated")
                        game_state = {
                            "map": self.background.dict_block,
                            "Player": {pid: p.crea_data() for pid, p in self.entities.players_dict.items()},
                            "Mob": {mid: m.crea_data() for mid, m in self.entities.mobs_dict.items()}
                        }
                        for pid, (w, _) in self.players.items():
                            try:
                                await send_dict_async(w, game_state)
                            except Exception as e:
                                self.logger.error(f"Error sending game state to player {pid}: {e}")
                        await asyncio.sleep(1 / self.entities.fps)
                    except asyncio.TimeoutError:
                        self.logger.info(f"Timeout waiting for data from {addr}. Closing connection.")
                        break
                    except Exception as e:
                        self.logger.error(f"Error in update_and_broadcast: {e}")
            else:
                self.logger.warning(f"Player request verification failed for {addr}: {player_request}")
                confirmation = {"status": "refused", "player_id": None}
                self.logger.debug(f"Sending refusal to {addr}: {confirmation}")
                await send_dict_async(writer, confirmation)
                self.logger.info(f"Sent refusal to {addr}: {confirmation}")
        except Exception as e:
            self.logger.error(f"Error handling client {addr}: {e}")
        finally:
            # Cleanup
            if player_id and player_id in self.players:
                del self.players[player_id]
            writer.close()
            await writer.wait_closed()
            if player_id and player_id in self.entities.players_dict:
                self.entities.remove_player(player_id)
            self.logger.info(f"Connection closed for {addr}")

    async def update_and_broadcast(self):
        while self.running:
            try:
                self.logger.debug("Playing game to update state")
                self.play()
                self.logger.debug("Game state played")

                game_state = {
                    "map": self.background.dict_block,
                    "Player": {pid: p.crea_data() for pid, p in self.entities.players_dict.items()},
                    "Mob": {mid: m.crea_data() for mid, m in self.entities.mobs_dict.items()}
                }
                self.logger.debug(f"Broadcasting game state: {game_state}")
                for player_id, (writer, _) in self.players.items():
                    try:
                        await send_dict_async(writer, game_state)
                        self.logger.debug(f"Sent game state to player {player_id}")
                    except Exception as e:
                        self.logger.error(f"Error sending game state to player {player_id}: {e}")
                await asyncio.sleep(1 / self.entities.fps)
            except Exception as e:
                self.logger.error(f"Error in update_and_broadcast: {e}")

