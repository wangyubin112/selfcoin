import multiprocessing
import asyncio
import aiosqlite
import base58
import sys
import os
from time import time

from god.conf import tune as T
from common import globall as G
from god.act import Ack
from god.comm import UdpServerProtocol
from common.crypto import Ecc, Hash
from common.chain import Chain
from god import handle

async def init():
    T.LOGGER.debug('')

    ID_own = None
    # load key
    try:
        c_root_auth = None
        async with aiosqlite.connect(T.PATH_CREDIT) as db:
            await db.execute('create table if not exists \
                                table_own(name nchar({0}) primary key, \
                                        id char({1}) unique, \
                                        pri_key char({2}), \
                                        pub_key_x char({2}), \
                                        pub_key_y char({2}))'. 
                                format(G.LEN_NAME, G.LEN_ID, G.LEN_KEY))
            async with db.execute('select * from table_own where name=?', (G.NAME_GOD,)) as cursor:
                async for row in cursor:
                    ID_own = row[T.P_OWN_ID]
                    T.LOGGER.debug(b'select: ' + ID_own)
                    pri_key = base58.b58decode_int(row[T.P_OWN_PRI])
                    pub_key_x = base58.b58decode_int(row[T.P_OWN_PUB_X])
                    pub_key_y = base58.b58decode_int(row[T.P_OWN_PUB_Y])
                    ch_own = Chain(T.FO_CH, ID_own, pri_key, pub_key_x, pub_key_y)
                    
            # no record, create root card
            if ID_own is None:          
                ID_own, pri_key, pub_key_x, pub_key_y = Ecc.generate()
                T.LOGGER.debug(b'create: ' + ID_own)
                pri_key_b58 = base58.b58encode_int(pri_key)
                pub_key_x_b58 = base58.b58encode_int(pub_key_x)
                pub_key_y_b58 = base58.b58encode_int(pub_key_y)
                
                await db.execute('insert into table_own values(?,?,?,?,?)',
                                    (G.NAME_GOD, ID_own, pri_key_b58, pub_key_x_b58, pub_key_y_b58))
                await db.commit()

                ch_own = Chain(T.FO_CH, ID_own, pri_key, pub_key_x, pub_key_y)
                c_root_auth = handle.root(ch_own)

        #  own chain
        if not await ch_own.init(c_root_auth):
            return False
        return ch_own
        
    except Exception as e:
        T.LOGGER.warning(e)
        return False


async def main(ch_own):
    T.LOGGER.debug('Starting UDP server')

    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    # One protocol instance will be created to serve all
    # client requests.
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UdpServerProtocol(loop, ch_own),
        local_addr = T.ADDR_GOD)

    try:
        await asyncio.sleep(2**32-1)  # Serve for 100+ years.        
    finally:
        transport.close()

    # loop.run_forever()
    # loop.close()


def process_work(ch_own):
    T.LOGGER.debug('')
    asyncio.run(main(ch_own))

def init_work():
    T.LOGGER.debug('')
    asyncio.run(init())
    # print('2')

if __name__ == "__main__":
    T.LOGGER.debug('')

    # pool_init = multiprocessing.Pool(processes = 1)
    # pool_init.apply_async(init_work)
    # pool_init.close()
    # pool_init.join()

    # init_work()
    ch_own = asyncio.run(init())
    
    if ch_own:
        T.LOGGER.debug(ch_own)
        
        num_cpu = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes = num_cpu)
        
        # # asyncio.run(main(G.TRADE_SERVER_ADDR))
        # pool.apply_async(asyncio.run, (main(G.TRADE_SERVER_ADDR, Trade),))
        # pool.apply_async(asyncio.run, (main(G.WATCH_SERVER_ADDR, Watch),))
        
        # asyncio.run(main(G.TRADE_SERVER_ADDR))
        for i in range(num_cpu):
            pool.apply_async(process_work, (ch_own,))


        pool.close()
        pool.join()
    else:
        T.LOGGER.error('')
        sys.exit(1) # to do: can not exit
        # os._exit()
        # exit()

