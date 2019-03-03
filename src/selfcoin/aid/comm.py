import asyncio
import sys

from common import globall as G
from aid.conf import tune as T
from common.crypto import Hash, Ecc
from aid.act import Ack

def check_rx(c_list):
    '''
    different c_types have different checks:
    check the valid of hash and sign of the card
    
    '''
    T.LOGGER.debug(sys._getframe().f_code.co_name)

    if c_list[G.P_VER] != G.VER:
        T.LOGGER.error('Card version is wrong.')
        return False
    
    # # valid the type of the card 
    # if c_list[G.P_TYPE] != c_type:
    #     T.LOGGER.error('Card type is wrong.')
    #     return False

    # valid hash
    content_hash = b' '.join(c_list[:G.P_HASH])
    value_hash = c_list[G.P_HASH]
    if Hash.sha(content_hash) != value_hash:
        T.LOGGER.warn('Hash of the card is wrong.')
        return False

    # valid sign
    c_sign = content_hash
    if c_list[G.P_SUBTYPE] == G.EARN:
        ID = c_list[G.P_ID_EARN]
    elif c_list[G.P_SUBTYPE] == G.PAY:
        ID = c_list[G.P_ID_PAY]
    else:
        ID = c_list[G.P_ID]

    if not Ecc.verify(c_sign, ID):
        T.LOGGER.error('Sign of the card is wrong.')
        return False

    return True


class UdpServerProtocol:
    def __init__(self):
        pass

    def connection_made(self, transport):
        T.LOGGER.debug(sys._getframe().f_code.co_name)
        self.transport = transport

    async def datagram_received(self, c_rx, addr_rx):
        T.LOGGER.debug('---------------------------------------------------')
        T.LOGGER.debug(sys._getframe().f_code.co_name)
        T.LOGGER.debug('card = ' + c_rx)
        T.LOGGER.debug('addr = ' + addr_rx)
        
        c_list = c_rx.strip().split()
        if not check_rx(c_list):
            return
        ack = Ack(G.OWN_ID, c_list)
        
        c_ack_auth = ack.run()
        if c_ack_auth:
            attempt = T.TX_ATTEMPT
            while attempt:
                attempt = attempt - 1
                self.transport.sendto(c_ack_auth, addr_rx)
                await asyncio.sleep(T.TX_INTERVAL)   
            T.LOGGER.debug('Success to TX card.')
        
