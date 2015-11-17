import socket
from protocoin.clients import *

class MyChainClient(ChainClient):
    def handle_block(self, message_header, message):
        print (message)
        print ("Block hash:", message.calculate_hash())

    def handle_inv(self, message_header, message):
        getdata = GetData()
        getdata_serial = GetDataSerializer()
        getdata.inventory = message.inventory
        self.send_message(getdata, getdata_serial)

    def handle_message_header(self, message_header, payload):
        print ("Received message:", message_header.command)

    def handle_send_message(self, message_header, message):
        print ("Message sent:", message_header.command)

def run_main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("bitcoin.sipa.be", 8333))
    client = MyChainClient(sock, 'BTC')
    client.handshake()
    client.loop()

if __name__ == "__main__":
    run_main()
