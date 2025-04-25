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
        if self.info_hash:
            informations.append(f"Info Hash: {self.info_hash.hex()}")
        else:
            informations.append("Info Hash: No info hash found")
        return "\n".join(informations)
    
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
                        if peers:
                            self.peers.extend(peers)
                            print(f"Found {len(peers)} peers from {url}")
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


def main():
    try:
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        torrent_dir = os.path.join(base_dir, 'torrents')
        if not os.path.exists(torrent_dir):
            os.makedirs(torrent_dir)
        torrent_file = os.path.join(torrent_dir, 'Revolt_of_the_Zombies.avi.torrent')
        torrent_file = torrent(torrent_file)
        torrent_file.contact_trackers()
        torrent_file.close_tracker()
        print("Torrent file information:")
        print(torrent_file)
    except Exception as e:
        print(f"Error: {e}")
        print("Please check the torrent file and try again.")

if __name__ == "__main__":
    main()
