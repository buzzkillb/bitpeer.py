import socket
from bitpeer.node import *


if __name__ == "__main__":
    LASTBLOCK = '00000000005a060113161bd7a46d0812b72c5f5c0618777e70288c032a3b98c7'
    LASTBLOCKINDEX = '606496'
    node = ProtocoinNode ('XTN', './test.db', LASTBLOCK, LASTBLOCKINDEX)

    node.bootstrap ()
    node.loop ()
