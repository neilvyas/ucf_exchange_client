"""

ucf_exchange_client
===================

A client wrapper for ucf_exchange that aims to allow rapid development of strategies
for algorithmic trading while automatically handling IO and accounting.

"""


__version__ = '0.1'


from .app import Strategy
# TODO export all of these
from .RPC_types import Hello, Trade
