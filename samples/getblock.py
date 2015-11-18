import socket
from protocoin.clients import *
import protocoin.networks

class MyChainClient(ChainClient):
    def handle_block(self, message_header, message):
        print (message, message_header)
        print ("Block hash:", message.calculate_hash())

    def handle_inv(self, message_header, message):
        getdata = GetData()
        getdata_serial = GetDataSerializer()
        getdata.inventory = message.inventory
        self.send_message(getdata)


def run_main():
    chain = 'BTC'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(networks.peers[chain][0])
    client = MyChainClient(sock, chain)
    client.handshake()

    if chain == 'BTC':
	lb = 0x00000000000000000fac2a67530fd5f6ba7c7b25f81578ddfaa405148509b7cb
    elif chain == 'XLT':
	lb = 0xd21fb875ca8244dcb6ae90b1e8e74f31fcc985a814450d188c59f6fff337c6df
    else:
	raise Exception ('This sample has test data only for BTC and XLT')
	
    getblock = GetBlocks ([lb]) # specify last block hash
    client.send_message (getblock)
    
    client.loop()

if __name__ == "__main__":
    run_main()
