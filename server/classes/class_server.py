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
            self.logger.debug(f"Received player request: {player_request}")
            
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
                await send_dict_async(writer, confirmation)
                self.logger.info(f"Sent confirmation to {addr}: {confirmation}")

                # Send initial game state
                self.sent_data["Player"][player_id] = self.entities.players_dict[player_id].crea_data()
                initial_game_state = {
                    "map": self.background.dict_block,
                    "data": self.sent_data
                }
                await send_dict_async(writer, initial_game_state)
                self.logger.info(f"Sent initial game state to {addr}")

                # Main communication loop
                while True:
                    try:
                        # Handle player input with a timeout
                        data_dict = await asyncio.wait_for(recv_dict_async(reader), timeout=10.0)
                        if not data_dict:
                            self.logger.info(f"No data received. Closing connection for {addr}")
                            break

                        self.logger.debug(f"Received data from {addr}: {data_dict}")
                        if verif_data_received(data_dict, player_request["height_screen"], player_request["width_screen"]):
                            self.entities.players_dict[player_id].dict_touches = data_dict
                        self.players[player_id] = (writer, asyncio.get_event_loop().time())

                        # Update and send game state
                        self.play()  # Update game state
                        await send_dict_async(writer, {"data": self.sent_data})
                        self.logger.debug(f"Sent game state to {addr}")
                    except asyncio.TimeoutError:
                        self.logger.info(f"Timeout waiting for data from {addr}. Closing connection.")
                        break
            else:
                self.logger.warning(f"Player request verification failed for {addr}: {player_request}")
                confirmation = {"status": "refused", "player_id": None}
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

    async def run_server(self):
        try:
            # Démarrage de l'écoute du serveur
            async with self.server:
                await self.server.serve_forever()
        except Exception as e:
            print(f"Error while starting the server: {e}")

    async def stop_server(self):
        """Arrête proprement le serveur."""
        print("Stopping server...")
        self.running = False  # Arrête la gestion des joueurs
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        # Déconnecte tous les joueurs connectés
        for player_id, (writer, _) in list(self.players.items()):
            print(f"Disconnecting player {player_id}...")
            writer.close()
            await writer.wait_closed()
        self.players.clear()
        print("Server stopped.")

