import multiprocessing
import sys
import asyncio


from aid.conf import tune as T
from common import globall as G
from aid.act import Ack
from aid.comm import UdpServerProtocol


async def main(addr):
    print("Starting UDP server")

    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    # One protocol instance will be created to serve all
    # client requests.
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UdpServerProtocol(),
        local_addr = addr)

    try:
        await asyncio.sleep(2**32-1)  # Serve for 100+ years.        
    finally:
        transport.close()

    # loop.run_forever()
    # loop.close()


def process_work(addr):
    T.LOGGER.debug(sys._getframe().f_code.co_name)
    asyncio.run(main(addr))

if __name__ == "__main__":
    T.LOGGER.debug(sys._getframe().f_code.co_name)

    num_cpu = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes = num_cpu)
    
    # # asyncio.run(main(G.TRADE_SERVER_ADDR))
    # pool.apply_async(asyncio.run, (main(G.TRADE_SERVER_ADDR, Trade),))
    # pool.apply_async(asyncio.run, (main(G.WATCH_SERVER_ADDR, Watch),))
    
    # asyncio.run(main(G.TRADE_SERVER_ADDR))
    for i in range(num_cpu):
        pool.apply_async(process_work, (T.ADDR_TEST,))


    pool.close()
    pool.join()


