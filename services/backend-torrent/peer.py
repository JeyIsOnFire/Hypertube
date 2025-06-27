# peer.py
import asyncio
import hashlib
from typing import Tuple


class Peer:
    def __init__(self, ip: str, port: int, info_hash: bytes, peer_id: bytes):
        self.ip = ip
        self.port = port
        self.info_hash = info_hash
        self.peer_id = peer_id
        self.reader: asyncio.StreamReader = None  # type: ignore
        self.writer: asyncio.StreamWriter = None  # type: ignore
        self.handshake_done = False

    async def connect(self, timeout: float = 5.0) -> None:
        self.reader, self.writer = await asyncio.wait_for(
            asyncio.open_connection(self.ip, self.port), timeout=timeout
        )
        await self._handshake()

    async def _handshake(self) -> None:
        pstr = b"BitTorrent protocol"
        msg = b"".join([
            bytes([len(pstr)]), pstr,
            b"\x00"*8, self.info_hash, self.peer_id
        ])
        self.writer.write(msg)
        await self.writer.drain()
        resp = await self.reader.readexactly(68)
        if resp[1:20] != pstr or resp[28:48] != self.info_hash:
            raise ConnectionError(f"Handshake failed with {self.ip}:{self.port}")
        self.handshake_done = True

    async def close(self) -> None:
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
