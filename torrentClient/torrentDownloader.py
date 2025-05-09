import asyncio
from urllib.parse import urlencode
import aiohttp

class Peer:
    def __init__(self, ip:str, port:int):
        if not isinstance(ip, str):
            raise TypeError("IP must be a string.")
        if not isinstance(port, int):
            raise TypeError("Port must be an integer.")
        if len(ip) == 0:
            raise ValueError("IP cannot be empty.")
        if port < 0 or port > 65535:
            raise ValueError("Port must be between 0 and 65535.")
        self.ip = ip
        self.port = port
        self.reader = None
        self.writer = None
        self.status = "disconnected"
    
    def __str__(self):
        return f"Peer({self.ip}:{self.port})"
    def __repr__(self):
        return f"Peer({self.ip}:{self.port})"

    async def connect(self):
        try:
            self.reader, self.writer = await asyncio.wait_for(
                asyncio.open_connection(self.ip, self.port),
                timeout=5
            )
            self.status = "connected"
        except Exception as e:
            self.status = "disconnected"
        return self
    
    async def close(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()

class TorrentFile:
    def __init__(self, file_name:str = None, magnet_link:str = None):
        import os
        import random
        import string
        if file_name is None and magnet_link is None:
            raise ValueError("Either file_name or magnet_link must be provided.")
        if file_name is not None and magnet_link is not None:
            raise ValueError("Only one of file_name or magnet_link must be provided.")
        if file_name is not None:
            if not isinstance(file_name, str):
                raise TypeError("file_name must be a string.")
            if len(file_name) == 0:
                raise ValueError("file_name cannot be empty.")
            if not file_name.endswith(".torrent"):
                raise ValueError("file_name must end with .torrent.")
            if not os.path.exists(os.path.join(os.path.dirname(__file__), "torrents", file_name)):
                raise FileNotFoundError(f"Torrent file {file_name} does not exist.")
        if magnet_link is not None:
            if not isinstance(magnet_link, str):
                raise TypeError("magnet_link must be a string.")
            if len(magnet_link) == 0:
                raise ValueError("magnet_link cannot be empty.")
            if not magnet_link.startswith("magnet:"):
                raise ValueError("magnet_link must start with 'magnet:'.")
            raise NotImplementedError("Magnet link support is not implemented yet.")
        self.file_name = file_name
        self.torrent_file_path = os.path.join(os.path.dirname(__file__), "torrents", f"{file_name}")
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
            "trackers": {
                "default": None,
                "groups": [],
                "active": [],
                "next_contact": None
            },
        }
        self._parse_torrent_file()
        self._exclude_udp_tracker()

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
            "Torrent trackers: " + str(self.torrent_infos["trackers"]["default"]),
            "Torrent trackers groups: " + str(self.torrent_infos["trackers"]["groups"]),
            "Torrent Creation Date: " + str(self.torrent_infos["creation_date"]),
            "Torrent Comment: " + str(self.torrent_infos["comment"]),
            "Torrent Created By: " + str(self.torrent_infos["created_by"]),
            "Torrent Peers Available: " + str(self.torrent_infos["peers"]["available"]),
            "Torrent Peers Connected: " + str(self.torrent_infos["peers"]["connected"]),
            "Torrent Trackers Active: " + str(self.torrent_infos["trackers"]["active"]),
            "Torrent Trackers Next Contact: " + str(self.torrent_infos["trackers"]["next_contact"]),
        ]
        return "\n".join(infos)
    
    def __repr__(self):
        return f"TorrentFile({self.file_name})"
    
    async def close(self):
        if len(self.torrent_infos["peers"]["connected"]) > 0:
            for peer_conn in self.torrent_infos["peers"]["connected"]:
                await peer_conn.close()
                self.torrent_infos["peers"]["connected"].remove(peer_conn)
        await self.close_trackers()

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
            info = torrent_data[b'info']
            self.torrent_infos["name"] = info[b'name'].decode(errors='ignore')

            if b'files' in info:  # Multi-fichier
                self.torrent_infos["size"] = 0
                for file in info[b'files']:
                    file_path = os.path.join(
                        self.torrent_infos["name"],
                        *[part.decode(errors='ignore') for part in file[b'path']]
                    )
                    self.torrent_infos["files"].append(file_path)
                    self.torrent_infos["size"] += file[b'length']
            else:  # Mono-fichier
                self.torrent_infos["files"].append(self.torrent_infos["name"])
                self.torrent_infos["size"] = info[b'length']
            if b'creation date' in torrent_data:
                self.torrent_infos["creation_date"] = torrent_data[b'creation date']
            if b'comment' in torrent_data:
                self.torrent_infos["comment"] = torrent_data[b'comment']
            if b'created by' in torrent_data:
                self.torrent_infos["created_by"] = torrent_data[b'created by']
            if b'announce' not in torrent_data:
                raise ValueError("Torrent file does not contain tracker URL.")
            self.torrent_infos["trackers"]["default"] = torrent_data[b'announce']
            if b'tracker-list' in torrent_data:
                for group in torrent_data[b'announce-list']:
                    self.torrent_infos["trackers"]["groups"].append([url for url in group])
            else:
                self.torrent_infos["trackers"]["groups"].append([self.torrent_infos["trackers"]["default"]])
        except Exception as e:
            raise ValueError(f"Failed to parse torrent file: {e}")
    
    def _exclude_udp_tracker(self):
        import re
        if self.torrent_infos["trackers"]["default"] is not None:
            if re.search(r"^udp://", self.torrent_infos["trackers"]["default"].decode('utf-8')):
                self.torrent_infos["trackers"]["default"] = None
        for group in self.torrent_infos["trackers"]["groups"]:
            for url in group:
                if re.search(r"^udp://", url.decode('utf-8', errors='ignore')):
                    group.remove(url)

    async def contact_tracker(self, event: str, session: aiohttp.ClientSession) -> list | None:
        from urllib.parse import urlparse
        if len(self.torrent_infos["trackers"]["groups"]) == 0:
            raise ValueError("No tracker URL found.")
        response_ret = []
        loop_on = self.torrent_infos["trackers"]["groups"]
        if event == "stopped":
            loop_on = [self.torrent_infos["trackers"]["active"]]
        for group in loop_on:
            if len(group) == 0:
                continue
            if len(response_ret) > 0:
                break
            for url in group:
                if isinstance(url, bytes):
                    url = url.decode('utf-8', errors='ignore')
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
                    urlparams = f"{url}?{urlencode(params)}"
                    async with session.get(urlparams) as response:
                        print(f"Contacting tracker: {url}")
                        if response.status == 200:
                            data = await response.read()
                            if len(data) > 0:
                                response_ret.append(data)
                                if event == "started":
                                    self.torrent_infos["trackers"]["active"].append(url)
                                elif event == "stopped":
                                    self.torrent_infos["trackers"]["active"].remove(url)
                            else:
                                print(f"No data received from {url}")
                except Exception as e:
                    print(f"Failed to contact tracker: {e}")
        return response_ret if len(response_ret) > 0 else None
    
    async def recover_peers(self):
        import bencodepy
        try:
            async with aiohttp.ClientSession() as session:
                response = await self.contact_tracker("started", session)
                if response is None:
                    raise ValueError("No response from tracker.")
                for data in response:
                    decoded_data = bencodepy.decode(data)
                    print(f"Decoded data: {decoded_data}")
                    if b'failure reason' in decoded_data:
                        raise ValueError(f"Tracker error: {decoded_data[b'failure reason']}")
                    if b'interval' in decoded_data:
                        if self.torrent_infos["trackers"]["next_contact"] is None:
                            self.torrent_infos["trackers"]["next_contact"] = decoded_data[b'interval']
                        else:
                            self.torrent_infos["trackers"]["next_contact"] = min(self.torrent_infos["trackers"]["next_contact"], decoded_data[b'interval'])
                    if b'peers' in decoded_data:
                        peers = decoded_data[b'peers']
                        print(f"Peers data: {peers}")
                        if len(peers) % 6 == 0:  # Format compact, chaque peer fait 6 octets
                            parsed_peers = []
                            for i in range(0, len(peers), 6):
                                peer = peers[i:i+6]
                                ip = '.'.join(map(str, peer[:4]))  # Les 4 premiers octets pour l'IP
                                port = (peer[4] << 8) + peer[5]  # Les 2 derniers octets pour le port
                                parsed_peers.append((ip, port))
                            self.torrent_infos["peers"]["available"].extend(parsed_peers)
        except Exception as e:
            raise ValueError(f"Failed to recover peers: {e}")

    async def connect_peers(self):
        peers = self.torrent_infos["peers"]["available"]
        if len(peers) == 0:
            raise ValueError("No peers available.")
        tasks = []
        for peer in peers:
            if not isinstance(peer, tuple) or len(peer) != 2:
                raise ValueError("Invalid peer format.")
            ip, port = peer
            if not isinstance(ip, str) or not isinstance(port, int):
                raise TypeError("IP must be a string and port must be an integer.")
            if len(ip) == 0:
                raise ValueError("IP cannot be empty.")
            if port < 0 or port > 65535:
                raise ValueError("Port must be between 0 and 65535.")
            peer_conn = Peer(ip, port)
            tasks.append(peer_conn.connect())
        if len(tasks) == 0:
            raise ValueError("No peers to connect to.")
        connected_peers = await asyncio.gather(*tasks)
        for peer_conn in connected_peers:
            if peer_conn.status == "connected":
                self.torrent_infos["peers"]["connected"].append(peer_conn)
            else:
                print(f"Failed to connect to peer: {peer_conn}")

    async def close_trackers(self):
        import aiohttp
        try:
            async with aiohttp.ClientSession() as session:
                await self.contact_tracker("stopped", session)
        except Exception as e:
            raise ValueError(f"Failed to close trackers: {e}")


async def async_main():
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    torrent_dir = os.path.join(base_dir, "torrents")
    if not os.path.exists(torrent_dir):
        os.makedirs(torrent_dir)
    user_input =  "Child_Bride.avi.torrent"
    if not user_input:
        print("No input provided.")
        return
    try:
        torrent = TorrentFile(file_name=user_input)
        await torrent.recover_peers()
        await torrent.connect_peers()
        # await torrent.close_trackers()
        print(torrent)
        await torrent.close()
        del torrent

    except Exception as e:
        print(f"An error occurred: {e}")
        return

if __name__ == "__main__":
    asyncio.run(async_main())
    