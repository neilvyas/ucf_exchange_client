from collections import defaultdict
import asyncio

from ucf_exchange_client import connection


class Strategy:
    def __init__(self, name, default_handlers=True):
        """
        """
        self.name = name

        # TODO add default handlers for hello, ack, updating accounting stuff, etc.
        self.handlers = defaultdict(list)

        self.orderid = 0
        self.orders = dict()

        # TODO add a clock here, for scheduled functions as well as if strategies need
        # access to a clock.
        self.clock = None

    def run(self, host, port):
        """Run the strategy against a connected exchange."""
        asyncio.get_event_loop().run_until_complete(self._run(host, port))

    async def _run(self, host, port):
        """Sets up the connection and handles incoming messages."""
        self.conn = await connection.create(host, port)
        while True:
            msg = await self.conn.read()
            resp = await self._handle(msg)
            for part in resp: self.conn.write(part)

    def _handle(self, msg):
        """Update state and issue outbound messages."""
        handlers = self.handlers.get(type(msg).__name__, [])
        for handler in handlers:
            # yield from handler(self, msg)
            for outmsg in handler(self, msg):
                yield outmsg

    # Defining functions on the strategy.
    def _add_handler(self, msg_type, handler):
        self.handlers[msg_type].append(handler)

    def handle(self, msg_type):
        """Decorator for adding callbacks to the strategy to handle messages.
        """
        def decorator(handler):
            # TODO add arity / argument checking here.
            self._add_handler(msg_type, handler)
            return handler
        return decorator

    def _schedule_func(self, func, timeout):
        pass

    def schedule_func(self, timeout):
        """Decorator to schedule a function to run every :timeout seconds."""
        def decorator(func):
            self._schedule_func(func, timeout)
            return func
        return decorator
