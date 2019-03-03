import aiosqlite

from node.conf import tune as T
from common import globall as G

'''
credit level:
0: friend, can be trusted
1: partner, not trustworthy, need check
2: stranger, not trustworthy, check if interested
3: bankrupt, only allow spending coin that is earned
4: cheat, blacklist
'''

class Credit:
    def __init__(self):
        pass

    @classmethod
    async def add(cls, table, name, ID, credit_int):
        T.LOGGER.debug('')

        try:
            async with aiosqlite.connect(T.PATH_CREDIT) as db:
                await db.execute('create table if not exists \
                              {0}(name nchar({1}) primary key, \
                                          id char({2}) unique, \
                                          credit integer)'.
                             format(table, G.LEN_NAME, G.LEN_ID))
                sql = 'insert into {} values(?,?,?)'.format(table)
                await db.execute(sql, (name, ID, credit_int))
                await db.commit()
                return True
        except Exception as e:
            T.LOGGER.warning(e)
            return False

    @classmethod
    async def search(cls, table, name):
        T.LOGGER.debug('')

        try:
            async with aiosqlite.connect(T.PATH_CREDIT) as db:
                sql = 'select * from {} where name=?'.format(table)
                async with db.execute(sql, (name,)) as cursor:
                    async for row in cursor:
                        return row
                return None
        except Exception as e:
            T.LOGGER.warning(e)
            return None




