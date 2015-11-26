import socket
from bitpeer.clients import *

class MyChainClient(ChainClient):
    def handle_tx(self, message_header, message):
        print (message)
        for tx_out in message.tx_out:
            print ("BTC: %.8f" % tx_out.get_btc_value())
	    
    def handle_inv(self, message_header, message):
        getdata = GetData()
        getdata_serial = GetDataSerializer()
        getdata.inventory = message.inventory
        self.send_message(getdata)

def run_main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(networks.PEERS['BTC'][0])
    print ("Connected !")
    client = MyChainClient(sock, 'BTC')
    client.handshake()
    client.loop()

if __name__ == "__main__":
    run_main()
