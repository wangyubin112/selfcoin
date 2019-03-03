from time import time
import base58

from common.chain import Chain
from common import globall as G
from god.conf import tune as T
from common.crypto import Ecc, Hash

def ack_god(ch_god, content, hash_src):
    T.LOGGER.debug('')

    type_c = G.ACK
    
    c = (
            G.VER + b' ' +                               # 0
            base58.b58encode_int(int(time())) + b' ' +   # 1
            type_c + b' ' +                              # 2
            ch_god.ID_own + b' ' +                         # 3
            hash_src + b' ' +                            # 4                
            content + b' '                               # 5
        )

    sign_c = Ecc.sign(c, ch_god.pri_key)
    hash_c = Hash.sha(c + b' ' + sign_c)
    c_auth = c + b' ' + sign_c + b' ' + hash_c
    return c_auth


async def init(self, type_act):
    T.LOGGER.debug('')

    # remained coin: -6
    self.coin_rest = self.ch_own.coin_rest
    # if self.ch_own.c_last[G.P_TYPE] == G.CHARGE:
    #     self.coin_rest = (base58.b58decode_int(self.ch_own.c_last[G.P_COIN_REST]) + 
    #                         base58.b58decode_int(self.ch_own.c_last[G.P_COIN_CHRE]))
    # elif self.ch_own.c_last[G.P_TYPE] == G.REDEEM:
    #     self.coin_rest = (base58.b58decode_int(self.ch_own.c_last[G.P_COIN_REST]) - 
    #                         base58.b58decode_int(self.ch_own.c_last[G.P_COIN_CHRE]))
    # else:
    #     self.coin_rest = base58.b58decode_int(self.ch_own.c_last[G.P_COIN_REST])

    # previous mutual chain index: -5            
    self.i_m = base58.b58decode_int(self.c_rx_list[G.P_I_M])
    row = await self.ch_own.get_guide(self.ID_node)
    if row == None: # for node register in god
        if type_act == G.CHARGE and self.i_m == 0:
            self.i_ch_m_pre = 0
        else:
            T.LOGGER.error('guide of ID_node is None')
            return False
    else:
        if type_act == G.CHARGE or type_act == G.REDEEM:   
            p_guide_m = T.P_GUIDE_M_CHRE
            p_guide_ch = T.P_GUIDE_CH_CHRE
        elif type_act == G.POST:
            p_guide_m = T.P_GUIDE_M_POST
            p_guide_ch = T.P_GUIDE_CH_POST
        else:
            T.LOGGER.error('act type is not valid')
            return False

        self.i_m_guide = row[p_guide_m]
        # check i_m
        if self.i_m == (self.i_m_guide + 1) % G.NUM_I_M:            
            self.i_ch_m_pre = row[p_guide_ch]
        else:
            # if self.i_m <= self.i_m_guide and self.i_m >= 0:
            if self.i_m == self.i_m_guide:# TODO: only consider this case now
                self.i_ch_fetch = row[p_guide_ch] 
                T.LOGGER.debug('mutual index small, turn to TX card already exist')
                return True
            else:
                T.LOGGER.error('mutual index not valid: rx_card is {0}; DB guide is {1}'.
                            format(self.i_m, self.i_m_guide))
                return False

    # god chain index: -4 --> chain.i_ch

    # previous hash: -3
    self.hash_pre = self.ch_own.c_last[G.P_HASH]

    T.LOGGER.debug(self.hash_pre)

    return True    


class Root():
    def __init__(self, ch_own):
        self.ch_own = ch_own
        self.ID_god = ch_own.ID_own
        self.type = G.ROOT
        self.hash_content = Hash.sha(G.ID_REAL_GOD)
        self.i_m = 0
        self.coin_rest = 0
        self.i_ch_m_pre = 0
        self.i_ch = 0
        self.hash_pre = Hash.sha(G.ID_REAL_GOD)
                
    def root(self):
        T.LOGGER.debug('')     


        
        c_root = (G.VER + b' ' +                                    # 0
                  base58.b58encode_int(int(time())) + b' ' +        # 1
                  self.type + b' ' +                                # 2
                  self.ID_god + b' ' +                              # 3
                  self.ID_god + b' ' +                              # 4
                  base58.b58encode_int(self.i_m) + b' ' +           # 5
                  self.hash_content + b' ' +                        # 6
                  base58.b58encode_int(self.coin_rest) + b' ' +     # -6
                  base58.b58encode_int(self.i_ch_m_pre) + b' ' +    # -5
                  base58.b58encode_int(self.i_ch) + b' ' +          # -4
                  self.hash_pre                                     # -3
                  )
        sign_c_root = Ecc.sign(c_root, self.ch_own.pri_key)         # -2
        hash_c_root = Hash.sha(c_root + b' ' + sign_c_root)         # -1
        c_root_auth = c_root + b' ' + sign_c_root + b' ' + hash_c_root

        return c_root_auth


class Charge():
    def __init__(self, ch_own, c_rx_list):
        self.ch_own = ch_own
        self.ID_god = ch_own.ID_own
        self.c_rx_list = c_rx_list
        self.ID_node = c_rx_list[G.P_ID_NODE]
        self.i_m = 0
        self.i_m_guide = 0
        self.coin_rest = 0
                
    async def charge(self):
        T.LOGGER.debug('')      

        # charge coin: -7
        self.coin_charge = G.COIN_CREDIT

        if not await init(self, G.CHARGE):
            return False
        if self.i_m <= self.i_m_guide:
            return self.i_ch_fetch # TODO: only consider this case now
        T.LOGGER.debug('init success')

        c = (
                b' '.join(self.c_rx_list[:G.P_HASH]) + b' ' +
                base58.b58encode_int(self.coin_charge) + b' ' +
                base58.b58encode_int(self.coin_rest) + b' ' +
                base58.b58encode_int(self.i_ch_m_pre) + b' ' +
                base58.b58encode_int(self.ch_own.i_ch_next) + b' ' +
                self.hash_pre
            )          
        sign_c = Ecc.sign(c, self.ch_own.pri_key)
        hash_c = Hash.sha(c + b' ' + sign_c)
        c_auth = c + b' ' + sign_c + b' ' + hash_c # to TX all card

        content_ack = (
                        base58.b58encode_int(self.coin_charge) + b' ' +
                        base58.b58encode_int(self.coin_rest) + b' ' +
                        base58.b58encode_int(self.i_ch_m_pre) + b' ' +
                        base58.b58encode_int(self.ch_own.i_ch_next) + b' ' +
                        self.hash_pre + b' ' +
                        sign_c + b' ' + 
                        hash_c    # to do, is it need to be TX
                      )
        c_ack_auth = ack_god(self.ch_own, content_ack, self.c_rx_list[G.P_HASH]) # to TX part card

        T.LOGGER.debug('c_auth success') 
        return c_auth

class Redeem:
    def __init__(self, ch_own, c_rx_list):
        self.ch_own = ch_own
        self.ID_god = ch_own.ID_own
        self.c_rx_list = c_rx_list

    async def init(self):
        T.LOGGER.debug('')

    async def redeem(self):
        T.LOGGER.debug('')

        if not await self.init():
            return False

        c = (
                b' '.join(self.c_rx_list[:G.P_HASH]) + b' ' +
                base58.b58encode_int(self.coin_charge) + b' ' +
                base58.b58encode_int(self.coin_rest) + b' ' +
                base58.b58encode_int(self.i_ch_m_pre) + b' ' +
                base58.b58encode_int(self.ch_own.i_ch_next) + b' ' +
                self.hash_pre
            )

        sign_c = Ecc.sign(c, self.ch_own.pri_key)
        hash_c = Hash.sha(c + b' ' + sign_c)
        c_auth = c + b' ' + sign_c + b' ' + hash_c

        # add pay card into chain and update guide
        await self.ch_own.append(c_auth)   

        return c_auth
     

class Post():
    def __init__(self, ch_own, c_rx_list):
        self.ch_own = ch_own
        self.ID_god = ch_own.ID_own
        self.c_rx_list = c_rx_list
        self.ID_node = c_rx_list[G.P_ID_NODE]
        self.i_m = 0
        self.i_m_guide = 0
        self.coin_rest = 0
    

    async def post(self):
        T.LOGGER.debug('')   

        if not await init(self, G.POST):
            return False
        if self.i_m <= self.i_m_guide:
            return self.i_ch_fetch # TODO: only consider this case now
        T.LOGGER.debug('init success') 

        c = (
                b' '.join(self.c_rx_list[:G.P_HASH]) + b' ' +
                base58.b58encode_int(self.coin_rest) + b' ' +
                base58.b58encode_int(self.i_ch_m_pre) + b' ' +
                base58.b58encode_int(self.ch_own.i_ch_next) + b' ' +
                self.hash_pre
            )
        sign_c = Ecc.sign(c, self.ch_own.pri_key)
        hash_c = Hash.sha(c + b' ' + sign_c)
        c_auth = c + b' ' + sign_c + b' ' + hash_c # to TX all card

        return c_auth


class Demand():
    def __init__(self, ch_own, c_rx_list):
        self.ch_own = ch_own
        self.ID_god = ch_own.ID_own
        self.c_rx_list = c_rx_list

class Ack():
    def __init__(self, ch_own, c_rx_list):
        self.ch_own = ch_own
        self.ID_god = ch_own.ID_own
        self.c_rx_list = c_rx_list

    async def init(self):
        T.LOGGER.debug('')

        return True

    async def ack(self):
        T.LOGGER.debug('')   

        if not await self.init():
            return False

        ID_earn = self.c_rx_list[G.P_ID_DEMAND]
        ID_pay = self.c_rx_list[G.P_ID_DEMANDED]
        i_m_pay = self.c_rx_list[G.P_I] # for ch_pay
        ch_pay = Chain(ID_pay, T.FO_CH)
        # fetch demand card
        c_fetch = await ch_pay.fetch_m(ID_earn, i_m_pay)
        # c_fetch_list = c_fetch.split()
        c = (G.ACK + b' ' +\
                base58.b58encode_int(int(time())) + b' ' +
                self.ID_ack + b' ' +
                self.c_rx_list[G.P_HASH] + b' ' +
                c_fetch)
        sign_c = Ecc.sign(c, self.ch_own.pri_key)
        hash_c = Hash.sha(c + b' ' + sign_c)
        c_auth = c + b' ' + sign_c + b' ' + hash_c

        return c_auth