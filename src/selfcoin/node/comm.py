# import socket
import sys
import struct
from time import time
import threading
import asyncio

from common.crypto import Hash, Ecc
from common import globall as G
from node.conf import tune as T


def check_rx(c_list, hash_src=None):
    '''
    check the valid of hash and sign of the card
    '''
    T.LOGGER.debug('')
    
    if c_list[G.P_VER] != G.VER:
        T.LOGGER.error('Card version is wrong.')
        return False

    # valid hash    
    content_hash = b' '.join(c_list[:G.P_HASH])
    value_hash = c_list[G.P_HASH]
    if Hash.sha(content_hash) != value_hash:
        T.LOGGER.warn('Hash of the card is wrong.')
        return False

    # valid sign
    content_sign = b' '.join(c_list[:G.P_SIGN])
    value_sign = c_list[G.P_SIGN]
    if c_list[G.P_TYPE] == G.EARN:
        ID = c_list[G.P_ID_EARN]
    elif c_list[G.P_TYPE] == G.PAY:
        ID = c_list[G.P_ID_PAY]
    elif c_list[G.P_TYPE] == G.CHARGE or c_list[G.P_TYPE] == G.POST:
        ID = c_list[G.P_ID_GOD]
    elif c_list[G.P_TYPE] == G.ACK:
        ID = c_list[G.P_ID_ACK]
        # check if it is the source card ack
        if c_list[G.P_HASH_SRC] != hash_src:
            T.LOGGER.error('Not the corresponding acker.')
            return False
    
    if not Ecc.verify(content_sign, value_sign, ID):
        T.LOGGER.error('Sign of the card is wrong.')
        return False

    return True


async def send(self):
    T.LOGGER.debug('')
    
    attempt = T.TX_ATTEMPT
    while attempt:
        T.LOGGER.debug('send start')
        self.transport.sendto(self.c_tx)
        await asyncio.sleep(T.TX_INTERVAL)
        try:
            if self.on_con_lost.result():
                T.LOGGER.debug('get rx in time')
                return
        except:
            attempt -= 1

    T.LOGGER.debug('send as many as possible already')
    self.on_con_lost.set_result(True)
    

class UdpClientProtocol:
    def __init__(self, loop, c_tx, hash_c):
        self.c_tx = c_tx
        self.loop = loop
        self.transport = None
        self.on_con_lost = loop.create_future()
        self.c_rx_list = None
        self.hash_c = hash_c

    def connection_made(self, transport):
        T.LOGGER.debug('')

        self.transport = transport                         
        
        task = send(self)
        asyncio.run_coroutine_threadsafe(task, self.loop) 
    

    def datagram_received(self, c_rx, addr):
        T.LOGGER.debug('')

        c_list = c_rx.strip().split()
        if check_rx(c_list, self.hash_c):
            self.c_rx_list = c_list
            T.LOGGER.debug('Success to get card ack, now close the socket.')

            #self.transport.close()
            self.on_con_lost.set_result(True)

    def error_received(self, exc):
        T.LOGGER.debug(exc)

    def connection_lost(self, exc):
        T.LOGGER.debug(exc)
        self.on_con_lost.set_result(True)


class UdpGroupProtocol:
    def __init__(self, loop, c_tx):
        self.c_tx = c_tx
        self.loop = loop
        self.transport = None
        self.on_con_lost = loop.create_future()
    
    def connection_made(self, transport):
        T.LOGGER.debug('')

        self.transport = transport 

        task = send(self)
        asyncio.run_coroutine_threadsafe(task, self.loop) 

    def datagram_received(self, c_rx, addr):
        T.LOGGER.debug(c_rx)
        T.LOGGER.debug(addr)

    def error_received(self, exc):
        T.LOGGER.debug(exc)

    def connection_lost(self, exc):
        T.LOGGER.debug(exc)
        self.on_con_lost.set_result(True)


class UdpServerProtocol:
    def __init__(self, Act):
        self.Act = Act

    def connection_made(self, transport):
        T.LOGGER.debug('')
        self.transport = transport

    def datagram_received(self, c_rx, addr_rx):
        T.LOGGER.debug('---------------------------------------------------')
        T.LOGGER.debug('')
        
        c_list = c_rx.strip().split()
        if not check_rx(c_list):
            return
        
        act = self.Act(T.OWN_ID, c_list)
        card_ack_auth = act.run()
        if card_ack_auth:
            attempt = T.TX_ATTEMPT
            while attempt:  
                attempt = attempt - 1          
                self.transport.sendto(card_ack_auth, addr_rx)
                # await asyncio.sleep(T.TX_INTERVAL)   
            T.LOGGER.debug('Success to TX card.')


    
async def tx_rx(cls_App, c_auth, hash_c):
    T.LOGGER.debug('')    
    
    transport, protocol = await cls_App.loop.create_datagram_endpoint(
                lambda: UdpClientProtocol(cls_App.loop, c_auth, hash_c),
                remote_addr=T.ADDR_GOD)
    try:
        await protocol.on_con_lost
    finally:
        transport.close()  

        T.LOGGER.debug(protocol.c_rx_list)
        return protocol.c_rx_list


async def tx(cls_App, c_auth):
    T.LOGGER.debug('')
    
    transport, protocol = await cls_App.loop.create_datagram_endpoint(
                lambda: UdpGroupProtocol(cls_App.loop, c_auth),
                remote_addr=T.ADDR_GROUP)
    try:
        await protocol.on_con_lost
    finally:
        transport.close()  

        T.LOGGER.debug("Broadcast card finished")
        return True

async def rx():
    T.LOGGER.debug('')



class Udp:
    def __init__(self, activity):
        '''
        the Udp can only act as tx or rx, 
        can not act as both
        now I think tx is for client and rx for server
        '''
        self.activity = activity
        
        # start the link
        self.link = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.link.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.activity['rx_buf']) # tx buf
        self.link.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.activity['tx_buf']) # rx buf


    def tx(self, card_bytes, addr_peer, card_hash=None):
        G.LOGGER.debug('')

        attempt = self.activity['tx_attempt']
        timeout = self.activity['rx_timeout']
        self.link.connect(addr_peer) # connect action can cover last settings, 
                                     # this is used to filter and receive paticular addr in UDP
        
        while attempt:  
            attempt = attempt - 1          
            self.link.sendto(card_bytes, addr_peer)
            if self.activity['tx_interval']:
                sleep(self.activity['tx_interval'])
            else:
                time_start = time() # the current time in seconds since the Epoch
                while True:
                    self.link.settimeout(timeout)
                    card_rx, addr_rx = self.link.recvfrom(self.activity['card_size'])                    
                    card_list = card_rx.strip().split()
                    if self.ack_check(card_list, card_hash):
                        G.LOGGER.debug('Success to get card ack.')
                        return card_list
                    else:
                        timeout = timeout - (time() - time_start)
                        continue
                    
        if self.activity['tx_interval']:
            G.LOGGER.debug('Success to TX card.')
            return True
        else:
            G.LOGGER.warn('Timeout to get right card ack.')
            return False



            

    def ack_check(self, card_list, card_hash):
        G.LOGGER.debug('')

        # first check the card
        if not rx_check(card_list):
            return False

        # then check the acker
        if card_list[G.POSITION_ACK_HASH] != card_hash:
            G.LOGGER.error('Not the corresponding acker.')
            return False

        return True

    def rx_check(self, card_list):
        '''
        different card_types have different checks:
        check the valid of hash and sign of the card
        Note that in trade, there is no complete trade card to tranceive,
        so G.P_PUB_KEY to verify is ok to cover all trade card
        '''
        G.LOGGER.debug('')
        
        # valid the type of the card 
        if card_list[0] != self.activity['card_type']:
            G.LOGGER.error('Card type is wrong.')
            return False

        if card_list[1] not in self.activity['card_subtype']:
            G.LOGGER.error('Card subtype is wrong.')
            return False

        # valid the card of the hash and sign
        hash_content = b' '.join(card_list[:-1])
        hash_value = card_list[-1]
        if Hash.sha256(hash_content) != hash_value:
            G.LOGGER.warn('Hash of the card is wrong.')
            return False

        sign_content = b' '.join(card_list[:-2])
        sign_value = card_list[-2]
        if not Ecc.verify(sign_content, G.P_PUB_KEY):
            G.LOGGER.error('Sign of the card is wrong.')
            return False

        return True


