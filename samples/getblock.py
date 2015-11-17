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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(networks.peers['BTC'][0])
    client = MyChainClient(sock, 'BTC')
    client.handshake()

    getblock = GetBlocks ([0x00000000000000000fac2a67530fd5f6ba7c7b25f81578ddfaa405148509b7cb]) # specify last block hash
    client.send_message (getblock)
    
    client.loop()

if __name__ == "__main__":
    run_main()
