import socket
import json
import logging

# Ensure that logs are also printed to the terminal by adding a StreamHandler.
logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])

def recv_dict(sock: socket.socket):
    try:
        total_length = int.from_bytes(sock.recv(4), byteorder='big')
        data = bytearray()
        while len(data) < total_length:
            packet = sock.recv(4096)
            if not packet:
                logging.debug("No more packets received.")
                return None
            data.extend(packet)
        json_data = data.decode()
        logging.debug(f"Received data: {json_data}")
        return json.loads(json_data)
    except Exception as e:
        logging.error(f"Error receiving data: {e}")
        return None