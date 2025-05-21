import asyncio
import asyncpg
import dotenv
import os

dotenv.load_dotenv()

db_conn = None

async def get_db_connection():  
    global db_conn
    if db_conn is None:
        db_conn = await asyncpg.connect(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB"),
            host=os.getenv("POSTGRES_HOST"),
            port=5432
        )
    return db_conn

async def close_db_connection():
    global db_conn
    if db_conn is not None:
        await db_conn.close()
        db_conn = None

async def ensure_users_table_exists():
    conn = await get_db_connection()
    result = await conn.fetchval("SELECT to_regclass('public.scrapped_films');")

    if result is None:
        print("Creating 'scrapped_films' table...")
        await conn.execute("""
            CREATE TABLE scrapped_films (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                year TEXT NOT NULL,
                origin TEXT NOT NULL,
                magnet TEXT NOT NULL
            );
        """)
    else:
        print("'scrapped_films' table already exists.")
    await conn.close()

async def main():
    await ensure_users_table_exists()
    await close_db_connection()

if __name__ == "__main__":
    asyncio.run(main())
