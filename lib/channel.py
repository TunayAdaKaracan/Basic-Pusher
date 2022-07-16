from .imports import json


class Channel:
    def __init__(self, name):
        self.name = name
        self.connected_clients = []

    async def sendPacketToClients(self, event, packet):
        packet["_channel_name"] = self.name
        packet["_event_type"] = event
        packet_dumped = json.dumps(packet)
        for websocket in self.connected_clients:
            await websocket.send(packet_dumped)

    def add_client(self, client):
        self.connected_clients.append(client)

    def remove_client(self, client):
        self.connected_clients.remove(client)
