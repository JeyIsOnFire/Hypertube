import asyncio
from urllib.parse import urlencode
import aiohttp

class TorrentFile:
    def __init__(self, file_name):
        import os
        import random
        import string
        self.file_name = file_name
        self.torrent_file_path = os.path.join(os.path.dirname(__file__), "torrents", f"{file_name}.torrent")
        if not os.path.exists(self.torrent_file_path):
            raise FileNotFoundError(f"Torrent file {self.file_name} does not exist.")
        self.torrent_infos = {
            "peer_id": ("-PC0001-" + "".join(random.choices(string.ascii_letters + string.digits, k=12))),
            "name": None,
            "size": None,
            "hash": None,
            "files": [],
            "pieces": {
                "length": None,
                "hashes": []
            },
            "creation_date": None,
            "comment": "",
            "created_by": None,
            "peers": {
                "available": [],
                "connected": []
            },
            "announces": {
                "default": None,
                "groups": []
            },
            "time_before_next_announce": None,
        }
        self._parse_torrent_file()
        self._exclude_udp_announce()

    def __str__(self):
        infos = [
            "Torrent File Name: " + self.file_name,
            "Torrent File Path: " + self.torrent_file_path,
            "Torrent Peer ID: " + str(self.torrent_infos["peer_id"]),
            "Torrent Name: " + str(self.torrent_infos["name"]),
            "Torrent Size: " + str(self.torrent_infos["size"]),
            "Torrent Hash: " + str(self.torrent_infos["hash"]),
            "Torrent Files: " + str(self.torrent_infos["files"]),
            "Torrent Pieces Length: " + str(self.torrent_infos["pieces"]["length"]),
            "Torrent announces: " + str(self.torrent_infos["announces"]["default"]),
            "Torrent announces groups: " + str(self.torrent_infos["announces"]["groups"]),
            "Torrent Creation Date: " + str(self.torrent_infos["creation_date"]),
            "Torrent Comment: " + str(self.torrent_infos["comment"]),
            "Torrent Created By: " + str(self.torrent_infos["created_by"]),
            "Torrent Peers Available: " + str(self.torrent_infos["peers"]["available"]),
            "Torrent Peers Connected: " + str(self.torrent_infos["peers"]["connected"]),
        ]
        return "\n".join(infos)
    
    def __repr__(self):
        return f"TorrentFile({self.file_name})"

    def _parse_torrent_file(self):
        import bencodepy
        import hashlib
        import os
        try:
            with open(self.torrent_file_path, 'rb') as f:
                torrent_data = bencodepy.decode(f.read())
            if b'info' not in torrent_data:
                raise ValueError("Invalid torrent file format.")
            self.torrent_infos["hash"] = hashlib.sha1(bencodepy.encode(torrent_data[b'info'])).digest() 
            if b'name' not in torrent_data[b'info']:
                raise ValueError("Torrent file does not contain a name.")
            self.torrent_infos["name"] = torrent_data[b'info'][b'name']
            if b'piece length' not in torrent_data[b'info']:
                raise ValueError("Torrent file does not contain piece length.")
            self.torrent_infos["size"] = torrent_data[b'info'][b'length']
            if b'piece length' not in torrent_data[b'info']:
                raise ValueError("Torrent file does not contain piece length.")
            self.torrent_infos["pieces"]["length"] = torrent_data[b'info'][b'piece length']
            if b'pieces' not in torrent_data[b'info']:
                raise ValueError("Torrent file does not contain pieces.")
            self.torrent_infos["pieces"]["hashes"] = [torrent_data[b'info'][b'pieces'][i:i+20] for i in range(0, len(torrent_data[b'info'][b'pieces']), 20)]
            if b'files' in torrent_data[b'info']:
                for file in torrent_data[b'info'][b'files']:
                    file_path = os.path.join(self.torrent_infos["name"], *[part for part in file[b'path']])
                    self.torrent_infos["files"].append(file_path)
                    self.torrent_infos["size"] += file[b'length']
            else:
                self.torrent_infos["files"].append(self.torrent_infos["name"])
                self.torrent_infos["size"] = torrent_data[b'info'][b'length']
            if b'creation date' in torrent_data:
                self.torrent_infos["creation_date"] = torrent_data[b'creation date']
            if b'comment' in torrent_data:
                self.torrent_infos["comment"] = torrent_data[b'comment']
            if b'created by' in torrent_data:
                self.torrent_infos["created_by"] = torrent_data[b'created by']
            if b'announce' not in torrent_data:
                raise ValueError("Torrent file does not contain announce URL.")
            self.torrent_infos["announces"]["default"] = torrent_data[b'announce']
            if b'announce-list' in torrent_data:
                for group in torrent_data[b'announce-list']:
                    self.torrent_infos["announces"]["groups"].append([url for url in group])
            else:
                self.torrent_infos["announces"]["groups"].append([self.torrent_infos["announces"]["default"]])
        except Exception as e:
            raise ValueError(f"Failed to parse torrent file: {e}")
    
    def _exclude_udp_announce(self):
        import re
        if self.torrent_infos["announces"]["default"] is not None:
            if re.search(r"^udp://", self.torrent_infos["announces"]["default"].decode('utf-8')):
                self.torrent_infos["announces"]["default"] = None
        for group in self.torrent_infos["announces"]["groups"]:
            for url in group:
                if re.search(r"^udp://", url.decode('utf-8')):
                    group.remove(url)

    async def contact_tracker(self, event: str, session: aiohttp.ClientSession) -> list | None:
        from urllib.parse import urlparse, quote_from_bytes
        import requests
        import time
        if len(self.torrent_infos["announces"]["groups"]) == 0:
            raise ValueError("No announce URL found.")
        response_ret = []
        for group in self.torrent_infos["announces"]["groups"]:
            if len(group) == 0:
                continue
            if len(response_ret) > 0:
                break
            for url in group:
                url = url.decode('utf-8')
                parsed_url = urlparse(url)
                if parsed_url.scheme.lower() not in ['http', 'https']:
                    continue
                try:
                    params = {
                        "info_hash": self.torrent_infos["hash"],
                        "peer_id": self.torrent_infos["peer_id"],
                        "port": 6881,
                        "uploaded": 0,
                        "downloaded": 0,
                        "left": self.torrent_infos["size"],
                        "event": event,
                        "compact": 1,
                    }
                    url = f"{url}?{urlencode(params)}"
                    async with session.get(url) as response:
                        print(f"Contacting tracker: {url}")
                        if response.status == 200:
                            data = await response.read()
                            if len(data) > 0:
                                response_ret.append(data)
                            else:
                                print(f"No data received from {url}")
                except Exception as e:
                    print(f"Failed to contact tracker: {e}")
                    # print(f"details: {e.with_traceback()}")
        return response_ret if len(response_ret) > 0 else None
    
    async def recover_peers(self):
        import json
        import bencodepy
        import hashlib
        import os
        import time
        try:
            async with aiohttp.ClientSession() as session:
                response = await self.contact_tracker("started", session)
                # print(f"Response from tracker: {bencodepy.decode(response)}")
                await asyncio.sleep(1)
                await self.contact_tracker("stopped", session)
                # if response is None:
                #     raise ValueError("No response from tracker.")
                # for data in response:
                #     decoded_data = bencodepy.decode(data)
                #     if b'peers' in decoded_data:
                #         peers = decoded_data[b'peers']
                #         if isinstance(peers, bytes):
                #             peers = [peers[i:i+6] for i in range(0, len(peers), 6)]
                #         self.torrent_infos["peers"]["available"] += peers
                #     if b'interval' in decoded_data:
                #         self.torrent_infos["time_before_next_announce"] = decoded_data[b'interval']
                #     if b'complete' in decoded_data:
                #         self.torrent_infos["peers"]["connected"] = decoded_data[b'complete']
                #     if b'incomplete' in decoded_data:
                #         self.torrent_infos["peers"]["available"] = decoded_data[b'incomplete']
            return self.torrent_infos
        except Exception as e:
            raise ValueError(f"Failed to recover peers: {e}")


async def async_main():
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    torrent_dir = os.path.join(base_dir, "torrents")
    if not os.path.exists(torrent_dir):
        os.makedirs(torrent_dir)
    user_input =  "ubuntuiso"
    if not user_input:
        print("No input provided.")
        return
    try:
        torrent = TorrentFile(user_input)
        await torrent.recover_peers()
        # print(result)
        print(torrent)
    except Exception as e:
        print(f"An error occurred: {e}")
        return

if __name__ == "__main__":
    asyncio.run(async_main())
    