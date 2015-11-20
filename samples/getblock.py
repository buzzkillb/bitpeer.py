import socket
from protocoin.clients import *
import protocoin.networks

class MyChainClient(ChainClient):
    def handle_block(self, message_header, message):
        print (message, message_header)
        print ("Block hash:", message.calculate_hash())

    def handle_inv(self, message_header, message):
        print (message_header)
        getdata = GetData()
        getdata_serial = GetDataSerializer()
        getdata.inventory = message.inventory
        self.send_message(getdata)


def run_main():
    chain = 'XLT'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 19333))#networks.peers[chain][0])
    client = MyChainClient(sock, chain)
    client.handshake()

    if chain == 'BTC':
        lb = 0x00000000000000000fac2a67530fd5f6ba7c7b25f81578ddfaa405148509b7cb
    elif chain == 'XLT':
        lb = 0x3bb88477fa7bc04177ef1a3a98e5ee5ad58f635ea0637bb26e25acc1f4c2fae0
    elif chain == 'XTN':
        lb = 0x00000000004c71555e5954065dcd61b305c3aeea3d64b689b809b1ea087649dd
    else:
        raise Exception ('This sample has test data only for BTC and XLT')

    print ('GetBlock')
    getblock = GetBlocks ([lb]) # specify last block hash
    client.send_message (getblock)

    print ('Loop')
    client.loop()

if __name__ == "__main__":
    run_main()
