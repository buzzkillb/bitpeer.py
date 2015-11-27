from bitpeer.node import *
import logging

stream = logging.StreamHandler()
logger = logging.getLogger('halfnode')
logger.addHandler(stream)
logger.setLevel (10)


if __name__ == "__main__":
	LASTBLOCK = '000000000933ea01ad0ee984209779baaec3ced90fa3f408719526f8d77f4943'
	LASTBLOCKINDEX = 0
	node = Node ('XTN', './test.db', LASTBLOCK, LASTBLOCKINDEX, logger=logger)

	node.bootstrap ()
	node.connect ()
	node.loop ()
