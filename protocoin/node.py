import shelve
import .clients
import .networks


class NodeClient (clients.ChainClient):
    def handle_block(self, message_header, message):
        print (message, message_header)
        print ("Block hash:", message.calculate_hash())

    def handle_inv(self, message_header, message):
        getdata = GetData()
        getdata_serial = GetDataSerializer()
        getdata.inventory = message.inventory
        self.send_message(getdata)
	
# Protocoin node
class ProtocoinNode:
    def __init__ (self, chain, dbfile, lastblockhash = None, lastblockheight = None):
	if not networks.isSupporterd (chain):
	    raise networks.UnsupportedChainException ()
		
	self.chain = chain
	self.dbfile = dbfile
	self.db = shelve.open (dbfile)
	self.sockets = []
	self.clients = []
	self.lastblockheight = lastblockheight
	self.lastblockhash = lastblockhash
	
	
    def connect (self):
	for peer in networks.peers [self.chain]:
	    try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect (peer)
		pcc = NodeClient (sock, self.chain)
		self.sockets.append (sock)
		self.clients.append (pcc)
	    except:
		pass
	if len (self.clients) == 0:
	    raise Exception ()

	getblock = GetBlocks ([self.lastblockhash]) # specify last block hash
	self.clients[0].send_message (getblock)

    def loop (self):
	self.clients[0].loop ()

	
    def bootstrap (self):
	pass

    
    def getLastBlockHeight (self):
	return None

    
    def getBlockHash (self, index):
	return None

    
    def getBlockByHash (self, bhash):
	return None

    
    def broadcastTransaction (self, transaction):
	return None

    
    def getTransaction (self, txid):
	return None
