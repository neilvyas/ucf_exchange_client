from collections import defaultdict
from .utils.socket import get_msg, get_conn
from .RPC_types import msg_from_json, msg_to_json


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
        sock = get_conn(host, port)
        while not sock.closed:
            # TODO: figure out how to run scheduled functions within this event loop,
            # since get_msg is probably blocking. (We can make it non-blocking to make
            # stuff easier).
            msg = msg_from_json(get_msg(sock))
            for outmsg in self._handle(msg):
                # TODO if we're making orders then we should
                # handle the orderid stuff automatically.
                sock.write(msg_to_json(msg._asdict()))

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
