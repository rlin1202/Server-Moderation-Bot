from datetime import datetime

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

#insert query example: INSERT into infractions (server_id, user_id, moderator_id, type, reason, created_at, expires_at)
async def add_server_info(pool,server_id: int, welcome_channel: int):
    query = """
            INSERT INTO servers(
                server_id,
                welcome_channel
            )
            VALUES ($1,$2)
            RETURNING server_id;
    """
    return await pool.fetchval(query,server_id,welcome_channel)

async def fetch_welcome_channel(pool, server_id: int):
    query = """
        SELECT welcome_channel
        FROM servers
        WHERE server_id = $1
    """

    return await pool.fetchval(query,server_id)

async def add_infraction(pool,member_id,server_id, moderator_id, type, reason, expires_at:datetime = None, active:bool = False):
    query = """
            INSERT INTO infractions(
                member_id,
                server_id,
                moderator_id,
                type,
                reason,
                expires_at,
                active
            )
            VALUES($1,$2,$3,$4,$5,$6,$7)
            RETURNING infraction_id
    """
    return await pool.fetchval(query,member_id,server_id,moderator_id,type,reason,expires_at,active)


