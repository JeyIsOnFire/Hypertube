# client.py
import aiohttp
import asyncio
from typing import List
from torrent import TorrentMeta
from peer import Peer
from storage import FileStorage

class TorrentClient:
    def __init__(self, torrent_file: str, download_path: str):
        self.meta = TorrentMeta(torrent_file)
        self.peer_id = b"-PC0001-" + asyncio.get_event_loop().run_until_complete(
            asyncio.to_thread(lambda: __import__('random').choices(__import__('string').ascii_letters + __import__('string').digits, k=12))
        )
        self.download_path = download_path
        self.storage = FileStorage(download_path, self.meta)
        self.peers: List[Peer] = []

    async def fetch_peers(self) -> None:
        async with aiohttp.ClientSession() as session:
            for group in self.meta.announce_list:
                for url in group:
                    params = {
                        'info_hash': self.meta.info_hash,
                        'peer_id': self.peer_id,
                        'port': 6881,
                        'uploaded': 0,
                        'downloaded': 0,
                        'left': sum(f['length'] for f in self.meta.files),
                        'compact': 1,
                        'event': 'started'
                    }
                    async with session.get(url, params=params) as resp:
                        if resp.status == 200:
                            data = await resp.read()
                            # parsing compact peers omitted for brevity
                            # fill self.peers list with Peer instances

    async def start(self) -> None:
        await self.fetch_peers()
        tasks = [peer.connect() for peer in self.peers]
        await asyncio.gather(*tasks)
        # further download logic omitted
