import socket
import json
import logging

def recv_dict(sock: socket.socket):
    try:
        total_length = int.from_bytes(sock.recv(4), byteorder='big')
        data = bytearray()
        while len(data) < total_length:
            packet = sock.recv(4096)
            if not packet:
                return None
            data.extend(packet)
        json_data = data.decode()
        logging.debug(f"Received data: {json_data}")
        return json.loads(json_data)
    except Exception as e:
        logging.error(f"Error receiving data: {e}")
        return None