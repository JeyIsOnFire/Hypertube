from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import re
import asyncio
import httpx
from bs4 import BeautifulSoup

from db import get_db_connection, close_db_connection

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
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
           "Accept-Language": "en-US,en;q=0.5",
           "Referer": "https://google.com/",
}


async def fetch_html(client, url, delay=1.0):
    try:
        await asyncio.sleep(delay)
        resp = await client.get(url, timeout=5)
        # resp.raise_for_status()
        if resp.status_code != 200:
            print(f"Error fetching {url}: {resp.status_code}")
            return None
        return resp.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

async def get_torrent_details(client, relative_url):
    html = await fetch_html(client, BASE_URL + relative_url)
    soup = BeautifulSoup(html, "html.parser")

    title = soup.select_one("div.box-info-heading h1")
    magnet = soup.select_one('a[href^="magnet:"]')
    return {
        "title": title.text.strip() if title else "No title",
        "magnet": magnet["href"] if magnet else None
    }

async def search_torrents_1337x(keyword, client, get_magnet=True):
    url = f"{LEET_URL}/category-search/{keyword}/Movies/1/"
    print(f"Searching for {keyword} at {url}")
    if get_magnet:
        html = await fetch_html(client, url)
    else:
        html = await fetch_html(client, url, delay=0)
    if not html:
        return []
    else:
        results = []
        soup = BeautifulSoup(html, "html.parser")
        links = soup.select("td.name > a:nth-of-type(2)")
        links = links[:5]
        if get_magnet:
            tasks = [get_torrent_details(client, a["href"]) for a in links]
            page_results = await asyncio.gather(*tasks)
            results.extend([r for r in page_results if r["magnet"]])
        else:
            for a in links:
                title = a.text.strip()
                results.append(title)
            # results.extend([r for r in links if r["href"]])
        return results


async def search_torrents_yts(keyword, client, get_magnet=True):
    url = f"https://yts.mx/browse-movies/{keyword}/all/all/0/latest/0/all"
    print(f"Searching for {keyword} at {url}")
    if get_magnet:
        html = await fetch_html(client, url)
    else:
        html = await fetch_html(client, url, delay=0)
    if not html:
        return []
    else:
        results = []
        soup = BeautifulSoup(html, "html.parser")
        links = soup.select("a.browse-movie-title")
        links = links[:5]
        if get_magnet:
            tasks = [get_torrent_details(client, a["href"]) for a in links]
            page_results = await asyncio.gather(*tasks)
            results.extend([r for r in page_results if r["magnet"]])
        else:
            for a in links:
                title = a.text.strip()
                results.append(title)
            # results.extend([r for r in links if r["href"]])
        return results

def clean_title(raw_title):
    return ' '.join(word.capitalize() for word in raw_title.strip().split())

def parse_movie_name(filename):
    clean_name = re.sub(r'[._\-]+', ' ', filename)
    clean_name = re.sub(r'\[.*?\]|\(.*?\)', '', clean_name)
    clean_name = re.sub(':', '', clean_name)
    clean_name = re.sub(r'\s+', ' ', clean_name).strip()
    match = re.search(r'^(.*?)(?:19|20)\d{2}', clean_name)
    raw_title = filename
    if match:
        raw_title = match.group(1)
    else:
        raw_title = re.split(r'\b(720p|1080p|2160p|x264|x265|WEBRip|BluRay|HDRip|HDTS|HDTC|CAM|NF|AMZN|DDP|HEVC)\b', clean_name, flags=re.IGNORECASE)[0]
    title = clean_title(raw_title)
    return title if title else raw_title

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

async def search_in_database(keyword):
    pass
@app.get("/search")
async def search(request: Request):
    keyword = request.query_params.get("query")
    if not keyword:
        raise HTTPException(status_code=400, detail="Keyword is required")
    ret = []
    async with httpx.AsyncClient(headers=HEADERS) as client:
        tasks = []
        keywords = keyword.split(",")
        for i in range(len(keywords)):
            keywords[i] = keywords[i].strip()
            key = keywords[i]
            if not key:
                continue
            database_results = await search_in_database(key)
            tasks.append(search_torrents_1337x(key, get_magnet=False, client=client))
            tasks.append(search_torrents_yts(key, get_magnet=False, client=client))
        results = await asyncio.gather(*tasks)
        for key in keywords:
            print("key :", key)
            key = key.strip()
            if not key:
                continue
            leet_res = results.pop(0)
            yts_res = results.pop(0)
            result_req = leet_res + yts_res
            if len(result_req) == 0:
                print(f"No results found for keyword '{key}'")
                continue
            print(f"Found {len(result_req)} results for keyword '{key}'")
            try:
                for result in result_req:
                    print("result :", result, type(result))
                    if type(result) == str and len(result) > 0:
                        movie_name = parse_movie_name(result)
                        movie_name = movie_name.lower()
                        if key.lower()[:4] in movie_name:
                            print("movie_name :", movie_name)
                            if movie_name not in ret:
                                ret.append(movie_name)
                            # if result in leet_res:
                            #     print("Found in 1337x")
                            # elif result in yts_res:
                            #     print("Found in YTS")
                    else:
                        print("No title found")
                        continue
            except Exception as e:
                print(f"Error parsing result on key {key}: {e}")
                continue
        print("Final results:", ret)
        return ret