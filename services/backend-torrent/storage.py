# storage.py
import hashlib
import os
from typing import BinaryIO


def verify_piece(data: bytes, expected_hash: bytes) -> bool:
    return hashlib.sha1(data).digest() == expected_hash


class FileStorage:
    def __init__(self, download_path: str, meta):
        self.base = download_path
        os.makedirs(self.base, exist_ok=True)
        self.meta = meta

    def write_piece(self, index: int, data: bytes) -> None:
        piece_len = self.meta.piece_length
        offset = index * piece_len
        filename = os.path.join(self.base, self.meta.name)
        # ensure file exists
        with open(filename, 'r+b' if os.path.exists(filename) else 'wb') as f:
            f.seek(offset)
            f.write(data)
