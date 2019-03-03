import asyncio
import base58
from time import time
import aiosqlite

from common.chain import Chain
from node.act import Earn, Pay, Post, Watch, Charge, Redeem
from node.conf import tune as T
from common import globall as G
from node.comm import UdpClientProtocol, UdpGroupProtocol, tx_rx, tx, rx
from common.crypto import Ecc, Hash

async def regist(cls_App, name, hash_ID_real, row_god):
    '''
    init the root card 
    row_god is in credit_DB.free_table: name, ID, credit
    '''
    T.LOGGER.debug('')

    ID_god = row_god[T.P_FREE_ID]
    ID, pri_key, pub_key_x, pub_key_y = Ecc.generate()
    pri_key_b58 = base58.b58encode_int(pri_key)
    pub_key_x_b58 = base58.b58encode_int(pub_key_x)
    pub_key_y_b58 = base58.b58encode_int(pub_key_y)

    # create init root card to chain
    ch_own = Chain(T.FO_CH, ID, pri_key, pub_key_x, pub_key_y)
    cls_App.ch_own = ch_own

    if not await charge(cls_App, ID_god, hash_ID_real, root=1):
        return False

    # add ID to table_own. to do: check the ID conflict
    try:
        async with aiosqlite.connect(T.PATH_CREDIT) as db:
            await db.execute('create table if not exists \
                                table_own(name nchar({0}) primary key, \
                                        id char({1}) unique, \
                                        pri_key char({2}), \
                                        pub_key_x char({2}), \
                                        pub_key_y char({2}))'. 
                                format(G.LEN_NAME, G.LEN_ID, G.LEN_KEY))

            await db.execute('insert into table_own values(?,?,?,?,?)',
                                (name, ID, pri_key_b58, pub_key_x_b58, pub_key_y_b58))
            await db.commit()
    except Exception as e:
        T.LOGGER.warning(e)
        return False

    return True


async def login(cls_App, row_own):
    T.LOGGER.debug('')

    ID_own = row_own[T.P_OWN_ID]
    pri_key = base58.b58decode_int(row_own[T.P_OWN_PRI])
    pub_key_x = base58.b58decode_int(row_own[T.P_OWN_PUB_X])
    pub_key_y = base58.b58decode_int(row_own[T.P_OWN_PUB_Y])

    # own chain
    cls_App.ch_own = Chain(T.FO_CH, ID_own, pri_key, pub_key_x, pub_key_y)
    if not await cls_App.ch_own.init():
        return False

    # init DB_credit
    async with aiosqlite.connect(T.PATH_CREDIT) as db:
        await db.execute('create table if not exists \
                            table_restrict(id char({0}) primary key, \
                                        credit integer)'.
                            format(G.LEN_ID))

        # await db.commit() # to do: see if needed after create table
    
    return True  

async def charge(cls_App, ID_god, hash_content, root=None):
    T.LOGGER.debug('')

    charge = Charge(ID_god, cls_App.ch_own, root)
    if not await act2god(cls_App, charge, hash_content, root):
        return False

    return True


async def post(cls_App, ID_god, hash_content):
    T.LOGGER.debug('')

    post = Post(ID_god, cls_App.ch_own)
    if not await act2god(cls_App, post, hash_content):
        return False

    return True


async def act2god(cls_App, act, hash_content, root=None):
    T.LOGGER.debug('')
    
    # charge to god card    
    c_auth, hash_c = await act.act_god(hash_content)

    # TX and get RX with God
    c_rx_god = await tx_rx(cls_App, c_auth, hash_c)
    if not c_rx_god:
        T.LOGGER.warning('card act to god fail')
        return False

    # check c_rx_content
    c_auth_list = c_auth.split()
    if c_rx_god[:G.P_COIN_CHRE] != c_auth_list[:G.P_HASH]:
        T.LOGGER.error('not the corresponding charge card')
        return False
        
    # TODO: for now only consider the charge root
    if root and act.type == G.CHARGE:
        if c_rx_god[G.P_COIN_CHRE] != base58.b58encode_int(G.COIN_CREDIT):
            T.LOGGER.error('god coin credit is wrong')
            return False

    # charge card to broadcast
    c_auth_node = act.act_group(c_rx_god)

    T.LOGGER.debug('ready for add to chain and update guide')
    # add card to chain and update guide
    if root and act.type == G.CHARGE: # init root card
        if not await cls_App.ch_own.init(c_auth_node):
            return False
    else:
        if not await cls_App.ch_own.append(c_auth_node):
            return False
        
        if not await cls_App.ch_own.set_guide(cls_App.ch_own.ID_own, act.i_ch):
            T.LOGGER.error('set guide ID_own fails')
            return False
        cls_App.ch_own.update(c_auth_node.split())

    if act.type == G.CHARGE or act.type == G.REDEEM:
        if not await cls_App.ch_own.set_guide(act.ID_god, base58.b58decode_int(c_rx_god[G.P_I_CH]), i_m_2=act.i_m,
                                                            i_ch_2=act.i_ch):
            T.LOGGER.error('set guide ID_god fails')
            return False
    elif act.type == G.POST:
        if not await cls_App.ch_own.set_guide(act.ID_god, base58.b58decode_int(c_rx_god[G.P_I_CH]), i_m_1=act.i_m,
                                                            i_ch_1=act.i_ch):
            T.LOGGER.error('set guide ID_god fails')
            return False
    else:
        T.LOGGER.error('act type not valid')
        return False
    
    # broadcast to network
    if not await tx(cls_App, c_auth_node):
        T.LOGGER.warning('card charge to network fail')
        return False

    return True



async def pay(cls_App, ID_earn, coin):
    T.LOGGER.debug('')

    pay = Pay(ID_earn, cls_App.ch_own)
    if not await act2node(cls_App, pay, coin):
        return False

    return True

async def earn(cls_App, ID_pay, coin):
    T.LOGGER.debug('')



async def act2node(cls_App, act, coin):
    T.LOGGER.debug('')

    # pay act
    c_auth, hash_c = act.pay(coin_pay)
    # pay TX to Aid and get ACK
    transport, protocol = await cls_App.loop.create_datagram_endpoint(
                lambda: UdpClientProtocol(cls_App.loop, c_auth, hash_c),
                remote_addr=T.ADDR_AID)
    
    T.LOGGER.debug(protocol.c_rx_list)

    c_rx_content = protocol.c_rx_list[G.P_CONTENT:G.P_SIGN]
    # if fail
    
    # add the pay card to chain and update guide


async def pay_defer(cls_App, ID_earn, coin_pay):
    T.LOGGER.debug('')

    # pay act
    pay = Pay(ID_earn, cls_App.ch_own)
    c_auth, hash_c = pay.pay(coin_pay)
    # pay TX to Aid and get ACK
    transport, protocol = await cls_App.loop.create_datagram_endpoint(
                lambda: UdpClientProtocol(cls_App.loop, c_auth, hash_c),
                remote_addr=T.ADDR_AID)
    
    T.LOGGER.debug(protocol.c_rx_list)

    c_rx_content = protocol.c_rx_list[G.P_CONTENT:G.P_SIGN]
    # if fail
    
    # add the pay card to chain and update guide

async def earn_defer(cls_App, ID_pay):
    T.LOGGER.debug('')

    # earn act
    earn = Earn(ID_pay, cls_App.ch_own)

    # demand
    c_auth_demand, hash_c_demand = earn.demand()
    # TX and get RX
    transport, protocol = await cls_App.loop.create_datagram_endpoint(
                lambda: UdpClientProtocol(cls_App.loop, c_auth_demand, hash_c_demand),
                remote_addr=T.ADDR_AID)
    
    if protocol.c_rx_list == None:
        T.LOGGER.debug('earn demand fail, click to reset')
        return False
    c_rx_content = protocol.c_rx_list[G.P_CONTENT:G.P_SIGN]
    
    # earn
    cls_App.earn_status.set('earn close processing')
    c_auth_earn, hash_c_earn = earn.earn(c_rx_content)
    # TX and get ACK
    transport, protocol = await cls_App.loop.create_datagram_endpoint(
                lambda: UdpClientProtocol(cls_App.loop, c_auth_earn, hash_c_earn),
                remote_addr=T.ADDR_AID)
    
    if protocol.c_rx_list == None:
        T.LOGGER.debug('earn close fail, click to reset')
        return False
    c_rx_content = protocol.c_rx_list[G.P_CONTENT:G.P_SIGN]
    if c_rx_content == b'0':
        T.LOGGER.debug.set('earn close success')
        return True
    else:
        T.LOGGER.debug.set('earn close fail, click to reset')
        return False

    # add the earn card to chain and update guide





async def act2aid():
    T.LOGGER.debug('')
