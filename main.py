import pygame
from classes.class_server import GameServer
import utils.key_handler as key
import asyncio

async def main():
    # Initialisation de pygame
    pygame.init()
    pygame.display.set_mode((100, 100))  # Création d'une fenêtre invisible pour gérer les événements clavier

    # Création du serveur
    server = GameServer(host="127.0.0.1", port=8888)
    # Tentative de démarrer le serveur
    print(f"Attempting to start server on {server.host}:{server.port}")
    server.server = await asyncio.start_server(server.handle_client, server.host, server.port)
    print("Server started")
    addr = server.server.sockets[0].getsockname()
    print(f"Listening on {addr}")
    # Lancement du serveur dans une tâche asynchrone
    server_task = asyncio.ensure_future(server.run_server())

    # Boucle de jeu
    clock = pygame.time.Clock()
    running = True

    while running:
        # Mise à jour des événements Pygame
        pygame.event.pump()

        # Logique du serveur
        server.play()

        # Gestion de la fermeture via la touche 'close'
        if key.close():
            running = False

        clock.tick(30)  # Limiter le jeu à 30 FPS

    # Arrêt du serveur après la fin de la boucle de jeu
    await server.stop_server()

    # Annulation de la tâche du serveur
    server_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
