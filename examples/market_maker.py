from ucf_exchange_client import Strategy

market_maker = Strategy('mm')

@market_maker.handle('Handshake')
def initialize(state, msg):
    state.theos = {}
    return []

@market_maker.handle('Trade')
def update_values(state, msg):
    if msg.ticker not in state.theos:
        state.theos[msg.ticker] = msg.price
    else:
        state.theos[msg.ticker] = (state.theos[msg.ticker] + msg.price) / 2
    return []


market_maker.run('localhost', 8166)
