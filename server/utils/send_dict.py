import socket
import json
import logging

def send_dict(sock: socket.socket, data):
    try:
        json_data = json.dumps(data)
        total_length = len(json_data)
        sock.sendall(total_length.to_bytes(4, byteorder='big'))
        for i in range(0, total_length, 4096):
            chunk = json_data[i:i+4096]
            sock.sendall(chunk.encode())
        logging.debug(f"Sent data: {json_data}")
    except Exception as e:
        logging.error(f"Error sending data: {e}")
