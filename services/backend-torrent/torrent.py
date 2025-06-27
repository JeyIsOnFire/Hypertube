# torrent.py
import bencodepy
import hashlib
from typing import List, Dict, Any, Optional


class TorrentMeta:
    def __init__(self, path: str):
        self.path = path
        self.meta: Dict[bytes, Any] = {}
        self.info_hash: bytes = b''
        self.announce: str = ''
        self.announce_list: List[List[str]] = []
        self.piece_length: int = 0
        self.piece_hashes: List[bytes] = []
        self.files: Optional[List[Dict[str, Any]]] = None
        self.name: str = ''
        self._load()

    def _load(self) -> None:
        data = bencodepy.decode_from_file(self.path)
        if b'info' not in data:
            raise ValueError("Invalid torrent file: missing info key")
        self.meta = data
        raw_info = bencodepy.encode(data[b'info'])
        self.info_hash = hashlib.sha1(raw_info).digest()
        info = data[b'info']
        self.piece_length = info[b'piece length']
        pieces = info[b'pieces']
        self.piece_hashes = [pieces[i:i+20] for i in range(0, len(pieces), 20)]
        self.name = info[b'name'].decode('utf-8', errors='ignore')
        self.files = []
        if b'files' in info:
            for f in info[b'files']:
                self.files.append({
                    'path': [p.decode('utf-8', errors='ignore') for p in f[b'path']],
                    'length': f[b'length']
                })
        else:
            self.files.append({'path': [self.name], 'length': info[b'length']})
        if b'announce-list' in data:
            self.announce_list = [[u.decode() for u in grp] for grp in data[b'announce-list']]
        if b'announce' in data:
            self.announce = data[b'announce'].decode()
            if not any(self.announce in grp for grp in self.announce_list):
                self.announce_list.insert(0, [self.announce])
