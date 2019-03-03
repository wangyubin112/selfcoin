from time import time
import base58

from common.chain import Chain
from common import globall as G
from aid.conf import tune as T
from common.crypto import Ecc, Hash


class Ack():
    def __init__(self, ID_ack, c_list):
        self.ID_ack = ID_ack
        self.c_list = c_list
        
    async def run(self):
        if self.c_list[G.P_TYPE] == G.DEMAND:
            ID_earn = self.c_list[G.P_ID_DEMAND]
            ID_pay = self.c_list[G.P_ID_DEMANDED]
            i_m_pay = self.c_list[G.P_I] # for ch_pay
            ch_pay = Chain(ID_pay, T.FO_CH)
            # fetch demand card
            c_fetch = await ch_pay.fetch_m(ID_earn, i_m_pay)
            # c_fetch_list = c_fetch.split()
            c_ack = G.ACK + b' ' +\
                    base58.b58encode_int(int(time())) + b' ' +\
                    self.ID_ack + b' ' +\
                    self.c_list[G.P_HASH] + b' ' +\
                    c_fetch

        elif self.c_list[G.P_TYPE] == G.PAY:
            ID_pay = self.c_list[G.P_ID_PAY]
            ch_pay = Chain(ID_pay, T.FO_CH)
            # add pay card into chain and update guide
            await ch_pay.append(self.c_list)
            
            c_ack = G.ACK + b' ' +\
                   base58.b58encode_int(int(time())) + b' ' +\
                   self.ID_ack + b' ' +\
                   self.c_list[G.P_HASH]

        elif self.c_list[G.P_TYPE] == G.EARN:
            ID_earn = self.c_list[G.P_ID_EARN]
            ch_earn = Chain(ID_earn, T.FO_CH)
            # add earn card into chain and update guide
            await ch_earn.append(self.c_list)

            c_ack = G.ACK + b' ' +\
                   base58.b58encode_int(int(time())) + b' ' +\
                   self.ID_ack + b' ' +\
                   self.c_list[G.P_HASH]
        elif self.c_list[G.P_TYPE] == G.WATCH:
            pass
        elif self.c_list[G.P_TYPE] == G.POST:
            pass
        else:
            T.LOGGER.error(b'There should not be c_type: ' + self.c_list[G.P_TYPE])
            return False

        c_ack_sign = Ecc.sign(c_ack)
        c_ack_hash = Hash.sha(c_ack + b' ' + c_ack_sign)
        c_ack_auth = c_ack + b' ' + c_ack_sign + b' ' + c_ack_hash

        return c_ack_auth



