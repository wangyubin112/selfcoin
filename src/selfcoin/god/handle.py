import asyncio

from common import globall as G
from god.conf import tune as T
from common.crypto import Hash, Ecc
from god.act import Root, Charge, Redeem, Post, Ack

def root(ch_own):
    T.LOGGER.debug('')

    root = Root(ch_own)
    return root.root()


async def update_god(act, c_last):
    T.LOGGER.debug('')

    if not await act.ch_own.set_guide(act.ID_god, act.ch_own.i_ch_next):
        T.LOGGER.debug('chain set_guide god false')
        return False

    if not await act.ch_own.append(c_last):
        T.LOGGER.debug('chain append false')
        return False
    T.LOGGER.debug('chain append success')

    if not act.ch_own.update(c_last.split()):
        T.LOGGER.debug('chain update false')
        return False
    T.LOGGER.debug('chain update success')

    return True


async def handle(self, c_list):
    T.LOGGER.debug('')

    if c_list[G.P_TYPE] == G.CHARGE:
        return await charge(self, c_list)
    elif c_list[G.P_TYPE] == G.REDEEM:
        return await redeem(self, c_list)
    elif c_list[G.P_TYPE] == G.POST:
        return await post(self, c_list)
    elif c_list[G.P_TYPE] == G.DEMAND:
        return await ack(self, c_list)
    else:
        T.LOGGER.error(b'There should not be card type: ' + c_list[G.P_TYPE])
        return

async def charge(self, c_list):
    T.LOGGER.debug('')

    charge = Charge(self.ch_own, c_list)
    c_auth = await charge.charge()

    # update node info: charge
    if not await charge.ch_own.set_guide(charge.ID_node, 0, i_m_2=charge.i_m,
                                                        i_ch_2=charge.ch_own.i_ch_next):
        T.LOGGER.debug('chain set_guide node false')
        return False
    # update god info
    if not await update_god(charge, c_auth):
        T.LOGGER.debug('update god false')
        return False

    return c_auth


async def redeem(self, c_list):
    T.LOGGER.debug('')

    redeem = Redeem(self.ch_own, c_list)
    c_auth = redeem.redeem()


async def post(self, c_list):
    T.LOGGER.debug('')

    post = Post(self.ch_own, c_list)
    c_auth = await post.post()

    if type(c_auth) is int:
        i_ch_fetch = c_auth
        i_f = i_ch_fetch//G.NUM_L_BODY
        i_l = i_ch_fetch% G.NUM_L_BODY
        c_fetch = await post.ch_own.fetch_ch(i_f, i_l)
        if not c_fetch:
            T.LOGGER.debug('chain fetch nothing')
            return False
        return c_fetch

    # update node info: post
    if not await post.ch_own.set_guide(post.ID_node, 0, i_m_1=post.i_m,
                                                        i_ch_1=post.ch_own.i_ch_next):
        T.LOGGER.debug('chain set_guide node false')
        return False
    # update god info
    if not await update_god(post, c_auth):
        T.LOGGER.debug('update god false')
        return False

    return c_auth


async def ack(self, c_list):
    T.LOGGER.debug('')

    