import socket
import json
import logging
import asyncio

async def send_dict_async(writer: asyncio.StreamWriter, data):
    try:
        json_data = json.dumps(data)
        total_length = len(json_data)
        # Send the length of the data first
        writer.write(total_length.to_bytes(4, byteorder='big'))
        await writer.drain()
        # Send the actual data in chunks
        for i in range(0, total_length, 4096):
            chunk = json_data[i:i+4096]
            writer.write(chunk.encode())
            await writer.drain()
        logging.debug(f"Sent data: {json_data}")
    except Exception as e:
        logging.error(f"Error sending data asynchronously: {e}")
