SUPPORTED_CHAINS = [ "BTC", "XTN", "NMC", "LTC", "XLT" ]

MAGIC_VALUES = {
    "BTC": 0xD9B4BEF9,
    "XTN": 0x0709110B,
    "NMC": 0xFEB4BEF9,
    "LTC": 0xDBB6C0FB,
    "XLT": 0xDCB7C1FC
}


def isSupported (chain):
    return (chain.upper ()) in SUPPORTED_CHAINS)


class UnsupportedChainException (Exception):
    pass
