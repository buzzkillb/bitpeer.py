import socket
import codecs
from protocoin.clients import *
import protocoin.networks

class MyChainClient(ChainClient):
    def handle_block(self, message_header, message):
        print (message, message_header)
        print ("Block hash:", message.calculate_hash())

        for tx in message.txns[1:2]:
             #print ('\t',tx.calculate_hash ())

             #for txin in tx.tx_in:
             #    print ('\t',txin.signature_script)
             #    print (codecs.encode (txin.signature_script, 'hex'))
             #hash_fields = ["version", "tx_in", "tx_out", "lock_time"]
             #serializer = TxSerializer()
             #bin_data = serializer.serialize(tx, hash_fields)
             #print (codecs.encode (bin_data, 'hex'))
             pass
	 
    def handle_inv(self, message_header, message):
        print (message_header)
        getdata = GetData()
        getdata_serial = GetDataSerializer()
        getdata.inventory = message.inventory
        self.send_message(getdata)


def run_main():
    chain = 'XLT'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(networks.peers[chain][0]) #('localhost', 19333))#
    client = MyChainClient(sock, chain)
    client.handshake()

    if chain == 'BTC':
        lb = 0x00000000000000000fac2a67530fd5f6ba7c7b25f81578ddfaa405148509b7cb
    elif chain == 'XLT':
        lb = 0x22f9d7316645dc02cdd05c32db902ae4aca582c7f138b2b7cecbc58d269e58a6
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
