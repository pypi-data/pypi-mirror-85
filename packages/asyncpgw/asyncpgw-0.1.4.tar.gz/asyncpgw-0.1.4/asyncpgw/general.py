import discord


"""
asyncpgのラッパーのつもり
ーーーーーーーーーーーーーーーーーー
以下このクラスのそれぞれの関数に共通するパラメーターの説明
opt:
    column1=value1, column2=value2・・・

    引数に可変長キーワードを渡してる。
    optをdict型にし、key, valuesを取得する。
    column, column2 -> opt.keys()
    valu1, valu2 -> opt.values()
    $1, $2 -> enumerate(opt.keys(), 1) optのkeysの数をカウント。デフォルトを1に
"""


class Pg:
    """
    bot - Bot
    table - 対象のテーブル名
    普通はこのクラスを使う
    """
    def __init__(self, bot, table: str):
        self.bot = bot
        self.pool = bot.pool
        self.table = table

    
    async def ncfetchs(self):
        content = await self.pool.fetch(f"SELECT * FROM {self.table}")
 
        return content

    async def fetch(self, **opt):
        "テーブルの最初のデータを取得する"

        if opt is None:
            content = await self.pool.fetchrow(f"SELECT * FROM {self.table}")

        enums = enumerate(opt.keys(), 1)
        content = await self.pool.fetchrow(f"SELECT * FROM {self.table} WHERE {' AND '.join(f'{c} = ${i}' for i, c in enums)}", *opt.values())
        return content


    async def fetchs(self, **opt):
        "テーブルのデータを複数取得する"
        
        enums = enumerate(opt.keys(), 1)
        columns = ' AND '.join(f'{c} = ${i}' for i, c in enums)
   
    
        content = await self.pool.fetch(f"SELECT * FROM {self.table} WHERE {columns}", *opt.values())
 
        return content

    async def limit_fetchs(self, **opt):
        "テーブルのデータを制限数付きで取得する"

        keys = list(opt.keys())
        column = f"{keys[0]} = $1"
        limit = f"{keys[1]} $2"
        offset = f"{keys[2]} $3"

        contents = await self.pool.fetch(f'SELECT * FROM {self.table} WHERE {column} {limit} {offset}', *opt.values())
        return contents
    


    async def sort_fetchs(self, target, **opt):
        "データをソートして取得"

        column = f"{list(opt.keys())[0]} = $1"
        limit = f"{list(opt.keys())[1]} $2"

        contents = await self.pool.fetch(f'SELECT * FROM {self.table} WHERE {column} ODER BY {target} DESC {limit}', *opt.values())
        return contents
        

    async def insert(self, **opt):
        "テーブルのデータに追加する"
        
        columns = ', '.join(column for column in opt.keys())
        enums = ','.join(f"${i}" for i, column in enumerate(opt.keys(), 1))
        
        await self.pool.execute(f'INSERT INTO {self.table} ({columns}) VALUES ({enums})', *opt.values())

            
    async def update(self, **opt):
        "テーブルのデータを 上書きする"

        one_column = f"{list(opt.keys())[0]} = $1"
        enums = enumerate(opt.keys(), 1)
        key=' AND '.join(f'{c} = ${i}' for i, c in enums if i !=1)

        await self.pool.execute(f"UPDATE {self.table} SET {one_column} WHERE {key}", *opt.values())
    

    async def delete(self, **opt):
        "テーブルのデータを削除する"

        enums = enumerate(opt.keys(), 1)

        await self.pool.execute(f"DELETE FROM {self.table} WHERE {' AND '.join(f'{c} = ${i}' for i, c in enums)}", *opt.values())


    async def add(self, **opt):
        one_column = f"{list(opt.keys())[0]} = array_append({list(opt.keys())[0]}, $1)"
        enums = enumerate(opt.keys(), 1)
        columns = ' AND '.join(f'{c} = ${i}' for i, c in enums if i != 1) 

        await self.pool.execute(f'UPDATE {self.table} SET {one_column} WHERE {columns}', *opt.values())

    
    async def remove(self, **opt):
        one_column = f"{list(opt.keys())[0]} = array_remove({list(opt.keys())[0]}, $1)"
        enums = enumerate(opt.keys(), 1)
        columns = ' AND '.join(f'{c} = ${i}' for i, c in enums if i != 1)

        await self.pool.execute(f'UPDATE {self.table} SET {one_column} WHERE {columns}', *opt.values())