import asyncio
import asyncpg
import dotenv
import os

dotenv.load_dotenv()

db_conn = None

db_pool = None


async def get_connection():
    global db_pool
    loop = 0
    while True:
        try:
            if db_pool is None:
                db_pool = await asyncpg.create_pool(
                    user=os.getenv("POSTGRES_USER"),
                    password=os.getenv("POSTGRES_PASSWORD"),
                    database=os.getenv("POSTGRES_DB"),
                    host=os.getenv("POSTGRES_HOST"),
                    port=5432
                )
            break
        except Exception as e:
            if loop > 5:
                print("Max retries reached. Exiting...")
                break
            loop += 1
            print(f"Error creating connection pool: {e}")
            await asyncio.sleep(5)
    return db_pool


async def single_conn_db():
    global db_conn
    loop = 0
    if db_conn is None:
        while True:
            try:
                if db_conn is None:
                    db_conn = await asyncpg.connect(
                        user=os.getenv("POSTGRES_USER"),
                        password=os.getenv("POSTGRES_PASSWORD"),
                        database=os.getenv("POSTGRES_DB"),
                        host=os.getenv("POSTGRES_HOST"),
                        port=5432
                    )
                break
            except Exception as e:
                if loop > 5:
                    print("Max retries reached. Exiting...")
                    break
                loop += 1
                print(f"Error connecting to database: {e}")
                await asyncio.sleep(5)
                continue
    return db_conn

async def close_db_connection():
    global db_conn
    if db_conn is not None:
        await db_conn.close()
        db_conn = None

async def ensure_users_table_exists():
    conn = await single_conn_db()
    result = await conn.fetchval("SELECT to_regclass('public.movies_movie');")

    if result is None:
        print("Creating 'movies_movie' table...")
        await conn.execute("""
            CREATE TABLE movies_movie (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                year INT NOT NULL,
                origin TEXT NOT NULL,
                magnet TEXT,
                page TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
