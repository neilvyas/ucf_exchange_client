"""
Encodes possible messages from the RPC.
"""
from collections import namedtuple


# Ensure that all names and fields match up with the RPC so that it's easy to
# go back and forth between the JSON RPC representation and the python repr.
Hello = namedtuple('Hello', ['posns'])
Trade = namedtuple('Trade', ['ticker', 'direction', 'quantity', 'price'])
# TODO encode them all here...
# TODO switch from namedtuples to actual classes for better docstrings?
# TODO note that we shouldn't worry about including order_id as a field
# because we'll  handle it automatically in Strategy.run.


def msg_from_json(json_msg):
    """Given a message from the JSON RPC, marshal it into a python message."""
    pass


def msg_to_json(msg):
    """Given a python message, fit it to the JSON RPC."""
    # call msg._asdict() and then add a field for 'type'.
    pass
