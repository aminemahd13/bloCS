import asyncio
import logging
from typing import Optional
from dataclasses import dataclass

@dataclass
class ServerConfig:
    host: str = "127.0.0.1"
    port: int = 55000
    max_clients: int = 10

class GameServer:
    def __init__(self, config: ServerConfig = ServerConfig()):
        self.config = config
        self.server: Optional[asyncio.Server] = None
        self.clients = set()
        self.running = False
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('GameServer')

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')
        self.logger.info(f"New connection from {addr}")
        
        if len(self.clients) >= self.config.max_clients:
            self.logger.warning(f"Max clients reached, rejecting {addr}")
            writer.close()
            await writer.wait_closed()
            return

        self.clients.add(writer)
        try:
            while self.running:
                data = await reader.read(1024)
                if not data:
                    break
                self.logger.debug(f"Received data from {addr}: {data}")
                # Process data here
                # await self.broadcast(data, writer)
        except Exception as e:
            self.logger.error(f"Error handling client {addr}: {e}")
        finally:
            self.clients.remove(writer)
            writer.close()
            await writer.wait_closed()
            self.logger.info(f"Connection closed for {addr}")

    async def broadcast(self, data: bytes, sender: asyncio.StreamWriter):
        for client in self.clients:
            if client != sender:
                try:
                    client.write(data)
                    await client.drain()
                except Exception as e:
                    self.logger.error(f"Error broadcasting to client: {e}")

    async def start(self):
        self.running = True
        try:
            self.server = await asyncio.start_server(
                self.handle_client,
                self.config.host,
                self.config.port
            )
            addr = self.server.sockets[0].getsockname()
            self.logger.info(f"Server started on {addr}")
            await self.server.serve_forever()
        except Exception as e:
            self.logger.error(f"Server error: {e}")
            self.running = False

    async def stop(self):
        self.running = False
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.logger.info("Server stopped")

def setup_file_logging():
    file_handler = logging.FileHandler('server.log')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)
    
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    logging.getLogger().addHandler(stream_handler)

async def main():
    setup_file_logging()
    config = ServerConfig()
    server = GameServer(config)
    
    try:
        await server.start()
    except KeyboardInterrupt:
        await server.stop()

if __name__ == "__main__":
    asyncio.run(main())