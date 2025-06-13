from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import re
import asyncio
import httpx
from bs4 import BeautifulSoup

from db import get_connection

import unicodedata

import time

app = FastAPI()
 
origins = [
    "http://localhost/",
    "http://127.0.0.1/",
    "http://backend-movies:7000",
]
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""],
)


LEET_URL = "https://1337x.to"
YTS_URL = "https://yts.mx"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
           "Accept-Language": "en-US,en;q=0.5",
           "Referer": "https://google.com/",
}


def is_latin_letters_only(s):
    for c in s:
        if c.isalpha():
            name = unicodedata.name(c, '')
            if 'LATIN' not in name:
                return False
    return True

async def fetch_html(client, url, delay=1.0):
    try:
        if delay > 0:
            await asyncio.sleep(delay)
        resp = await client.get(url, timeout=5)
        if resp.status_code != 200:
            print(f"Error fetching {url}: {resp.status_code}")
            return None
        return resp.text
    except Exception as e:
        return None

# async def get_torrent_details(client, relative_url):
#     html = await fetch_html(client, BASE_URL + relative_url)
#     soup = BeautifulSoup(html, "html.parser")

#     title = soup.select_one("div.box-info-heading h1")
#     magnet = soup.select_one('a[href^="magnet:"]')
#     return {
#         "title": title.text.strip() if title else "No title",
#         "magnet": magnet["href"] if magnet else None
#     }

async def search_torrents_1337x(keyword, client, background_tasks):
    url = f"{LEET_URL}/category-search/{keyword}/Movies/1/"
    html = await fetch_html(client, url, delay=0)
    if not html:
        return []
    else:
        results = []
        soup = BeautifulSoup(html, "html.parser")
        links = soup.select("td.name > a:nth-of-type(2)")
        links = links[:5]
        if links is None or len(links) == 0:
            background_tasks.add_task(save_not_exists_in_database, {
                "title": keyword[:-4].strip(),
                "year": int(keyword[-4:]),
                "link": url,
                "source": "1337x",
                "keyword": keyword
            })
            return []
        for a in links:
            title = a.text.strip()
            title = parse_movie_name(title, keyword[:-4])
            if title:
                results.append({
                    "title": title,
                    "link": LEET_URL + a["href"],
                    "source": "1337x",
                    "keyword": keyword
                })
        return results


async def search_torrents_yts(keyword, client, background_tasks):
    url = f"{YTS_URL}/browse-movies/{keyword}/all/all/0/latest/0/all"
    html = await fetch_html(client, url, delay=0)
    if not html:
        return []
    else:
        results = []
        soup = BeautifulSoup(html, "html.parser")
        links = soup.select("a.browse-movie-title")
        links = links[:5]
        if links is None or len(links) == 0:
            background_tasks.add_task(save_not_exists_in_database, {
                "title": keyword[:-4].strip(),
                "year": int(keyword[-4:]),
                "link": url,
                "source": "YTS",
                "keyword": keyword
            })
            return []
        for a in links:
            title = a.text.strip()
            title = parse_movie_name(title, keyword[:-4])
            if title:
                results.append({
                    "title": title,
                    "link": a["href"],
                    "source": "YTS",
                    "keyword": keyword
                })
        return results

def clean_title(raw_title):
    return ' '.join(word.capitalize() for word in raw_title.strip().split())

def resub_title_regex(title:str) -> str:
    return re.sub(r'[^a-zA-Z0-9&-]', '', title)

def parse_movie_name(filename: str, keyword: str):
    keyword = keyword.lower()
    keyword = resub_title_regex(keyword)
    filename = filename.lower()
    filename = resub_title_regex(filename)
    return filename[0:len(keyword)]

# @app.get("/")
# async def root():
#     keyword = "avatar"
#     results = await search_torrents(keyword, max_pages=1)
#     ret = []
#     for result in results:
#         movie_name = parse_movie_name(result["title"])
#         ret.append({
#             "title": movie_name if movie_name else result["title"],
#             "magnet": result["magnet"]
#         })
#     return ret

async def search_in_database(keyword:str) -> str | None:
    try:
        db_pool = await get_connection()
        title = keyword[:-4].strip()
        year = int(keyword[-4:])
        async with db_pool.acquire() as conn:
            exist = await conn.fetch("SELECT * FROM movies_movie WHERE name = $1 AND year = $2", title, year)
            if exist:
                return keyword
            return None
    except Exception as e:
        print(f"Error searching in database: {e}")
        return None

async def search_many_in_database(keywords:list[str]) -> dict[str, dict]:
    db_pool = await get_connection()
    async with db_pool.acquire() as conn:
        names = [k[:-4].strip() for k in keywords]
        years = [int(k[-4:]) for k in keywords]

        query = """
        SELECT * FROM movies_movie
        WHERE (name, year) IN (
            SELECT UNNEST($1::text[]), UNNEST($2::int[])
        )
        """

        rows = await conn.fetch(query, names, years)
        result = {}
        for row in rows:
            keyword = f"{row['name']} {row['year']}"
            result[keyword] = {
                "title": row["name"],
                "year": row["year"],
                "link": row["page"],
                "source": row["origin"],
                "keyword": keyword,
                "exist": True
            }
        return result

async def save_in_database(film_info:dict):
    db_pool = await get_connection()
    async with db_pool.acquire() as conn:
        print("Saving in database")
        exist = await conn.fetch("SELECT * FROM movies_movie WHERE name = $1 AND year = $2 AND origin = $3", film_info["keyword"][:-4].strip(), int(film_info["keyword"][-4:]), film_info["source"])
        if exist:
            print("Already exists in database")
            return
        await conn.execute(
            """
            INSERT INTO movies_movie (name, year, origin, page)
            VALUES ($1, $2, $3, $4)
            """,
            film_info["keyword"][:-4].strip(), int(film_info["keyword"][-4:]), film_info["source"], film_info["link"]
        )

async def save_not_exists_in_database(film_info:dict):
    db_pool = await get_connection()
    async with db_pool.acquire() as conn:
        print("Saving not exists in database")
        exist = await conn.fetch("SELECT * FROM movies_movie_not_exists WHERE name = $1 AND year = $2 AND origin = $3", film_info["keyword"][:-4].strip(), int(film_info["keyword"][-4:]), film_info["source"])
        if exist:
            print("Already exists in not exists database")
            return
        await conn.execute(
            """
            INSERT INTO movies_movie_not_exists (name, year, origin, page)
            VALUES ($1, $2, $3, $4)
            """,
            film_info["keyword"][:-4].strip(), int(film_info["keyword"][-4:]), film_info["source"], film_info["link"]
        )

async def search_many_not_exists_in_database(keywords:list[str]) -> dict[str, dict]:
    db_pool = await get_connection()
    async with db_pool.acquire() as conn:
        names = [k[:-4].strip() for k in keywords]
        years = [int(k[-4:]) for k in keywords]

        query = """
        SELECT * FROM movies_movie_not_exists
        WHERE (name, year) IN (
            SELECT UNNEST($1::text[]), UNNEST($2::int[])
        )
        """

        rows = await conn.fetch(query, names, years)
        result = {}
        for row in rows:
            keyword = f"{row['name']} {row['year']}"
            result[keyword] = {
                "title": row["name"],
                "year": row["year"],
                "link": row["page"],
                "source": row["origin"],
                "keyword": keyword,
                "exist": False
            }
        return result

@app.get("/search")
async def search(request: Request, background_tasks: BackgroundTasks):
    keyword = request.query_params.get("query")
    if not keyword:
        raise HTTPException(status_code=400, detail="Keyword is required")
    ret = []
    async with httpx.AsyncClient(headers=HEADERS) as client:
        actual_time = time.time()
        tasks = []
        keywords = keyword.split("~")
        clean_keywords = []
        for keyword in keywords:
            keyword = keyword.strip()
            if not keyword:
                continue
            if len(keyword) < 6:
                continue
            if not is_latin_letters_only(keyword[:-4].strip()):
                continue
            clean_keywords.append(keyword)
        keywords = clean_keywords
        if len(keywords) == 0:
            raise HTTPException(status_code=400, detail="No valid keywords found")
        # for key in keywords:
        #     tasks.append(search_in_database(key))
        # results = await asyncio.gather(*tasks)
        # tasks = []
        results = await search_many_in_database(keywords)
        results_not_exists = await search_many_not_exists_in_database(keywords)
        results.update(results_not_exists)
        for key in keywords:
            if key in results:
                key_info = results[key]
                if key_info["exist"] and key not in ret:
                    ret.append(key)
                continue
            tasks.append(search_torrents_1337x(key, client=client, background_tasks=background_tasks))
            tasks.append(search_torrents_yts(key, client=client, background_tasks=background_tasks))
        if len(tasks) == 0:
            print("No tasks to run")
            print("time taken for search:", time.time() - actual_time)    
            return ret
        results = await asyncio.gather(*tasks)
        print("time taken for search:", time.time() - actual_time)
        unified_results = []
        actual_time = time.time()
        tasks = []
        for result in results:
            unified_results.extend(result)
        for result in unified_results:
            if type(result) != dict:
                continue
            if "title" not in result or "link" not in result or "source" not in result or "keyword" not in result:
                continue
            if len(result["title"].strip()) == 0 or len(result["link"].strip()) == 0 or len(result["source"].strip()) == 0 or len(result["keyword"].strip()) == 0:
                continue
            if result["title"] != resub_title_regex(result["keyword"][:-4].strip().lower()):
                continue
            if result["keyword"] in ret:
                continue
            background_tasks.add_task(save_in_database, result)
            ret.append(result["keyword"])
        print("time taken for saving in database:", time.time() - actual_time)
        return ret
    
@app.get("/health")
async def health():
    return {"status": "ok"}