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

    async def handshake(self):
        try:
            print(f"Connecting to peer {self.ip}:{self.port} for handshake...")
            # Send handshake message
            handshake_message = b'\x13BitTorrent protocol\x00\x00\x00\x00\x00\x00\x00\x00' + self.torrent_infos["hash"] + self.torrent_infos["peer_id"].encode('utf-8')
            self.writer.write(handshake_message)
            await self.writer.drain()
            self.status = "handshake sent"
            print(f"Handshake sent to {self.ip}:{self.port}. Waiting for response...")
            
            # Wait for response
            response = await self.reader.read(68)  # 68 bytes for handshake response
            if len(response) < 68:
                raise ValueError("Invalid handshake response.")
            self.status = "connected"
        except Exception as e:
            self.status = "disconnected"
            raise e

    async def connect(self):
        try:
            print(f"Connecting to peer {self.ip}:{self.port}...")
            self.reader, self.writer = await asyncio.wait_for(
                asyncio.open_connection(self.ip, self.port),
                timeout=10
            )
            self.status = "waiting for handshake"
            await self.handshake()
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
        self.origin = {}
        if file_name is not None:
            if not isinstance(file_name, str):
                raise TypeError("file_name must be a string.")
            if len(file_name) == 0:
                raise ValueError("file_name cannot be empty.")
            if not file_name.endswith(".torrent"):
                raise ValueError("file_name must end with .torrent.")
            if not os.path.exists(os.path.join(os.path.dirname(__file__), "torrents", file_name)):
                raise FileNotFoundError(f"Torrent file {file_name} does not exist.")
            self.origin["type"] = "torrent_file"
            self.origin["file_name"] = file_name
        elif magnet_link is not None:
            if not isinstance(magnet_link, str):
                raise TypeError("magnet_link must be a string.")
            if len(magnet_link) == 0:
                raise ValueError("magnet_link cannot be empty.")
            if not magnet_link.startswith("magnet:"):
                raise ValueError("magnet_link must start with 'magnet:'.")
            self.origin["type"] = "magnet_link"
            self.origin["magnet_link"] = magnet_link
        self.torrent_infos = {}
        self._init_torrent_infos()
        if self.origin["type"] == "torrent_file":
            self.torrent_file_path = os.path.join(os.path.dirname(__file__), "torrents", self.origin["file_name"])
            if not os.path.exists(self.torrent_file_path):
                raise FileNotFoundError(f"Torrent file {self.torrent_file_path} does not exist.")
            self._parse_torrent_file()
        elif self.origin["type"] == "magnet_link":
            self._parse_magnet_link()
    def __str__(self):
        infos = [
            "Torrent File Information:",
            "Torrent Origin: " + str(self.origin),
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

    def _init_torrent_infos(self):
        import random
        import string
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

    def _parse_torrent_file(self):
        import bencodepy
        import hashlib
        import os
        try:
            with open(self.torrent_file_path, 'rb') as f:
                torrent_data = bencodepy.decode(f.read())
            if b'info' not in torrent_data:
                raise ValueError("Invalid torrent file format.")
            if b'meta version' in torrent_data[b'info'] and torrent_data[b'info'][b'meta version'] != 1:
                raise ValueError("Unsupported torrent file meta version.")
            self.torrent_infos["hash"] = hashlib.sha1(bencodepy.encode(torrent_data[b'info'])).digest() 
            if b'name' not in torrent_data[b'info']:
                raise ValueError("Torrent file does not contain a name.")
            self.torrent_infos["name"] = torrent_data[b'info'][b'name']
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
    
    def _parse_magnet_link(self):
        from urllib.parse import urlparse, parse_qs
        import binascii
        parsed = urlparse(self.origin["magnet_link"])
        if parsed.scheme != "magnet":
            raise ValueError("Invalid magnet link scheme, must be 'magnet'.")
        params = parse_qs(parsed.query)
        if 'xt' not in params or not params['xt']:
            raise ValueError("Magnet link must contain 'xt' parameter.")
        xt_value = params['xt']
        if type(xt_value) is not list:
            raise ValueError("Magnet link 'xt' parameter must be a list.")
        if len(xt_value) > 1 or len(xt_value) == 0:
            raise ValueError("Magnet link 'xt' parameter must contain only one value.")
        xt_value = xt_value[0]
        if not xt_value.startswith("urn:btih:"):
            raise ValueError("Magnet link 'xt' parameter must start with 'urn:btih:'.")
        xt_value = xt_value[len("urn:btih:"):]
        if len(xt_value) != 40:
            raise ValueError("Magnet link 'xt' value must be 40 characters long.")
        self.torrent_infos["hash"] = binascii.unhexlify(xt_value.encode('utf-8'))
        if not 'tr' in params:
            raise ValueError("Magnet link must contain 'tr' parameter with at least one tracker URL.")
        trackers = params['tr']
        if type(trackers) is not list:
            raise ValueError("Magnet link 'tr' parameter must be a list.")
        if len(trackers) == 0:
            raise ValueError("Magnet link 'tr' parameter must contain at least one tracker URL.")
        self.torrent_infos["trackers"]["default"] = trackers[0].encode('utf-8')
        self.torrent_infos["trackers"]["groups"].append([tracker.encode('utf-8') for tracker in trackers])


    def _recover_metadata_from_tracker(self):
        pass

    def _exclude_udp_tracker(self):
        import re
        if self.torrent_infos["trackers"]["default"] is not None:
            if re.search(r"^udp://", self.torrent_infos["trackers"]["default"].decode('utf-8')):
                self.torrent_infos["trackers"]["default"] = None
        for group in self.torrent_infos["trackers"]["groups"]:
            for url in group:
                if re.search(r"^udp://", url.decode('utf-8', errors='ignore')):
                    group.remove(url)

    async def contact_udp_tracker(self, event: str, parsed_url):
        import socket
        import struct
        import random
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)
            transaction_id = random.randint(0, 0xFFFFFFFF)
            action = 0  # Action for 'announce'
            info_hash = self.torrent_infos["hash"]
            peer_id = self.torrent_infos["peer_id"].encode('utf-8')
            port = 6881
            left = self.torrent_infos["size"]
            uploaded = 0
            downloaded = 0
            
            # Build the request packet
            # UDP tracker protocol: first send a connect request to get a connection_id
            # Connect request: protocol_id (8 bytes), action (4 bytes), transaction_id (4 bytes)
            protocol_id = 0x41727101980  # magic constant
            connect_action = 0
            connect_packet = struct.pack('!QII', protocol_id, connect_action, transaction_id)
            sock.sendto(connect_packet, (parsed_url.hostname, parsed_url.port or 80))
            connect_response, _ = sock.recvfrom(4096)
            if len(connect_response) < 16:
                raise ValueError("Invalid connect response from UDP tracker.")
            action_response, transaction_id_response, connection_id = struct.unpack('!IIQ', connect_response[:16])
            if action_response != 0 or transaction_id_response != transaction_id:
                raise ValueError("Failed to get connection_id from UDP tracker.")

            # Announce request: connection_id (8), action (4), transaction_id (4), info_hash (20), peer_id (20), downloaded (8), left (8), uploaded (8), event (4), ip (4), key (4), num_want (4), port (2)
            announce_action = 1
            event_map = {"started": 2, "completed": 1, "stopped": 3}
            event_code = event_map.get(event, 0)
            ip = 0
            key = random.randint(0, 0xFFFFFFFF)
            num_want = -1  # default: -1 for all peers
            port = 6881
            announce_packet = struct.pack(
                '!QII20s20sQQQIIIiH',
                connection_id,
                announce_action,
                transaction_id,
                info_hash,
                peer_id,
                downloaded,
                left,
                uploaded,
                event_code,
                ip,
                key,
                num_want,
                port
            )
            sock.sendto(announce_packet, (parsed_url.hostname, parsed_url.port or 80))
            
            # Receive the response
            response_data, _ = sock.recvfrom(4096)
            if len(response_data) < 16:
                raise ValueError("Invalid response from UDP tracker.")
            
            # Parse the response
            action_response, transaction_id_response = struct.unpack('!II', response_data[:8])
            if action_response != 1:  # Action for 'announce'
                raise ValueError("Unexpected action in UDP tracker response.")
            if transaction_id_response != transaction_id:
                raise ValueError("Transaction ID mismatch in UDP tracker response.")
            
            peers_count = (len(response_data) - 16) // 6
            peers = []
            for i in range(peers_count):
                ip_start = 16 + i * 6
                ip_end = ip_start + 4
                port_start = ip_end
                port_end = port_start + 2
                ip_bytes = response_data[ip_start:ip_end]
                port_bytes = response_data[port_start:port_end]
                ip_address = '.'.join(map(str, ip_bytes))
                port_number = struct.unpack('!H', port_bytes)[0]
                peers.append((ip_address, port_number))
            return peers
        
        except Exception as e:
            print(f"Failed to contact UDP tracker: {e}")
        finally:
            sock.close()

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
                if parsed_url.scheme.lower() not in ['http', 'https', 'udp']:
                    continue
                if parsed_url.scheme.lower() == 'udp':
                    res = await self.contact_udp_tracker(event, parsed_url)
                    if res is not None:
                        response_ret.extend(res)
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
                    if isinstance(data, tuple):
                        self.torrent_infos["peers"]["available"].append(data)
                        continue
                    decoded_data = bencodepy.decode(data)
                    if b'failure reason' in decoded_data:
                        raise ValueError(f"Tracker error: {decoded_data[b'failure reason']}")
                    if b'interval' in decoded_data:
                        if self.torrent_infos["trackers"]["next_contact"] is None:
                            self.torrent_infos["trackers"]["next_contact"] = decoded_data[b'interval']
                        else:
                            self.torrent_infos["trackers"]["next_contact"] = min(self.torrent_infos["trackers"]["next_contact"], decoded_data[b'interval'])
                    if b'peers' in decoded_data:
                        peers = decoded_data[b'peers']
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
    magnet_test =  "magnet:?xt=urn:btih:A3CF436B6C4E243B4A1BCAAD0C5E3787DE814471&dn=White.Zombie.1932.%28Horror%29.1080p.BRRip.x264-Classics&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=UDP%3A%2F%2FEDDIE4.NL%3A6969%2FANNOUNCE&tr=UDP%3A%2F%2FTRACKER.COPPERSURFER.TK%3A6969%2FANNOUNCE&tr=UDP%3A%2F%2FTRACKER.LEECHERS-PARADISE.ORG%3A6969%2FANNOUNCE&tr=UDP%3A%2F%2FTRACKER.OPENTRACKR.ORG%3A1337%2FANNOUNCE&tr=UDP%3A%2F%2FTRACKER.ZER0DAY.TO%3A1337%2FANNOUNCE&tr=udp%3A%2F%2Fexplodie.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=http%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=udp%3A%2F%2Fopentracker.i2p.rocks%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fcoppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.zer0day.to%3A1337%2Fannounce"
    torrent_test = "A Minecraft Movie (2025) [720p] [BluRay] [YTS.MX].torrent"
    # if not user_input:
    #     print("No input provided.")
    #     return
    try:
        # torrent = TorrentFile(magnet_link=magnet_test)
        torrent = TorrentFile(file_name=torrent_test)
        print(torrent)
        await torrent.recover_peers()
        print(torrent)
        await torrent.connect_peers()
        await torrent.close()
        del torrent

    except Exception as e:
        print(f"An error occurred: {e}")
        return

if __name__ == "__main__":
    asyncio.run(async_main())
    