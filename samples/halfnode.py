from bitpeer.node import *
from bitpeer.storage.shelve import ShelveStorage
import logging

stream = logging.StreamHandler()
logger = logging.getLogger('halfnode')
logger.addHandler(stream)
logger.setLevel (10)


if __name__ == "__main__":
	LASTBLOCK = '000000000933ea01ad0ee984209779baaec3ced90fa3f408719526f8d77f4943'
	LASTBLOCKINDEX = 0
	node = Node ('XTN', ShelveStorage ('./test.db'), LASTBLOCK, LASTBLOCKINDEX, maxpeers=50, logger=logger)

	node.bootstrap ()
	node.connect ()
	node.loop ()
