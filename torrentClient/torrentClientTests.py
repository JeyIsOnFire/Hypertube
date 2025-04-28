import logging
class torrent():
    def __init__(self, filename):
        self.filename = filename
        self.torrent = None
        self.info_hash = None
        self.piece_length = None
        self.pieces = None
        self.announce = None
        self.announce_list = None
        self.comment = None
        self.created_by = None
        self.creation_date = None
        self.encoding = None
        self.name = None
        self.piece_hashes = None
        self.files = None
        self.decode_file()
        self.peer_id = self.generate_peer_id()
        self.peers = []
        self.peers_connected = []
        self.log("Torrent file loaded successfully, starting process...")
        self.start_process()
    
    def __str__(self):
        informations = []
        informations.append(f"Torrent file: {self.filename}")
        if self.announce_list:
            informations.append("Announce List:")
            for i in range(len(self.announce_list)):
                informations.append(f"  = Announce available on {i + 1} group")
                for announce in self.announce_list[i]:
                    informations.append(f"    - {announce}")
        else:
            informations.append("Announce List: No announce list provided")
        if self.comment:
            informations.append(f"Comment: {self.comment}")
        else:
            informations.append("Comment: No comment Found")
        informations.append(f"Piece Length: {self.piece_length}")
        informations.append(f"nb Pieces: {len(self.piece_hashes)}")
        if self.created_by:
            informations.append(f"Created By: {self.created_by}")
        else:
            informations.append("Created By: No creator found")
        if self.creation_date:
            informations.append(f"Creation Date: {self.creation_date}")
        else:
            informations.append("Creation Date: No creation date found")
        if self.name:
            informations.append(f"Name: {self.name}")
        else:
            informations.append("Name: No name found")
        if self.files:
            informations.append(f"Files: {self.files}")
        else:
            informations.append("Files: This torrent contains only one file")
        if self.peer_id:
            informations.append(f"Peer ID: {self.peer_id}")
        if self.peers:
            informations.append(f"Peers: {self.peers}")
        else:
            informations.append("Peers: No peers known, please check the tracker")
        if self.peers_connected:
            informations.append(f"Connected Peers: {self.peers_connected}")
        else:
            informations.append("Connected Peers: No peers connected")
        if self.info_hash:
            informations.append(f"Info Hash: {self.info_hash.hex()}")
        else:
            informations.append("Info Hash: No info hash found")
        return "\n".join(informations)

    def __repr__(self):
        return self.__str__()
    
    def __del__(self):
        return self.stop_torrent()

    def decode_file(self):
        import bencodepy
        import hashlib
        import os
        if not self.filename.endswith('.torrent'):
            raise ValueError("File is not a torrent file")
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"File {self.filename} does not exist")
        if not os.path.isfile(self.filename):
            raise IsADirectoryError(f"File {self.filename} is a directory")
        with open(self.filename, 'rb') as f:
            self.torrent = bencodepy.decode(f.read())
        self.info_hash = hashlib.sha1(bencodepy.encode(self.torrent[b'info'])).digest()
        self.piece_length = self.torrent[b'info'][b'piece length']
        self.pieces = self.torrent[b'info'][b'pieces']
        self.piece_hashes = [self.pieces[i:i+20] for i in range(0, len(self.pieces), 20)]
        if b'announce-list' in self.torrent:
            self.announce_list = self.torrent[b'announce-list']
        else:
            self.announce_list = []
        if b'announce' in self.torrent:
            announce = self.torrent[b'announce']
            if [announce] not in self.announce_list:
                self.announce_list.append([announce])
        if b'comment' in self.torrent:
            self.comment = self.torrent[b'comment']
        if b'created by' in self.torrent:
            self.created_by = self.torrent[b'created by']
        if b'creation date' in self.torrent:
            self.creation_date = self.torrent[b'creation date']
        # self.encoding = self.torrent[b'encoding']
        if b'name' in self.torrent[b'info']:
            self.name = self.torrent[b'info'][b'name']
        if b'files' in self.torrent[b'info']:
            self.files = self.torrent[b'info'][b'files']
    
    def generate_peer_id(self, prefix='-PC0001-'):
        import random
        import string
        peer_id = prefix
        if len(peer_id) != 8:
            raise ValueError("Peer ID must be 8 characters long")
        peer_id += ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        return peer_id
    
    def contact_trackers(self):
        import bencodepy
        import requests
        import time
        if not self.announce_list:
            raise ValueError("No announce list found")
        
        for group in self.announce_list:
            if self.peers is not None and len(self.peers) > 0:
                break
            for url in group:
                try:
                    response = requests.get(url, params={
                        'info_hash': self.info_hash,
                        'peer_id': self.peer_id,
                        'port': 6881,
                        'uploaded': 0,
                        'downloaded': 0,
                        'left': 0,
                        'compact': 1,
                        'event': 'started'
                    })
                    if response.status_code == 200:
                        # Traiter la réponse
                        data = response.content
                        peers = self.parse_peers(data)
                        self.log(f"Peers found: {peers} on {url}")
                        if peers:
                            self.peers.extend(peers)
                    else:
                        print(f"Failed to contact tracker: {url} - Status code: {response.status_code}")
                except requests.RequestException as e:
                    print(f"Error contacting tracker {url}: {e}")
                time.sleep(1)

    def close_tracker(self):
        import bencodepy
        import requests
        import time
        if not self.announce_list:
            raise ValueError("No announce list found")
        
        for announce in self.announce_list:
            for url in announce:
                try:
                    response = requests.get(url, params={
                        'info_hash': self.info_hash,
                        'peer_id': self.peer_id,
                        'port': 6881,
                        'uploaded': 0,
                        'downloaded': 0,
                        'left': 0,
                        'compact': 1,
                        'event': 'stopped'
                    })
                    if response.status_code == 200:
                        data = response.content
                        peers = self.parse_peers(data)
                        if peers:
                            self.peers = peers
                    else:
                        print(f"Failed to contact tracker: {url} - Status code: {response.status_code}")
                except requests.RequestException as e:
                    print(f"Error contacting tracker {url}: {e}")
                time.sleep(1)

    def parse_peers(self, data):
        import bencodepy
        response = bencodepy.decode(data)
        peers = response.get(b'peers', [])
        if len(peers) % 6 == 0:  # Format compact, chaque peer fait 6 octets
            parsed_peers = []
            for i in range(0, len(peers), 6):
                peer = peers[i:i+6]
                ip = '.'.join(map(str, peer[:4]))  # Les 4 premiers octets pour l'IP
                port = (peer[4] << 8) + peer[5]  # Les 2 derniers octets pour le port
                parsed_peers.append((ip, port))
            return parsed_peers
        return []

    def connect_peer(self, peer: tuple):
        """
        Connect to a single peer using the socket module.
        """
        import socket
        if not isinstance(peer, tuple):
            raise TypeError("Peer must be a tuple")
        if len(peer) != 2:
            raise ValueError("Peer must be a tuple of (ip, port)")
        if not isinstance(peer[0], str):
            raise TypeError("IP must be a string")
        if not isinstance(peer[1], int):
            raise TypeError("Port must be an integer")
        if not (0 <= peer[1] <= 65535):
            raise ValueError("Port must be between 0 and 65535")
        ip, port = peer
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # Timeout de 5 secondes
            sock.connect((ip, port))
            peer_save = (ip, port, sock)
            self.peers_connected.append(peer_save)
            self.log(f"Connected to peer {ip}:{port}")
        except socket.error as e:
            self.log(f"Error connecting to peer {ip}:{port} - {e}")

    def connect_peers(self):
        """
        Connect to peers using the socket module and using the multithreaded module.
        """
        import socket
        import threading
        if not self.peers:
            raise ValueError("No peers found")
        
        threads = []
        for peer in self.peers:
            thread = threading.Thread(target=self.connect_peer, args=(peer,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def stop_torrent(self):
        self.log("Stopping torrent...")
        self.close_tracker()
        self.log("Tracker closed")
        while self.peers_connected:
            peer = self.peers_connected.pop()
            ip, port, sock = peer
            try:
                sock.close()
                self.log(f"Disconnected from peer {ip}:{port}")
            except Exception as e:
                print(f"Error disconnecting from peer {ip}:{port} - {e}")

        self.peers_connected = []
        self.peers = []
        self.log("Torrent stopped")

    def start_process(self):
        self.log("Starting process...")
        self.log("Contacting trackers...")
        self.contact_trackers()
        self.log("Trackers contacted, waiting for peers...")
        if not self.peers:
            raise ValueError("No peers found")
        self.connect_peers()
        self.log("Connected to peers")
        if not self.peers_connected:
            raise ValueError("No peers connected")
        self.log("Process started successfully")

    def log(self, message: str = ""):
        if not message:
            raise ValueError("Message cannot be empty")
        if not isinstance(message, str):
            raise TypeError("Message must be a string")
        if not self.name:
            raise ValueError("Torrent name is not set")
        print(f"TORRENT_LOG: {self.name} - {message}")


def main():
    try:
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        torrent_dir = os.path.join(base_dir, 'torrents')
        if not os.path.exists(torrent_dir):
            os.makedirs(torrent_dir)
        torrent_file = os.path.join(torrent_dir, 'Child_Bride.avi.torrent')
        try:
            torrent_file = torrent(torrent_file)
            del torrent_file
        except Exception as e:
            print(f"Error: {e}")
            print("Please check the torrent file and try again.")
    except Exception as e:
        print(f"Error: {e}")
        print("Please check the torrent file and try again.")

if __name__ == "__main__":
    main()
