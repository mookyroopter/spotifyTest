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
    def remove_element(self, element):
        try:
            delattr(self, element)
        except AttributeError:
            for item in dir(self):
                print ('item in dir: ' + item)
                try:
                    print ("Deleting in class: " + getattr(self, item)[element])
                    getattr(self,item).pop(element)
                    print ("it popped")
                except:
                    print ("that didn't work")
            #for value in self:
            #    try:
            #        self.value.pop(element)
            #    except:
            #        print ("couldn't pop " + element + " from " + value)