import hashlib
# import bitcoin

import binascii
import base58
from time import time

from common import globall as G

from common.ellipticcurve.privateKey import PrivateKey
from common.ellipticcurve.publicKey import PublicKey
from common.ellipticcurve.signature import Signature
from common.ellipticcurve.ecdsa import Ecdsa
from common.ellipticcurve.curve import secp256k1

from node.conf import tune as T

'''
Need to find a stable and fast lib to do crypto.
Now use ellipticcurve written by Python, which is slower.
'''

class Code():
    '''
    Not practical, it will be hard to split ' ' and '\n'
    '''
    def __init__(self):
        pass

    @classmethod
    def h2b(cls, num_hex):
        if len(num_hex)%2 != 0:
            num_hex = '0' + num_hex
        return binascii.a2b_hex(num_hex)
        
    @classmethod
    def b2h(cls, binary_bytes):
        return binascii.b2a_hex(binary_bytes)

    # @classmethod
    # def i2b(cls, num_int):
    #     num_hex = hex(num_int)[G.P_HEX:]
    #     cls.h2b(num_hex)

    # @classmethod
    # def b2i(cls, binary_bytes):
    #     num_hex = cls.b2h(binary_bytes)
    #     int(num_hex, 16)


class Hash():

    def __init__(self):
        pass

    @classmethod
    def sha(cls, text_byte):
        '''
        there is hash func in bitcoin lib, are they the same?
        In:
            text: string type of card
        Out:
            b58
        '''
        # binascii.a2b_hex(hexdigest()) = digest()
        value = hashlib.sha256(text_byte).hexdigest()
        value_int = int(value, 16)
        value_b58 = base58.b58encode_int(value_int)
        return value_b58


class Ecc():

    def __init__(self):
        pass

    # @classmethod
    # def time_b58(cls, odev):
    #     '''
    #     two pub_key_y will be deduced from pub_key_x and the curve,
    #     need odev to select the correct one
    #     '''
    #     time_int = int(time())
    #     if time_int % 2 != odev:
    #         time_int += 1
    #     return base58.b58encode_int(time_int)

    @classmethod
    def generate(cls):
        T.LOGGER.debug('')
        # use starkbank/ecdsa-python to generate
        pri = PrivateKey() # default curve is secp256k1
        pri_key = pri.secret
        
        pub = pri.publicKey()
        pub_key_x = pub.x
        pub_key_y = pub.y

        ID_int = pub_key_x * (2**G.NUM_B_ODEV) + pub_key_y%(2**G.NUM_B_ODEV)
        ID = base58.b58encode_int(ID_int)
        
        return ID, pri_key, pub_key_x, pub_key_y
        
        
    @classmethod
    def get_key(cls, nickname, f_path):
        '''
        assume there is only one pair keys
        '''
        f = open(f_path, 'rb')

        # # use bitcoin to get key
        # for l in file:
        #     l_list = l.decode('utf-8').strip('\n').split(' ')
        #     if l_list[0] == nickname:
        #         G.OWNER_NICKNAME = l_list[0]
        #         G.OWNER_PRV_KEY_HEX_STR = l_list[1]
        #         G.OWNER_PUB_KEY_HEX_STR = l_list[2]
        #         file.close()
        #         G.OWNER_PRV_KEY_INT = bitcoin.decode_privkey(G.OWNER_PRV_KEY_HEX_STR, 'hex')
        #         G.OWNER_PUB_KEY_INT_COORD = bitcoin.decode_pubkey(G.OWNER_PUB_KEY_HEX_STR, 'hex')
        #         G.OWNER_ID = base58.b58encode_int(int(G.OWNER_PUB_KEY_HEX_STR, 16)).decode('utf-8')
        #         return True

        # use starkbank/ecdsa-python to get key
        for l in f:
            l_list = l.strip().split()
            if l_list[0] == nickname.encode():
                f.close()
                G.OWN_NICKNAME = l_list[0]
                G.OWN_PRV_KEY_INT = int(l_list[1], 16)
                G.OWN_PUB_KEY_INT_X = int(l_list[2], 16)
                G.OWN_PUB_KEY_INT_Y = int(l_list[3], 16)
                G.OWN_ID = base58.b58encode_int(G.OWN_PUB_KEY_INT_X) + b'+' + \
                             base58.b58encode_int(G.OWN_PUB_KEY_INT_Y)
                return True

        f.close()
        return False


    @classmethod
    def sign(cls, c_bytes, pri_key):
        pri = PrivateKey(secret = pri_key)
        sign = Ecdsa.sign(c_bytes, pri)
        return (base58.b58encode_int(sign.r) + b'+' + base58.b58encode_int(sign.s))
        

    @classmethod
    def verify(cls, content_sign, value_sign, ID):
        '''
        card_list is a list with bytes elements
        ID is actually pub_key_x + odev
        '''        
        sign_list = value_sign.split(b'+')
        r = base58.b58decode_int(sign_list[0])
        s = base58.b58decode_int(sign_list[1])
        sign = Signature(r, s)

        ID_int = base58.b58decode_int(ID)
        pub_key_x = ID_int//(2**G.NUM_B_ODEV)
        odev = ID_int % (2**G.NUM_B_ODEV)
        pub_key_y = cls.pub_key_x2y(pub_key_x, odev)
        pub = PublicKey(pub_key_x, pub_key_y, secp256k1)

        return Ecdsa.verify(content_sign, sign, pub)

    @classmethod
    def pub_key_x2y(cls, pub_key_x, odev):
        '''
        calculate y by knowing x and curve
        '''
        return secp256k1.x2y(pub_key_x, odev)