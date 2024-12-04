import socket
import json
import logging
import asyncio

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

async def recv_dict_async(reader: asyncio.StreamReader):
    try:
        # Receive the length of the incoming data first
        raw_length = await reader.readexactly(4)
        total_length = int.from_bytes(raw_length, byteorder='big')
        data = bytearray()
        while len(data) < total_length:
            packet = await reader.read(min(4096, total_length - len(data)))
            if not packet:
                return None
            data.extend(packet)
        json_data = data.decode()
        logging.debug(f"Received data: {json_data}")
        return json.loads(json_data)
    except asyncio.IncompleteReadError:
        logging.error("Incomplete read error while receiving data.")
        return None
    except Exception as e:
        logging.error(f"Error receiving data asynchronously: {e}")
        return None
