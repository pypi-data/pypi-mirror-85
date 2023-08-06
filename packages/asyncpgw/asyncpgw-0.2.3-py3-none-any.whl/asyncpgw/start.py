import asyncpg


async def connect(url):
    "postgresqlに接続する関数"
    pool=await asyncpg.create_pool(url,
        max_size=1,
        min_size=1)
    return pool
    

async def create(pool, table):
    "postgresqlにテーブルを追加する関数"
    await pool.execute(f'CREATE TABLE IF NOT  EXISTS {table}')