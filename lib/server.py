from .imports import websockets
from .imports import asyncio
from .imports import json
from .imports import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_SECRET_KEY

from .channel import Channel

class Server:
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT, secret_key=DEFAULT_SECRET_KEY):
        self.host = host
        self.port = port
        self.secret_key = secret_key

        self.channels = []

    async def handle_client(self, websocket):
        while True:
            try:
                msg = json.loads(await websocket.recv())
            except:
                for channel in self.channels:
                    channel.remove_client(websocket)
                return
            if msg["server_response"] == True:
                channel = self.find_channel(msg["channel_name"])
                if not channel:
                    channel = Channel(msg["channel_name"])
                    self.channels.append(channel)
                if msg["type"] == "connect":
                    channel.add_client(websocket)
                elif msg["type"] == "quit":
                    channel.remove_client(websocket)
            else:
                pass


    async def wait_connection(self):
        async with websockets.serve(self.handle_client, "", 8080):
            await asyncio.Future()

    def run(self):
        asyncio.run(self.wait_connection())

    async def trigger(self, channel, event, packet):
        channel = self.find_channel(channel)
        await channel.sendPacketToClients(event, packet)

    def find_channel(self, name):
        for channel in self.channels:
            if channel.name == name:
                return channel
        return None

    def create_channel(self, name):
        self.channels.append(Channel(name))
