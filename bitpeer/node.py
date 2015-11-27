import binascii
import shelve
import socket
import random
from io import BytesIO
from threading import Thread, Lock, Timer
from . import clients
from . import networks
from . import serializers


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
		#print (message, message_header)
		#print ("Block hash:", message.calculate_hash())
		self.node.handle_block (message_header, message)

	def handle_inv(self, message_header, message):
		getdata = clients.GetData()
		getdata_serial = clients.GetDataSerializer()
		getdata.inventory = message.inventory
		self.send_message(getdata)


class Node:
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
		self.synctimer = None
		self.postblocks = {}


		# Set current block
		if ('lastblockheight' in self.db) and (self.db ['lastblockheight'] > lastblockheight):
			pass
		elif lastblockheight != None and lastblockhash != None:
			self.db ['lastblockheight'] = int (lastblockheight)
			self.db ['lastblockhash'] = lastblockhash
		else:
			self.db ['lastblockheight'] = 0
			self.db ['lastblockhash'] = networks.GENESIS[chain]


	# Contact the seed nodes for retrieving a peer list, also load a file peer list
	def bootstrap (self):
		for seed in networks.SEEDS [self.chain]:
			try:
				(hostname, aliaslist, ipaddrlist) = socket.gethostbyname_ex (seed)
				for ip in ipaddrlist:
					self.peers.append ((ip, networks.PORTS[self.chain]))

			except Exception as e:
				pass

		if len (self.peers) == 0:
			raise Exception ()

		random.shuffle (self.peers)
		self.peers = self.peers [0:10]

		print ('Bootstrap done')


	def connect (self):
		for peer in self.peers:
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.settimeout (3.0)
				sock.connect (peer)
				sock.settimeout (None)
				pcc = NodeClient (sock, self.chain, self)
				pcc.handshake ()
				self.sockets.append (sock)
				self.clients.append (pcc)
			except:
				pass

		if len (self.clients) == 0:
			raise Exception ()

		self.synctimer = Timer (0.0, self.sync)
		self.synctimer.start ()


	def sync (self):
		if len (self.clients) == 0:
			return
			
		r = random.randint(0, len (self.clients) - 1)
		p = self.clients [r]
		try:
			getblock = clients.GetBlocks ([int (self.db['lastblockhash'], 16)])
			p.send_message (getblock)
		except:
			self.clients.remove (p)

		self.synctimer.cancel ()
		self.synctimer = Timer (0.5, self.sync)
		self.synctimer.start ()


	def innerLoop (self, cl):
		try:
			cl.loop ()
		except:
			self.clients.remove (cl)

	def loop (self):
		# Start the loop in each client as a new thread
		for cl in self.clients:
			t = Thread (target=self.innerLoop, args=(cl,))
			t.start ()
			self.threads.append (t)

	def stop (self):
		for cl in self.clients:
			cl.stop ()

		for t in self.threads:
			t.join ()


	def handle_block (self, message_header, message):
		#print (message_header, message)
		b = self.blockFilter (message)

		#print (b.calculate_hash ())
		if b.prev_block == int (self.db['lastblockhash'], 16):
			# Serialize block
			deserializer = serializers.BlockSerializer ()
			bb = deserializer.serialize (b)

			hash = str (b.calculate_hash ())[2:-1]
			self.db[str (int (self.db['lastblockheight']) + 1)] = hash
			self.db[hash] = bb
			self.db['lastblockheight'] += 1
			self.db['lastblockhash'] = hash
			print (self.db['lastblockheight'], self.db['lastblockhash'])

			if hash in self.postblocks:
				self.handle_block (None, self.prevblocks[hash])
				print ('PREVBLOCK found')
				del self.postblocks[hash]

			self.db.sync ()

			self.synctimer.cancel ()
			self.synctimer = Timer (0.5, self.sync)
			self.synctimer.start ()
		else:
			hash = str (hex (b.prev_block))[2:]
			hash = '0' * (64 - len (hash)) + hash
			if not hash in self.db:
				#print ('prev', hash)
				self.postblocks [hash] = b


	def getLastBlockHeight (self):
		return self.db['lastblockheight']

	def getBlockHash (self, index):
		if str(index) in self.db:
			return self.db[str(index)]
		else:
			return None

	def getBlockByHash (self, bhash):
		if bhash in self.db:
			#deserializer = serializers.BlockSerializer ()
			#b = deserializer.deserialize(BytesIO (self.db[bhash]))
			return self.db[bhash]
		else:
			return None

	def broadcastTransaction (self, transaction):
		return None
