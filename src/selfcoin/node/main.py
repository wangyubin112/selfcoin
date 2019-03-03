import os
import time
import base58
from tkinter import *
import asyncio
import aiofiles
import aiosqlite

from node.ui.ui import Ui
from common import globall as G
from common.crypto import Ecc, Hash
from node.credit import Credit
from node.comm import UdpClientProtocol
from common.chain import Chain
from node.conf import tune as T
from node import handle

class App(Ui):
    def __init__(self, loop, interval, master=None):
        self.ch_own = None

        Ui.__init__(self, master)
        self.loop = loop
        self.tasks = []
        self.updater(interval)

    def updater(self, interval): # to do: do not know the operation mechanism
        self.update()
        self.loop.call_later(interval, self.updater, interval)

    def handler(self, task):
        self.tasks.append(self.loop.create_task(task()))

    #################################### for show ###############################
    async def add(self):
        T.LOGGER.debug('')

        name = self.show_name_add_entry.get()
        ID = self.show_ID_add_entry.get()
        credit = self.show_credit_add_combobox.get()
        if credit == 'friend':
            credit_int = 0
        else:
            credit_int = 1 # partner

        if await Credit.add(T.TA_FREE, name.encode(), ID.encode(), credit_int):
            self.show_add_status.set('add success, go on')
        else:
            self.show_add_status.set('add fail, retry')

    async def search(self):
        T.LOGGER.debug('')

        name = self.show_name_entry.get()


    #################################### for access ###############################
    async def regist(self):
        T.LOGGER.debug('')

        name_str = self.regist_name_entry.get()
        ID_real_str = self.regist_ID_real_entry.get()
        if (not name_str) or (not ID_real_str):
            self.regist_status.set('input name/ID, retry')
            return
        
        row_god = await Credit.search(T.TA_FREE, G.NAME_GOD)
        if not row_god:
            self.regist_status.set('god is not added')
            return

        name = name_str.encode()
        hash_ID_real = Hash.sha(ID_real_str.encode())

        if not await handle.regist(self, name, hash_ID_real, row_god):
            self.regist_status.set('regist fail, retry')
            return                             
                
        self.regist_button.configure(state = 'disable')
        self.login_button.configure(state = 'active')
        self.regist_status.set('regist success')

    async def login(self):
        T.LOGGER.debug('')
        
        name_str = self.login_entry.get()
        if not name_str:
            self.login_status.set('input name and try')
            return
        name = name_str.encode()

        row_own = await Credit.search(T.TA_OWN, name)
        if not row_own:
            self.login_status.set('{} not regist, retry'.format(name_str))
            return

        row_god = await Credit.search(T.TA_FREE, G.NAME_GOD)
        if not row_god:
            self.login_status.set('God not regist, retry')
            return
        self.ID_god = row_god[T.P_FREE_ID]
        
        if not await handle.login(self, row_own):
            self.login_status.set('login fail, retry')
            return

        # ui access        
        self.login_button.configure(state = 'disable')
        self.login_entry.configure(state = 'disable')
        self.regist_button.configure(state = 'disable')
        self.logout_button.configure(state = 'active')

        # ui show
        self.show_own_name_status.set(name_str)
        self.show_own_ID_status.set(row_own[T.P_OWN_ID])
        self.show_own_coin_status.set(self.ch_own.coin_rest)
        T.LOGGER.debug('show success')

        # post
        self.post_imme_button.configure(state = 'active')
        self.post_demand_button.configure(state = 'active')

        # charge
        self.charge_imme_button.configure(state = 'active')
        self.charge_demand_button.configure(state = 'active')

        # trade
        self.earn_imme_button.configure(state = 'active')
        self.pay_imme_button.configure(state = 'active')
        
        
        # watch
        self.watch_button.configure(state = 'active')
        self.watch_demand_button.configure(state = 'active')

        self.login_status.set('login success')

    def logout(self):
        '''
        To do: need to kill all related threads, 
               maybe there is nothing need to do.
        '''
        T.LOGGER.debug('')

        self.regist_button.configure(state = 'active')
        self.login_button.configure(state = 'active')
        self.logout_button.configure(state = 'disable')
        
        self.logout_status.set('logout success')

    #################################### for Post imme #########################################
    async def post_imme(self):
        T.LOGGER.debug('')

        hash_content_str = self.post_entry.get()
        if not hash_content_str:
            self.regist_status.set('input hash content, retry')
            return
        
        hash_content = hash_content_str.encode()

        if not await handle.post(self, self.ID_god, hash_content):
            self.post_imme_status.set('post_imme fail, retry')
            return
        self.post_imme_status.set('post_imme success, go on')

    #################################### for Charge imme #########################################
    async def charge_imme(self):
        T.LOGGER.debug('')

    #################################### for Trade imme ###############################
    async def pay_imme(self):
        T.LOGGER.debug('')

        name_earn_str = self.pay_name_earn_entry.get()
        coin_pay_str = self.pay_coin_entry.get()
        if (not name_earn_str) or (not coin_pay_str):
            self.pay_imme_status.set('input name/coin, retry')
            return
        
        name_earn = name_earn_str.encode()
        row_earn = await Credit.search(T.TA_FREE, name_earn)
        if not row_earn:
            self.pay_imme_status.set('{} not regist or blacklist, retry'.format(name_earn_str))
            return

        coin_pay = int(coin_pay_str)
        if coin_pay <= 0:
            self.pay_imme_status.set('coin must more than 0, retry')
            return        

        if not await handle.pay(self, self.ID_god, coin_pay):
            self.pay_imme_status.set('pay_imme fail, retry')
            return

        self.pay_imme_status.set('pay_imme success, go on')


    async def earn_imme(self):
        T.LOGGER.debug('')

        name_pay_str = self.pay_name_earn_entry.get()
        coin_earn_str = self.pay_coin_entry.get()
        if (not name_earn_str) or (not coin_earn_str):
            self.earn_imme_status.set('input name/coin, retry')
            return
        
        name_pay = name_pay_str.encode()
        row_pay = await Credit.search(T.TA_FREE, name_pay)
        if not row_pay:
            self.earn_imme_status.set('{} not regist or blacklist, retry'.format(name_pay_str))
            return

        coin_earn = int(coin_earn_str)
        if coin_earn <= 0:
            self.earn_imme_status.set('coin must more than 0, retry')
            return        

        if not await handle.earn(self, self.ID_god, coin_earn):
            self.earn_imme_status.set('earn_imme fail, retry')
            return
            
        self.earn_imme_status.set('earn_imme success, go on')

    #################################### for Trade defer ###############################
    async def pay_defer(self):
        T.LOGGER.debug('')
        
        name_earn = self.pay_name_earn_entry.get()
        coin_pay = self.pay_coin_entry.get().encode()
        if (not name_earn) or (not coin_pay):
            self.pay_status.set('input name/coin, retry')
            return
        ID_earn = Credit.search(T.TA_FREE, name_earn)
        if not ID_earn:
            self.pay_status.set('earn is not partner/friend, retry')
            return
        self.pay_status.set('pay processing')
        
        if await handle.pay_defer(self, ID_earn, coin_pay):
            self.pay_status.set('pay success')
        else:
            self.pay_status.set('pay fail, retry')

    async def earn_defer(self):
        T.LOGGER.debug('')

        name_pay = self.earn_name_pay_entry.get()
        if not name_pay:
            self.earn_status.set('input name, retry')
            return
        ID_pay = Credit.search(T.TA_FREE, name_pay)
        if not ID_pay:
            self.earn_status.set('pay is not partner/friend, retry')
            return
        self.earn_status.set('earn processing')

        if await handle.earn_defer(self, ID_pay):
            self.earn_status.set('earn success')
        else:
            self.earn_status.set('earn fail, retry')







    async def post_launch(self):
        # self.tasks.append(loop.create_task(self.test()))
        pass

    async def launch(self):
        if self.earn_launch_button['text'] in {'payer is not partner, click to reset',\
                                        'fail, click to reset'}:
            self.earn_launch_status.set('earn launch')
            self.earn_entry_0.delete(0,END)
            self.earn_entry_1.delete(0,END)
            return
        if self.earn_launch_button['text'] == 'earn launch':
            payer = self.earn_entry_0.get().encode()
            pay_ID = Partner.search(payer)
            if not pay_ID:
                self.earn_launch_status.set('payer is not partner, click to reset')
                return
            self.earn_launch_status.set('earn launch processing')

            
            reward_coin_bytes = self.earn_entry_1.get().encode()
            # Trade instantiation
            self.trade = act.Trade(G0.OWN_ID, pay_ID, reward_coin_bytes)
            self.trade.earn_launch()







    
    async def watch_trade(self):        
        # One protocol instance will be created to serve all
        # client requests.
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: UdpWatchProtocol(),
            local_addr=T.ADDR_GROUP)

    async def watch_post(self):        
        # One protocol instance will be created to serve all
        # client requests.
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: UdpWatchProtocol(),
            local_addr=T.ADDR_GROUP)


    async def test(self):
        i = 100000
        while True:
            i += 1
            print(i)
            await asyncio.sleep(1)

    async def test1(self):
        i = 0
        while True:
            i += 1
            print(i)
            await asyncio.sleep(1)
    

    def alarm(self, info):
        while True:
            time.sleep(1)
            print(info)



if __name__ == "__main__":
    # for the ui
    top = Tk()
    # App(top).mainloop()
    
    interval = .02
    loop = asyncio.get_event_loop()
    # loop = asyncio.get_running_loop() # preferred
    app = App(loop,interval, top)
    loop.run_forever()
    loop.close()




    # # Get a reference to the event loop as we plan to use
    # # low-level APIs.
    # loop = asyncio.get_running_loop()

    # # One protocol instance will be created to serve all
    # # client requests.
    # transport, protocol = await loop.create_datagram_endpoint(
    #     lambda: UdpServerProtocol(act),
    #     local_addr = addr)

    # try:
    #     await asyncio.sleep(2**32-1)  # Serve for 100+ years.        
    # finally:
    #     transport.close()
