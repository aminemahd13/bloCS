import asyncio
import json
from uuid import uuid4
from classes.class_entities import Entities
from classes.class_background import Background





def verif_received_data_touches(data , height , width):
    if type(data) != dict:
        return False
    if len(data) != 6:
        return False
    for test in ["right" , "left" , "up" , "echap"]:
        if test not in data:
            return False
        if type(data[test])!= bool:
            return False
    if "number" not in data:
        return False
    if type(data["number"]) != int:
        return False
    if not(1<=data["number"]<=4):
        return False
    if "click" not in data:
        return False
    if data["click"] is None:
        return True
    if type(data["click"]) != list:
        return False
    if len(data["click"]) != 3:
        return False
    for i in range(3):
        if type(data["click"][i]) != int:
            return False
    if not(0<=data["click"][0]<=width and 0<=data["click"][1]<=height and data["click"][2] in [1,3]):
        return False
    return True

def verif_player_request(data):
    if type(data) != dict:
        return False
    if len(data) != 3:
        return False
    for test in ["name" , "height_screen" , "width_screen"]:
        if test not in data:
            return False
    if type(data["name"]) != str:
        return False
    if type(data["height_screen"]) != int:
        return False
    if type(data["width_screen"]) != int:
        return False
    if not(0<=data["height_screen"]<=1080):
        return False
    if not(0<=data["width_screen"]<=1920):
        return False
    return True
    


class GameServer:
    def __init__(self, host , port):
        self.host = host
        self.port = port
        self.players = {}
        self.sent_data = {
            "Player" : {},
            "Mob" : {}
        }
        self.entities = Entities()
        self.background = Background()
        self.running = True
        self.server = None
    
    def play(self):
        self.entities.play(background = self.background)
        self.entities.move()
        self.sent_data = self.entities.crea_data()
        
    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')

        player_id = None
        try:
            # Étape 1 : Attente de la demande du joueur
            player_request = await reader.read(1024)
            player_request = json.loads(player_request.decode())
            if verif_player_request(player_request):
                # Étape 2 : Génération d'un player_id et envoi de la confirmation
                player_id = str(uuid4())
                self.players[player_id] = (writer, asyncio.get_event_loop().time())
                self.entities.add_player(player_request["name"] , player_id , player_request["height_screen"] , player_request["width_screen"])
                confirmation = {"status": "accepted", "player_id": player_id}
                writer.write(json.dumps(confirmation).encode())
                await writer.drain()

                # Étape 3 : Échange continu entre le joueur et le serveur
                while True:
                    try:
                        # Lecture des données du joueur
                        data = await asyncio.wait_for(reader.read(1024), timeout=5.0)
                        if data:
                            data_dict = json.loads(data.decode())
                            if verif_received_data_touches(data_dict , player_request["height_screen"] , player_request["width_screen"]):
                                self.entities.players_dict[player_id].dict_touches = data_dict
                            self.players[player_id] = (writer, asyncio.get_event_loop().time())
                        else:
                            break

                        # Envoi des données des mobs au joueur
                        writer.write(json.dumps(self.sent_data).encode())
                        await writer.drain()
                    except asyncio.TimeoutError:
                        break
            else:
                confirmation = {"status": "refused", "player_id": None}
                writer.write(json.dumps(confirmation).encode())
                await writer.drain()
        except Exception:
            pass
        finally:
            # Étape 4 : Gestion de la déconnexion
            if player_id and player_id in self.players:
                del self.players[player_id]
            writer.close()
            await writer.wait_closed()
            if player_id and player_id in self.entities.players_dict:
                self.entities.remove_player(player_id)

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

