import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

#creates a open connection to postgres and manually closes it when bots down
async def create_pool():
    return await asyncpg.create_pool (
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PW"),
        database=os.getenv("DB"),
        host=os.getenv("host")
    )