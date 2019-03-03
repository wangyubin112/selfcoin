import asyncio

from common import globall as G
from god.conf import tune as T
from common.crypto import Hash, Ecc

from god import handle

def check_rx(c_list):
    '''
    different c_types have different checks:
    check the valid of hash and sign of the card
    
    '''
    T.LOGGER.debug('')

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
    T.LOGGER.debug(content_hash)
    T.LOGGER.debug(value_hash)
    if Hash.sha(content_hash) != value_hash:
        T.LOGGER.warn('Hash of the card is wrong.')
        return False
    T.LOGGER.debug('hash success')

    # valid sign
    content_sign = b' '.join(c_list[:G.P_SIGN])
    value_sign = c_list[G.P_SIGN]
    ID = c_list[G.P_ID_NODE]

    if not Ecc.verify(content_sign, value_sign, ID):
        T.LOGGER.error('Sign of the card is wrong.')
        return False

    T.LOGGER.debug('check_rx success')
    return True


class UdpServerProtocol:
    def __init__(self, loop, ch_own):
        self.ch_own = ch_own
        self.loop = loop

    def connection_made(self, transport):
        T.LOGGER.debug('')
        self.transport = transport

    def datagram_received(self, c_rx, addr_rx):
        T.LOGGER.debug('--------------------- receive one card ------------------------------------')
        T.LOGGER.debug(c_rx)        
        T.LOGGER.debug(addr_rx)
        
        c_list = c_rx.split(b' ')
        if not check_rx(c_list):
            T.LOGGER.debug('discard this card')
            return

        task = rx_tx(self, c_list, addr_rx)
        asyncio.run_coroutine_threadsafe(task, self.loop)

        
async def rx_tx(self, c_list, addr_rx):
    T.LOGGER.debug('')

    c_auth = await handle.handle(self, c_list)
        
    if c_auth:
        T.LOGGER.debug('rx handle success')
        attempt = T.TX_ATTEMPT
        while attempt:
            self.transport.sendto(c_auth, addr_rx)
            await asyncio.sleep(T.TX_INTERVAL)
            attempt -= 1            
        T.LOGGER.debug('Success to TX card.')
