# main.py
import asyncio
from fastapi import FastAPI, BackgroundTasks
from client import TorrentClient
import os


app = FastAPI()
clients = {}
DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', '/app/downloads')


@app.post('/start')
async def start_torrent(torrent_file: str, background: BackgroundTasks):
    client = TorrentClient(torrent_file, DOWNLOAD_DIR)
    # schedule the download task in the background
    background.add_task(client.start)
    clients[torrent_file] = client
    return {'status': 'started'}


@app.get('/health')
def health():
    return {'status': 'ok'}