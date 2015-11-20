SUPPORTED_CHAINS = [ "BTC", "XTN", "NMC", "LTC", "XLT" ]

MAGIC_VALUES = {
    "BTC": 0xD9B4BEF9,
    "XTN": 0x0709110B,
    "NMC": 0xFEB4BEF9,
    "LTC": 0xFBC0B6DB,
    "XLT": 0xDCB7C1FC
}

peers = {
    "BTC": [("bitcoin.sipa.be", 8333)],
    "XTN": [],
    "NMC": [],
    "LTC": [],
    "XLT": [("51.254.215.160", 19333)]
}


class UnsupportedChainException (Exception):
    pass

def isSupported (chain):
    return (chain.upper () in SUPPORTED_CHAINS)

