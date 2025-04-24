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
    
    def __str__(self):
        return f"Torrent file: {self.filename}\n" \
               f"Announce: {self.announce}\n" \
               f"Announce List: {self.announce_list}\n" \
               f"Comment: {self.comment}\n" \
               f"Piece Length: {self.piece_length}\n" \
               f"nb Pieces: {len(self.piece_hashes)}\n" \
               f"Created By: {self.created_by}\n" \
               f"Creation Date: {self.creation_date}\n" \
               f"Name: {self.name}\n" \
                f"Files: {self.files}\n" \
            #    f"Info Hash: {self.info_hash}\n" \
            #    f"Encoding: {self.encoding}\n"
    
    def decode_file(self):
        import bencodepy
        with open(self.filename, 'rb') as f:
            self.torrent = bencodepy.decode(f.read())
        self.info_hash = self.torrent[b'info'][b'pieces']
        self.piece_length = self.torrent[b'info'][b'piece length']
        self.pieces = self.torrent[b'info'][b'pieces']
        self.piece_hashes = [self.pieces[i:i+20] for i in range(0, len(self.pieces), 20)]
        self.announce = self.torrent[b'announce']
        if b'announce-list' in self.torrent:
            self.announce_list = self.torrent[b'announce-list']
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


def main():
    from pprint import pprint
    torrent_file = torrent('Revolt_of_the_Zombies.avi.torrent')
    print(torrent_file)

if __name__ == "__main__":
    main()
