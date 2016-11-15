from collections import namedtuple
from ucf_exchange_client import Strategy


# Stance on how to trade in a market.
Stance = namedtuple('Stance', ['ticker', 'initial_value', 'initial_spread', 'num_steps', 'max_spread', 'step', 'total_price'])
# initial_value is the initial theoretical value of the security.
# initial_spread is the initial spread percentage.
# num_steps is the number of steps the MM will generate.
# max_spread is the maximum spread percentage tolerable.
# step is the percentage between every position the MM has in the market.
# total_price is the total value of a position the MM could hold.


# TODO(igm): set these in flags
stances = [
    Stance('AAPL', 106.10, 0.01, 10, 0.05, 0.01, 10000),
    Stance('IGM', 23.45, 0.01, 10, 0.07, 0.01, 10000)
]

market_maker = Strategy('mm')

@market_maker.handle('Handshake')
def initialize(state, msg):
    state.theos = {}
    orders = []
    for stance in stances:
        # max_bid and min_ask define the initial spread.
        max_bid = stance.initial_value * (1 - stance.initial_spread / 2.)
        min_ask = stance.initial_value * (1 + stance.initial_spread / 2.)

        # We will place all of our initial buy and sell orders here.
        orders = orders.concat(generate_orders(Buy, stance.ticker, stance.initial_value, max_bid, -step, stance.num_steps))
        orders = orders.concat(generate_orders(Sell, ticker, stance.initial_value, min_ask, step, stance.num_steps))
    return orders

@market_maker.handle('Trade')
def update_values(state, msg):
    if msg.ticker not in state.theos:
        state.theos[msg.ticker] = msg.price
    else:
        state.theos[msg.ticker] = (state.theos[msg.ticker] + msg.price) / 2
    return []


def generate_orders(order_type, ticker, quantity, price, step, count=10):
    step_tot = 1. + step
    return [
        order_type(ticker, quantity, price + price * step ** x)
        for x in range(count)
    ]


if __name__ == "__main__":
    market_maker.run('localhost', 8166)
