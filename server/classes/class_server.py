import socket
import json
import threading


class MultiClientServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host  # Adresse IP du serveur
        self.port = port  # Port d'écoute du serveur
        self.shared_data = {}  # Dictionnaire partagé par tous les clients
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self):
        """Démarre le serveur et attend les connexions des clients."""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  # File d'attente de 5 connexions max
        print(f"Serveur en écoute sur {self.host}:{self.port}...")

        try:
            while True:
                # Accepter une nouvelle connexion
                conn, addr = self.server_socket.accept()
                print(f"Nouvelle connexion de {addr}")

                # Lancer un thread pour gérer ce client
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                client_thread.daemon = True  # Permet de terminer les threads avec le serveur
                client_thread.start()
        except KeyboardInterrupt:
            print("\nArrêt du serveur...")
        finally:
            self.server_socket.close()

    def handle_client(self, conn, addr):
        """Gère les communications avec un client spécifique."""
        try:
            while True:
                # Recevoir des données du client
                data = conn.recv(1024).decode('utf-8')
                if not data:  # Si aucune donnée, le client a fermé la connexion
                    break

                # Traiter les données reçues
                try:
                    received_dict = json.loads(data)
                    print(f"Dictionnaire reçu de {addr} :", received_dict)

                    # Mettre à jour les données partagées
                    self.update_shared_data(received_dict)

                    # Préparer une réponse
                    response = {
                        "status": "success",
                        "message": "Dictionnaire reçu et variable mise à jour",
                        "current_shared_data": self.shared_data
                    }
                except json.JSONDecodeError:
                    print(f"Données non valides reçues de {addr}")
                    response = {"status": "error", "message": "Données non valides"}

                # Envoyer la réponse au client
                conn.send(json.dumps(response).encode('utf-8'))

        except ConnectionResetError:
            print(f"Connexion réinitialisée par {addr}")
        finally:
            # Fermer la connexion avec le client
            print(f"Connexion avec {addr} terminée")
            conn.close()

    def update_shared_data(self, received_dict):
        """
        Met à jour les données partagées avec les informations reçues des clients.
        """
        self.shared_data.update(received_dict)
    
    def send_data(self , data):
        pass