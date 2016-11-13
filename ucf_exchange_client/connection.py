import asyncio
import websockets

from .RPC_types import msg_from_json, msg_to_json


class Connection:
    """The connection to the UCF exchange backend."""

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.websocket = websockets.connect(self._websocket_uri())

    async def write(self, msg):
        """Write one message to the socket."""
        json = msg_to_json(msg)
        return self.websocket.send(json)

    async def read(self):
        """Read one complete message from socket."""
        json = await websocket.recv()
        msg = msg_from_json(json)
        return msg

    def _websocket_uri(self):
        return 'ws://%s:%s/'.format(self.host, self.port)

def create(host, port):
    socket = Socket(host, port)
    socket.connect()
    return socket
