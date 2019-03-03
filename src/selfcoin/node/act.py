import base58
from time import time
# from typing import Any, Dict, List, Optional
# from uuid import uuid4

from common.crypto import Ecc, Hash
from common.chain import Chain
from common import globall as G
from node.conf import tune as T
from node.comm import Udp

'''
the received card is checked hash and sign before
'''
async def init(self, ID_partner):
    T.LOGGER.debug('')

    row = await self.ch_own.get_guide(ID_partner)
    if row is None:
        T.LOGGER.error('partner ID is not add to table guide')
        return False
    
    if self.type == G.CHARGE or self.type == G.REDEEM:
        p_guide_m = T.P_GUIDE_M_CHRE
        p_guide_ch = T.P_GUIDE_CH_CHRE
    elif self.type == G.POST:
        p_guide_m = T.P_GUIDE_M_POST
        p_guide_ch = T.P_GUIDE_CH_POST
    elif self.type == G.PAY:
        p_guide_m = T.P_GUIDE_M_PAY
        p_guide_ch = T.P_GUIDE_CH_PAY
    elif self.type == G.EARN:
        p_guide_m = T.P_GUIDE_M_EARN
        p_guide_ch = T.P_GUIDE_CH_EARN  
    else:
        T.LOGGER.error('card type is not valid')
        return False

    # mutual index: 5
    self.i_m = (row[p_guide_m] + 1) % G.NUM_I_M
    # previous mutual chain index: -5
    self.i_ch_m_pre = row[p_guide_ch]

def init_ch(self):
    T.LOGGER.debug('')

    # remained coin: -6
    self.coin_rest = self.ch_own.coin_rest
    # if self.ch_own.c_last[G.P_TYPE] == G.CHARGE:
    #     self.coin_rest = (base58.b58decode_int(self.ch_own.c_last[G.P_COIN_REST]) + 
    #                         base58.b58decode_int(self.ch_own.c_last[G.P_COIN_CHRE])) 
    # elif self.ch_own.c_last[G.P_TYPE] == G.REDEEM:
    #     self.coin_rest = (base58.b58decode_int(self.ch_own.c_last[G.P_COIN_REST]) - 
    #                         base58.b58decode_int(self.ch_own.c_last[G.P_COIN_CHRE])) 
    # elif self.ch_own.c_last[G.P_TYPE] == G.PAY:
    #     self.coin_rest = (base58.b58decode_int(self.ch_own.c_last[G.P_COIN_REST]) - 
    #                         base58.b58decode_int(self.ch_own.c_last[G.P_COIN_TRADE]))
    # elif self.ch_own.c_last[G.P_TYPE] == G.EARN:
    #     self.coin_rest = (base58.b58decode_int(self.ch_own.c_last[G.P_COIN_REST]) +
    #                         base58.b58decode_int(self.ch_own.c_last[G.P_COIN_TRADE]))
    # else:
    #     self.coin_rest = base58.b58decode_int(self.ch_own.c_last[G.P_COIN_REST])
    
    # chain index: -4
    self.i_ch = self.ch_own.i_ch_next
    # previous hash: -3
    self.hash_pre = self.ch_own.c_last[G.P_HASH]


class Charge:
    def __init__(self, ID_god, ch_own, root=None):
        self.ID_charge = ch_own.ID_own
        self.ch_own = ch_own
        self.ID_god = ID_god
        self.root = root
        self.type = G.CHARGE

        # for charge root
        if self.root:
            self.i_m = 0
            self.coin_rest = 0
            self.i_ch_m_pre = 0
            self.i_ch = 0
            self.hash_pre = base58.b58encode_int(0)

    async def act_god(self, hash_content):
        T.LOGGER.debug('')
        
        if not self.root:
            await init(self, self.ID_god)
        
        c = (
                G.VER + b' ' +                               # 0
                base58.b58encode_int(int(time())) + b' ' +   # 1
                self.type + b' ' +                              # 2
                self.ID_god + b' ' +                         # 3
                self.ID_charge + b' ' +                      # 4                
                base58.b58encode_int(self.i_m) + b' ' +      # 5
                hash_content                                 # 6
            )

        sign_c = Ecc.sign(c, self.ch_own.pri_key)            # -2
        hash_c = Hash.sha(c + b' ' + sign_c)                 # -1

        c_auth = c + b' ' + sign_c + b' ' + hash_c
        T.LOGGER.debug(c_auth)
        return c_auth, hash_c
    
    def act_group(self, c_sign_god):
        T.LOGGER.debug('')

        if not self.root:
            init_ch(self)
        c_node = (
                    b' '.join(c_sign_god) + b' ' +                    # 
                    base58.b58encode_int(self.coin_rest) + b' ' +     # -6
                    base58.b58encode_int(self.i_ch_m_pre) + b' ' +    # -5
                    base58.b58encode_int(self.i_ch) + b' ' +          # -4
                    self.hash_pre                                     # -3
                 )
        T.LOGGER.debug('')
        sign_c_node = Ecc.sign(c_node, self.ch_own.pri_key)  # -2
        hash_c_node = Hash.sha(c_node + b' ' + sign_c_node)  # -1
        c_auth_node = c_node + b' ' + sign_c_node + b' ' + hash_c_node

        T.LOGGER.debug('complete')
        return c_auth_node


class Redeem:
    def __init__(self):
        pass


class Post:
    def __init__(self, ID_god, ch_own):
        self.ID_post = ch_own.ID_own
        self.ch_own = ch_own
        self.ID_god = ID_god
        self.type = G.POST

    async def act_god(self, hash_content):
        T.LOGGER.debug('')
                
        await init(self, self.ID_god)        
        c = (
                G.VER + b' ' +                               # 0
                base58.b58encode_int(int(time())) + b' ' +   # 1
                self.type + b' ' +                              # 2
                self.ID_god + b' ' +                         # 3
                self.ID_post + b' ' +                        # 4                
                base58.b58encode_int(self.i_m) + b' ' +      # 5
                hash_content                                 # 6
            )

        sign_c = Ecc.sign(c, self.ch_own.pri_key)            # -2
        hash_c = Hash.sha(c + b' ' + sign_c)                 # -1

        c_auth = c + b' ' + sign_c + b' ' + hash_c
        T.LOGGER.debug(c_auth)
        return c_auth, hash_c
    
    def act_group(self, c_sign_god):
        T.LOGGER.debug('')

        init_ch(self)
        c_node = (
                    b' '.join(c_sign_god) + b' ' +                    # 
                    base58.b58encode_int(self.coin_rest) + b' ' +     # -6
                    base58.b58encode_int(self.i_ch_m_pre) + b' ' +    # -5
                    base58.b58encode_int(self.i_ch) + b' ' +          # -4
                    self.hash_pre                                     # -3
                 )
        T.LOGGER.debug('')
        sign_c_node = Ecc.sign(c_node, self.ch_own.pri_key)  # -2
        hash_c_node = Hash.sha(c_node + b' ' + sign_c_node)  # -1
        c_auth_node = c_node + b' ' + sign_c_node + b' ' + hash_c_node

        T.LOGGER.debug('complete')
        return c_auth_node

class Pay:
    def __init__(self, ID_earn, ch_own):
        self.ID_earn = ID_earn
        self.ID_pay = ch_own.ID_own
        self.ch_own = ch_own
        self.type = G.PAY

    async def init(self):
        # coin_rest: -6
        if self.ch_own.c_last[G.P_ID_PAY] == self.ID_pay:
            coin_rest = (base58.b58decode_int(self.ch_own.c_last[G.P_COIN_REST]) -   
                            base58.b58decode_int(self.ch_own.c_last[G.P_COIN_TRADE]) )
        else:
            coin_rest = (base58.b58decode_int(self.ch_own.c_last[G.P_COIN_REST]) +   
                            base58.b58decode_int(self.ch_own.c_last[G.P_COIN_TRADE]) )
        self.coin_rest = coin_rest

        # mutual index and previous partner chain index: 5 and -5
        row = await self.ch_own.get_guide(self.ID_earn)        
        if row:
            ID_earn, i_m_pay, i_ch_pay, i_m_earn, i_ch_earn = row
            i_m_pay_next = base58.b58encode_int((base58.b58decode_int(i_m_pay) + 1) % G.NUM_I_M)
            # i_m_earn_next = base58.b58encode_int((base58.b58decode_int(i_m_earn) + 1) % G.NUM_I_M)
        else:
            # create DB row when ID doesn't exist, start from 1
            await self.ch_own.set_guide(self.ID_earn)
            i_ch_pay = base58.b58encode_int(0)
            i_m_pay_next = base58.b58encode_int(1)
            
        self.i_ch_pay_pre = i_ch_pay
        self.i_m_pay = i_m_pay_next
        
        # pay chain index: -4
        if self.ch_own.i_l == G.NUM_L_BODY -1:
            i_f = self.ch_own.i_f + 1
            i_l = 0
        else:
            i_f = self.ch_own.i_f
            i_l = self.ch_own.i_l + 1
        self.i_ch = base58.b58encode_int(i_f * G.NUM_L_BODY + i_l)

        # previous hash: -3
        self.hash_pre = self.ch_own.c_last[G.P_HASH]

    async def pay(self, coin_pay):
        T.LOGGER.debug('')

        await self.init()                
        c = (G.VER + b' ' +                                  # 0
                base58.b58encode_int(int(time())) + b' ' +   # 1
                self.type + b' ' +                           # 2
                self.ID_pay + b' ' +                         # 3
                self.ID_earn + b' ' +                        # 4
                self.i_m_pay + b' ' +                        # 5
                coin_pay + b' ' +                            # 6
                self.coin_rest + b' ' +                      # -6
                self.i_ch_pay_pre + b' ' +                   # -5
                self.i_ch + b' ' +                           # -4
                self.hash_pre                                # -3
            )

        sign_c = Ecc.sign(c, self.ch_own.pri_key_own)        # -2
        hash_c = Hash.sha(c + b' ' + sign_c)                 # -1

        c_auth = c + b' ' + sign_c + b' ' + hash_c
        return c_auth, hash_c


class Earn:
    def __init__(self, ID_pay, ch_own):
        self.ID_earn = ch_own.ID_own
        self.ID_pay = ID_pay
        self.ch_own = ch_own

    async def init(self):
        # coin_rest: -6
        if self.ch_own.c_last[G.P_ID_PAY] == self.ID_earn:
            coin_rest = (base58.b58decode_int(self.ch_own.c_last[G.P_COIN_REST]) -   
                            base58.b58decode_int(self.ch_own.c_last[G.P_COIN_TRADE]) )
        else:
            coin_rest = (base58.b58decode_int(self.ch_own.c_last[G.P_COIN_REST]) +   
                            base58.b58decode_int(self.ch_own.c_last[G.P_COIN_TRADE]) )
        self.coin_rest = coin_rest

        # mutual index and previous partner chain index: 5 and -5
        row = await self.ch_own.get_guide(self.ID_pay)        
        if row:
            ID_pay, i_m_pay, i_ch_pay, i_m_earn, i_ch_earn = row
            # i_m_pay_next = base58.b58encode_int((base58.b58decode_int(i_m_pay) + 1) % G.NUM_I_M)
            i_m_earn_next = base58.b58encode_int((base58.b58decode_int(i_m_earn) + 1) % G.NUM_I_M)
        else:
            # create DB row when ID doesn't exist, start from 1
            await self.ch_own.set_guide(self.ID_pay)
            i_ch_earn = base58.b58encode_int(0)
            i_m_earn_next = base58.b58encode_int(1)
        self.i_ch_earn_pre = i_ch_earn
        self.i_m_earn = i_m_earn_next

        # pay chain index: -4
        if self.ch_own.i_l == G.NUM_L_BODY -1:
            i_f = self.ch_own.i_f + 1
            i_l = 0
        else:
            i_f = self.ch_own.i_f
            i_l = self.ch_own.i_l + 1
        self.i_ch = base58.b58encode_int(i_f * G.NUM_L_BODY + i_l)

        # previous hash: -3
        self.hash_pre = self.ch_own.c_last[G.P_HASH]


    async def demand(self):
        T.LOGGER.debug('')

        await self.init()

        type_c = G.DEMAND
        c = G.VER + b' ' +\
                base58.b58encode_int(int(time())) + b' ' +\
                type_c + b' ' +\
                self.ID_earn + b' ' +\
                self.ID_pay + b' ' +\
                self.i_m_earn
                
                
        sign_c = Ecc.sign(c, self.ch_own.pri_key_own)
        hash_c = Hash.sha(c + b' ' + sign_c)        
        c_auth = c + b' ' + sign_c + b' ' + hash_c               
        return c_auth, hash_c

    def earn(self, c_pay):
        T.LOGGER.debug('')

        # check the version
        if c_pay[G.P_VER] == G.VER:                              # 0
            # check the sign
            if not Ecc.verify(c_pay, c_pay[G.P_ID_PAY]):  # -2
                T.LOGGER.error('Sign of the close pay card is wrong.')
                return False
            # check the mutual part, ignore others for quick trade, leave for watch
            # trade coin: 6 is leaved for ui to check
            if (c_pay[G.P_TYPE] == G.PAY and                    # 2
                    c_pay[G.P_ID_PAY] == self.ID_pay and              # 3
                    c_pay[G.P_ID_EARN] == self.ID_earn and            # 4
                    c_pay[G.P_I_M] == self.i_m_earn ):                # 5

                c_pay[G.P_TYPE] = G.EARN
                c = (b' '.join(c_pay) + b' ' +
                        self.coin_rest + b' ' +                      # -6
                        self.i_ch_earn_pre + b' ' +                  # -5
                        self.i_ch + b' ' +                           # -4
                        self.hash_pre                                # -3
                    )
                        
                sign_c = Ecc.sign(c, self.ch_own.pri_key_own)        # -2
                hash_c = Hash.sha(c + b' ' + sign_c)                 # -1
                c_auth = c + b' ' + sign_c + b' ' + hash_c 
                return c_auth, hash_c




class Watch:
    def __init__(self):
        pass

    def watch_tx(self):
        pass

    def watch_rx(self):
        pass

    def watch(self):
        pass













    # @property
    # def last_block(self) -> Dict[str, Any]:
    #     return self.chain[-1]

    # @staticmethod
    # def hash(block: Dict[str, Any]) -> str:
    #     """
    #     生成块的 SHA-256 hash值

    #     :param block: Block
    #     """

    #     # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
    #     block_string = json.dumps(block, sort_keys=True).encode()
    #     return hashlib.sha256(block_string).hexdigest()



