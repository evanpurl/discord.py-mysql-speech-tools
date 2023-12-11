import os
import random
from aiomysql import Error
import aiomysql


async def create_speech_pool():
    try:
        pool = await aiomysql.create_pool(host=os.getenv('host'), port=int(os.getenv('port')),
                                          user=os.getenv('speech_user'), password=os.getenv('speech_password'),
                                          db=os.getenv('speech_db'))

        return pool
    except Exception or Error as e:
        print(f"Create Speech Pool: {e}")


async def get_all(pool, msg):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    f""" SELECT response FROM bot_speech WHERE prompt like '%{msg}%' order by rand() limit 1;""")
                results = await cur.fetchone()
        if not results:
            return None
        if len(results) == 0:
            return None
        return f"{results[0]}"
    except Exception or Error as e:
        print(f"speech get all: {e}")


async def get_response(message):
    try:
        conn = await create_speech_pool()
        return await get_all(conn, message)

    except Exception as e:
        print(f"get config: {e}")