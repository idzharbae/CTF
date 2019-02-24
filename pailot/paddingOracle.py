from paddingoracle import BadPaddingException, PaddingOracle  # https://github.com/mwielgoszewski/python-paddingoracle
from base64 import b64encode, b64decode  
from urllib import quote, unquote  
import requests  
import socket  
import time

class PadBuster(PaddingOracle):  
    def __init__(self, **kwargs):
        super(PadBuster, self).__init__(**kwargs)

    def oracle(self, data, **kwargs):
        print("[*] Trying: {}".format(b64encode(data)))

        # Do Crypto that throws something different if padding error
        r = requests.post('http://crypto.chal.csaw.io:8001/', data={'matrix-id':b64encode(data)})
        # r = p.recvline()
        if 'AES' in r.text:
            print ("[*] Padding error!")
            raise BadPaddingException
        else:
            print ("[*] No padding error")

if __name__ == '__main__':  
    import logging
    import sys

    logging.basicConfig(level=logging.DEBUG)
    # This is a random string the server printed for us, 
    # assuming have to decrypt this, and see what we get
    encrypted_value = 'XImKWrDW5dFvUVDuwbwLy+nHJmDClEXWLcJRmf44atNU2tKZcVFoyT81bmUkL6WPWg7Dn8HMeeWwhiC+CI8QhDtYqGCBidtHZ+alNqnyTn4='
    padbuster = PadBuster()

    value = padbuster.decrypt(b64decode(encrypted_value), block_size=16, iv=bytearray(16))

    print('Decrypted: %s => %r' % (encrypted_value, value))