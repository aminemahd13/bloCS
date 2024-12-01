import asyncio
import json
from classes.class_entities import Entities
from classes.class_background import Background
import utils.key_handler as key


class GameClient:
    def __init__(self, host , port):
        self.host = host
        self.port = port
        self.writer = None
        self.player_id = None
        self.running = False
        self.entities = Entities()
        self.background = Background()

    async def connect_to_server(self , player_name , height , width):
        try:
            reader, self.writer = await asyncio.open_connection(self.host, self.port)
            await self.handle_connection(reader, self.writer , player_name , height , width)
        except Exception as e:
            print(f"Error connecting to server: {e}")

    async def handle_connection(self, reader, writer , player_name , height , width):
        # Étape 1 : Envoi de la demande de connexion
        player_request = {
            "name" : player_name,
            "height_screen" : height,
            "width_screen" : width
        }
        writer.write(json.dumps(player_request).encode())
        await writer.drain()

        # Étape 2 : Réception de la confirmation et du player_id
        response = await reader.read(1024)
        response = json.loads(response.decode())
        if response["status"] == "accepted":
            self.running = True
            self.player_id = response["player_id"]
            self.entities.add_player(self.player_id , height , width , player_name)
            self.entities.players_dict[self.player_id].initialize()
            print(f"Connected with player_id: {self.player_id}")

            # Étape 3 : Échange continu des données
            try:
                while self.running:
                    # Envoi des données du joueur
                    data_dict = {
                        "right" : key.right(),
                        "left" : key.left(),
                        "up" : key.up(),
                        "echap" : key.close(),
                        "number" : key.get_number(),
                        "click" : None
                    }
                    writer.write(json.dumps(data_dict).encode())
                    await writer.drain()

                    # Lecture des données des mobs
                    mobs_data = await reader.read(1024)
                    mobs_data = json.loads(mobs_data.decode())
                    print(f"Received mobs data: {mobs_data}")
                    self.entities.recup_data(mobs_data)

                    # Pause avant le prochain envoi
                    await asyncio.sleep(0.01)
            except Exception as e:
                self.running = False
                print(f"Error during game loop: {e}")
            finally:
                # Étape 4 : Déconnexion
                self.running = False
            
        else:
            # Étape 4 : Déconnexion
            self.running = False

    def render(self):
        self.entities.render(player_id = self.player_id , background = self.background)
    
    async def close(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
        print("Disconnected from server.")
        self.entities.players_dict[self.player_id].close()

