"""

ucf_exchange_client
===================

A client wrapper for ucf_exchange that aims to allow rapid development of strategies
for algorithmic trading while automatically handling IO and accounting.

"""


__version__ = '0.1'


from .app import Strategy
# We only expose the sent-type messages.
from .RPC_types import (
    Handshake,
    Buy,
    Sell,
    Cancel,
)
