class Playlist:
    def __init__(self, id, name, uri, total):
        self.id = id
        self.name = name
        self.uri = uri
        self.total = total
        songs = {}

class Song:
    def __init__(self, dictionary):
        self.spotifyPlaylists = []
        if str(type(dictionary)) == "<class 'str'>":
            dictionary = json.loads(dictionary)
        for key in dictionary.keys():
            setattr(self, key, dictionary[key])
    def extract_features(self):
        self.key = self.features['key']
        self.tempo = self.features['tempo']
        self.mode = self.features['mode']