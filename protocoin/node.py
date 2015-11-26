import shelve
import socket
from . import clients
from . import networks


class SeedClient (clients.ChainClient):
	def __init__ (self, socket, chain, node):
		self.node = node
		super (SeedClient, self).__init__ (socket, chain)

	def handle_addr (self, message_header, message):
		self.node.handle_addr (message_header, message)


class NodeClient (clients.ChainClient):
	def __init__ (self, socket, chain, node):
		self.node = node
		super (NodeClient, self).__init__ (socket, chain)

	def handle_block(self, message_header, message):
		print (message, message_header)
		print ("Block hash:", message.calculate_hash())
		self.node.handle_block (message_header, message)

	def handle_inv(self, message_header, message):
		getdata = GetData()
		getdata_serial = GetDataSerializer()
		getdata.inventory = message.inventory
		self.send_message(getdata)


class ProtocoinNode:
	def __init__ (self, chain, dbfile, lastblockhash = None, lastblockheight = None):
		if not networks.isSupported (chain):
			raise networks.UnsupportedChainException ()

		self.chain = chain
		self.dbfile = dbfile
		self.db = shelve.open (dbfile)
		self.sockets = []
		self.clients = []
		self.threads = []
		self.peers = []
		self.blockFilter = lambda b: b

		if ('lastblockheight' in self.db) and (self.db ['lastblockheight'] > lastblockheight):
			self.lastblockheight = self.db ['lastblockheight']
			self.lastblockhash = self.db ['lastblockhash']
		else:
			self.lastblockheight = lastblockheight
			self.lastblockhash = lastblockhash
			self.db ['lastblockheight'] = lastblockheight
			self.db ['lastblockhash'] = lastblockhash

	def connect (self):
		for peer in self.peers:
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.connect (peer)
				pcc = NodeClient (sock, self.chain, self)
				self.sockets.append (sock)
				self.clients.append (pcc)
			except:
				pass
		if len (self.clients) == 0:
			raise Exception ()
		#getblock = GetBlocks ([self.lastblockhash]) # specify last block hash
		#self.clients[0].send_message (getblock)


	def loop (self):
		# Start the loop in each client as a new thread
		for cl in self.clients:
			t = Thread (target=cl.loop, args=())
			t.start ()
			self.threads.append (t)

	def stop (self):
		for cl in self.clients:
			cl.stop ()

		for t in self.threads:
			t.join ()


	# TODO This is called by all clients when a new block should be handled; should be thread safe!
	def handle_block (self, message_header, message):
		b = self.blockFilter (message)
		print (message_header, message)


	# TODO This is called by all seeds clients when a new list should be handled; should be thread safe!
	def handle_addr (self, message_header, message):
		print (message_header, message)

		for peer in message.addresses:
			print (peer)


	# Contact the seed nodes for retrieving a peer list, also load a file peer list
	def bootstrap (self):
		st = []

		for seed in networks.SEEDS [self.chain]:
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.connect ((seed, networks.PORTS [self.chain]))
				pcc = SeedClient (sock, self.chain, self)

				getaddr = GetAddr ()
				pcc.send_message (getblock)
				t = Thread (target=pcc.loop, args=())
				t.start ()
				st.append ([t, pcc])
			except:
				pass

		if len (st) == 0:
			raise Exception ()

		while len (self.peers) < 10:
			time.sleep (10)
			print ('Waiting for seeds', len (self.peers))

		for s in st:
			s[1].stop ()
			s[0].join ()

		print ('Bootstrap done')

	def getLastBlockHeight (self):
		return self.db['lastblockheight']

	def getBlockHash (self, index):
		return self.db['bi'+str(index)]

	def getBlockByHash (self, bhash):
		return self.db[str(bhash)]

	def broadcastTransaction (self, transaction):
		return None
