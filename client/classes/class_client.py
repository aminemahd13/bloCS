import socket
import json


class MultiClient:
    def __init__(self, host='127.0.0.1', port=12345):
        """
        Initialise le client avec les paramètres du serveur.
        """
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        """
        Établit une connexion au serveur.
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print(f"Connecté au serveur {self.host}:{self.port}")

    def send_dict(self, data_to_send):
        """
        Envoie un dictionnaire au serveur et affiche la réponse.
        """
        if not self.client_socket:
            raise ConnectionError("Le client n'est pas connecté au serveur.")
        
        try:
            # Envoi du dictionnaire sous forme de chaîne JSON
            self.client_socket.send(json.dumps(data_to_send).encode('utf-8'))
            
            # Réception de la réponse
            response = self.client_socket.recv(1024).decode('utf-8')
            print("Réponse du serveur :", json.loads(response))
        except Exception as e:
            print("Erreur lors de l'envoi ou de la réception :", e)

    def close(self):
        """
        Ferme la connexion avec le serveur.
        """
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
            print("Connexion au serveur fermée.")
    
    def received_data(self):
        pass
