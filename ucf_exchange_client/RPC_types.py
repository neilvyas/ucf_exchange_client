"""
Encodes possible messages from the RPC.
"""
from collections import namedtuple


# Ensure that all names and fields match up with the RPC so that it's easy to
# go back and forth between the JSON RPC representation and the python repr.
#
# NOTE: we don't include a field for `order_id` on trade messages because the
# client wrapper handles that accounting, and we want these messages to be used
# by actual clients.

# Received messages.
HandshakeAck = namedtuple('Handshake', ['posns'])
Trade = namedtuple('Trade', ['ticker', 'direction', 'quantity', 'price'])
Ack = namedtuple('Ack', ['order_id', 'direction', 'price', 'quantity'])
Fill = namedtuple('Fill', ['order_id', 'price', 'quantity'])
Out = namedtuple('Out', ['order_id'])
Reject = namedtuple('Reject', ['body'])

received_messages = {
    "handshake": HandshakeAck,
    "trade": Trade,
    "ack": Ack,
    "fill": Fill,
    "out": Out,
    "reject": Reject,
}


def msg_from_rpc(rpc_msg):
    """Given a message from the JSON RPC, marshal it into a python message.

    Note: this doesn't read a JSON string, but a python dictionary. You should
    load the message yourself."""
    # TODO: determine exception handling scheme.
    # We want to just ignore mis-typed messages.
    msg_type = rpc_msg.pop("type", None)
    if not msg_type:
        return None

    msg_constructor = received_messages.get(msg_type)
    if not msg_constructor:
        return None

    # since the fields of the RPC and the python types are the same,
    # we can just do this!
    return msg_constructor(**rpc_msg)


# Sent messages. Pass `quantity = - 1` to place a market order.
Handshake = namedtuple('Handshake', ['name'])
Buy = namedtuple('Buy', ['ticker', 'quantity'])
Sell = namedtuple('Sell', ['ticker', 'quantity'])
Cancel = namedtuple('Cancel', ['order_id'])


def msg_to_rpc(msg):
    """Given a python message, fit it to the JSON RPC.

    Note: this doesn't return actual JSON. You should do the conversion
    yourself. If necessary, you should also append an order_id."""
    res = msg._asdict()
    res["type"] = type(msg).__name__.lower()
    if isinstance(msg, Buy) or isinstance(msg, Sell):
        if msg.quantity < 0:
            res.pop("quantity", None)
            res["type"] = "market"
            res["direction"] = "buy" if isinstance(msg, Buy) else "sell"

    return res
