import base58
import os
import sys
import aiofiles
import aiosqlite

from common import globall as G
from node.conf import tune as T

class Chain:
    def __init__(self, folder, ID_own, pri_key=None, pub_key_x=None, pub_key_y=None):
        '''
        ID: byte of base58 encode of Public Key coordinate x
        ''' 
        self.ID_own = ID_own
        if pub_key_x:
            self.pri_key = pri_key
            self.pub_key_x = pub_key_x
            self.pub_key_y = pub_key_y
        
        self.fo_ID = folder + ID_own + b'/'
        if not os.path.exists(self.fo_ID):
            os.makedirs(self.fo_ID)
        self.fo_db = folder + b'db/'
        self.path_guide = self.fo_db + b'guide.db'

        # init value for root card
        self.i_ch = 0
        self.i_ch_next = 1
        self.i_f = 0
        self.i_f_next = 0
        self.i_l = 0
        self.i_l_next = 1

        self.coin_rest = 0
        self.c_last = None

    def update(self, c_last, i_ch_0=None):
        T.LOGGER.debug('')
        
        if i_ch_0 == None: # for non-init
            if c_last[G.P_I_CH] != base58.b58encode_int(self.i_ch_next):
                T.LOGGER.error('chain index is not corrent for last card')
                return False

            self.i_ch = self.i_ch_next
            self.i_f = self.i_f_next
            self.i_l = self.i_l_next
        

        if self.i_l == G.NUM_L_BODY -1:
            self.i_f_next = self.i_f + 1
            self.i_l_next = 0
        else:
            self.i_f_next = self.i_f
            self.i_l_next = self.i_l + 1

        self.i_ch_next = self.i_f_next * G.NUM_L_BODY + self.i_l_next

        self.c_last = c_last

        if self.c_last[G.P_TYPE] == G.CHARGE:
            self.coin_rest = (base58.b58decode_int(self.c_last[G.P_COIN_REST]) + 
                                base58.b58decode_int(self.c_last[G.P_COIN_CHRE])) 
        elif self.c_last[G.P_TYPE] == G.REDEEM:
            self.coin_rest = (base58.b58decode_int(self.c_last[G.P_COIN_REST]) - 
                                base58.b58decode_int(self.c_last[G.P_COIN_CHRE])) 
        elif self.c_last[G.P_TYPE] == G.PAY:
            self.coin_rest = (base58.b58decode_int(self.c_last[G.P_COIN_REST]) - 
                                base58.b58decode_int(self.c_last[G.P_COIN_TRADE]))
        elif self.c_last[G.P_TYPE] == G.EARN:
            self.coin_rest = (base58.b58decode_int(self.c_last[G.P_COIN_REST]) +
                                base58.b58decode_int(self.c_last[G.P_COIN_TRADE]))
        else:
            self.coin_rest = base58.b58decode_int(self.c_last[G.P_COIN_REST])
        
        T.LOGGER.debug('update success')
        return True


    async def init(self, c_root=None):
        '''
        for client
        To do: consider the consistency of files: chain and guide
        '''
        T.LOGGER.debug('')
        
        # check the guide.db, if not exit, then create
        async with aiosqlite.connect(self.path_guide) as db:
            await db.execute('create table if not exists \
                              table_guide(id char({0}) primary key, \
                                          ch_0 integer, \
                                          m_1 integer, \
                                          ch_1 integer, \
                                          m_2 integer, \
                                          ch_2 integer)'.
                             format(G.LEN_ID))
            i_ch_0 = None # the last chain index
            c_last = None # the last chain card
            T.LOGGER.debug(self.ID_own)
            async with db.execute('select * from table_guide where id=?', 
                                    (self.ID_own,)) as cursor:
                async for row in cursor:
                    i_ch_0 = row[T.P_GUIDE_CH_LAST]
                    T.LOGGER.debug(i_ch_0)
                    self.i_ch = i_ch_0
                    self.i_f = i_ch_0//G.NUM_L_BODY
                    self.i_l = i_ch_0% G.NUM_L_BODY
                    c_last = await self.fetch_ch(self.i_f, self.i_l)

            T.LOGGER.debug(c_last)
            if i_ch_0 == None:                
                if c_root is None:
                    c_last = self.find_c_last() # TODO
                else:
                    await db.execute('insert into table_guide values(?,?,?,?,?,?)', (self.ID_own,0,0,0,0,0))
                    await db.commit()
                    if not await self.append(c_root, 0, 0):
                        return False
                    self.c_last = c_root.split()
                    return True

        if not c_last:
            T.LOGGER.error('last own card should not be None')
            return False

        if not self.update(c_last.split(), i_ch_0):
            return False
                
        return True
    
    async def get_guide(self, ID):
        '''
        for node
        '''
        T.LOGGER.debug('')

        async with aiosqlite.connect(self.path_guide) as db:
            async with db.execute('select * from table_guide where id=?', (ID,)) as cursor:
                async for row in cursor:
                    return row
                return None


    async def set_guide(self, ID, i_ch_0=None, i_m_1=None, i_ch_1=None, i_m_2=None, i_ch_2=None):
        '''
        0: for last card
        1: for pay and post
        2: for earn and charge/redeem
        '''
        T.LOGGER.debug('')

        async with aiosqlite.connect(self.path_guide) as db:
            row_exist = None
            async with db.execute('select * from table_guide where id=?', (ID,)) as cursor:
                async for row in cursor:
                    row_exist = row

            if not row_exist:
                await db.execute('insert into table_guide values(?,?,?,?,?,?)', 
                            (ID,0,0,0,0,0))

            if (i_ch_0 == None) and (i_m_1 == None) and (i_m_2 == None):
                pass
            elif (i_ch_0 != None) and (i_m_1 == None) and (i_m_2 == None):
                await db.execute('update table_guide set ch_0=? where id=?', 
                                (i_ch_0, ID))
            elif (i_ch_0 != None) and (i_m_1 != None) and (i_m_2 == None):
                await db.execute('update table_guide set ch_0=?,m_1=?,ch_1=? where id=?', 
                                (i_ch_0, i_m_1, i_ch_1, ID))
            elif (i_ch_0 != None) and (i_m_1 == None) and (i_m_2 != None):
                await db.execute('update table_guide set ch_0=?,m_2=?,ch_2=? where id=?', 
                                (i_ch_0, i_m_2, i_ch_2, ID))
            elif (i_ch_0 == None) and (i_m_1 != None) and (i_m_2 == None):
                await db.execute('update table_guide set m_1=?,ch_1=? where id=?', 
                                (i_m_1, i_ch_1, ID))
            elif (i_ch_0 == None) and (i_m_1 == None) and (i_m_2 != None):
                await db.execute('update table_guide set m_2=?,ch_2=? where id=?', 
                                (i_m_2, i_ch_2, ID))
            else:
                T.LOGGER.error('guide index set is improper')
                await db.commit()
                return False

            await db.commit()
            T.LOGGER.debug('finish')
            return True
        
        
    async def create_f(self, path_f, i_l, l_new):
        '''
        for server and client

        line 0: version of chain file
        line 1: the next close line need to be checked (based on head line of file);                 
        line 2-3: reserved
        '''
        T.LOGGER.debug('')

        async with aiofiles.open(path_f, 'wb+') as f:
            for i in range(G.NUM_L_HEAD):
                await f.write((G.LEN_L-1)*b' ' + b'\n')
            
            await f.seek(0)
            l_0 = G.VER # line 0
            await f.write(l_0)

            await f.seek(G.LEN_L)
            l_1 = b'0' # line 1
            await f.write(l_1)

            await f.seek((i_l+G.NUM_L_HEAD)*G.LEN_L)
            await f.write(l_new)
    

    async def fetch_ch(self, i_f = None, i_l=None):
        '''
        need to check i_ch
        '''
        T.LOGGER.debug('')

        if i_f:
            if i_f > self.i_f or i_f < 0:
                return b''
            if i_l >= G.NUM_L_BODY or i_l < 0:
                return b''
        else:
            i_f = self.i_f
            i_l = self.i_l
        
        path_fetch = self.fo_ID + str(i_f).encode()
        p_seek = (i_l+G.NUM_L_HEAD) * G.LEN_L

        try:
            async with aiofiles.open(path_fetch, 'rb') as f:
                await f.seek(p_seek)
                l_byte = (await f.readline()).strip(b' \n\x00')
                return l_byte
        except FileNotFoundError:
            return b''

    async def fetch_m(self, ID, i_m):
        '''
        for server
        '''
        T.LOGGER.debug('')

        async with aiosqlite.connect(self.path_guide) as db:            
            # await db.execute('insert into table_guide values(?,?,?,?,?)', (ID,0,0,0,0))
            # await db.commit()
            return  


    async def append(self, c_byte, i_f=None, i_l=None):
        '''
        For client and server
        '''
        T.LOGGER.debug('')

        # check the i_ch
        if (i_f is None) or (i_l is None):
            i_f = self.i_f_next
            i_l = self.i_l_next
        else:
            if i_f < 0:
                return False
            if i_l >= G.NUM_L_BODY or i_l < 0:
                return False

        path_f = self.fo_ID + str(i_f).encode()

        len_pad = G.LEN_L-len(c_byte) - 1
        if len_pad < 0:
            # T.LOGGER.error('Card append size should be equal to designed.')
            return False
        l_new = c_byte + len_pad * b' ' + b'\n'

        try:
            async with aiofiles.open(path_f, 'rb+') as f:
                await f.seek((i_l+G.NUM_L_HEAD)*G.LEN_L)
                await f.write(l_new)
                return True
        except FileNotFoundError:
            await self.create_f(path_f, i_l, l_new)
            return True

        # do this out of the class
        # if (i_f > self.i_f) or (i_f == self.i_f 
        #                             and i_l > self.i_l):
        #     await self.set_guide(self.ID_own, i_f*G.NUM_L_BODY + i_l)
        


    def append_check(self, c_byte):
        '''
        Check the relation between the card and the last line
        '''
        T.LOGGER.debug('')
       

    def find_c_last(self):
        '''
        find the last card in chain file
        '''
        T.LOGGER.debug('')

        c_last = None
        return c_last
