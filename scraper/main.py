from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI()
 
origins = [
    "http://localhost/",
    "http://127.0.0.1/",
]
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""],
)

import asyncio
import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://1337x.to"
HEADERS = {"User-Agent": "Mozilla/5.0"}

async def fetch_html(client, url):
    resp = await client.get(url)
    resp.raise_for_status()
    return resp.text

async def get_torrent_details(client, relative_url):
    html = await fetch_html(client, BASE_URL + relative_url)
    soup = BeautifulSoup(html, "html.parser")

    title = soup.select_one("div.box-info-heading h1")
    magnet = soup.select_one('a[href^="magnet:"]')
    return {
        "title": title.text.strip() if title else "No title",
        "magnet": magnet["href"] if magnet else None
    }

async def search_torrents(keyword, max_pages=1):
    results = []
    async with httpx.AsyncClient(headers=HEADERS) as client:
        for page in range(1, max_pages + 1):
            url = f"{BASE_URL}/category-search/{keyword}/Movies/{page}/"
            html = await fetch_html(client, url)
            soup = BeautifulSoup(html, "html.parser")
            links = soup.select("td.name > a:nth-of-type(2)")
            tasks = [get_torrent_details(client, a["href"]) for a in links]
            page_results = await asyncio.gather(*tasks)
            results.extend([r for r in page_results if r["magnet"]])
    return results

def parse_movie_name(filename):
    import re
    # Remplace les points, underscores ou tirets par des espaces
    clean_name = re.sub(r'[._-]+', ' ', filename)

    # Regex pour extraire le titre et l'année
    match = re.search(r'^(.*?)\b(19|20)\d{2}\b', clean_name)
    
    if match:
        title = match.group(1).strip()
        year = match.group(2) + clean_name[match.end(2):match.end(2)+2]
        return {
            'title': title,
            'year': year
        }
    return None

@app.get("/")
async def root():
    keyword = "avatar"
    results = await search_torrents(keyword, max_pages=2)
    for r in results:
        print(parse_movie_name(r["title"]))
    return "Hello World"
