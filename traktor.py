from testing import *
#get songs from NML File
import xml.etree.ElementTree as ET

unneeded_fields = ['DIR', 'FILE', 'FILESIZE', 'VOLUME', 'VOLUMEID','TRACK','AUTHOR_TYPE','BITRATE','COVERARTID', 'PLAYTIME',
'PLAYTIME_FLOAT', 'RELEASE_DATE','FLAGS','BPM_QUALITY','PEAK_DB', 'PERCEIVED_DB','ANALYZED_DB']
unneeded_tags = ['CUE', 'CUE_V2','LOCATION','LOUDNESS', 'MODIFICATION_INFO', "FLAGS", "STEMS", "SAMPLE_TYPE_INFO"]


def replace_int_with_id(currentKey, song, songDict):
    songDict[song.CATALOG_NO] = songDict[currentKey]
    print ("current key: " + str(currentKey))
    songDict.pop(currentKey)
 

#Takes a Traktor NML file and converts each song into a Song Object
def create_songs_from_file(file):
    tree = ET.parse(file)
    root = tree.getroot()
    traktorSongs = {}
    for num,entry in enumerate(root[2]):
        songDict = {}
        title = entry.attrib['TITLE']
        songDict['TITLE'] = title
        try: 
            artist = entry.attrib['ARTIST']
            songDict['ARTIST'] = artist
        except:
            artist = "None"
            songDict['ARTIST'] = artist
        #for x in entry:
        for attributeSection in entry:
            if attributeSection.tag in unneeded_tags:
                pass
            else:
                #songDict[attributeSection.tag] = {}
                for value in attributeSection.attrib:
                    if value in unneeded_fields:
                        pass
                    else:
                        if attributeSection.tag == "ALBUM" or attributeSection.tag == "MUSICAL_KEY" or attributeSection.tag == "TEMPO":
                            songDict[attributeSection.tag] = attributeSection.attrib[value]
                        else:
                            songDict[value] = attributeSection.attrib[value]
        traktorSongs[num] = Song(songDict)
    listToCheck = list_of_songs_with_attr(traktorSongs, 'CATALOG_NO')
    for item in listToCheck:
        replace_int_with_id(item, traktorSongs[item], traktorSongs)
    return traktorSongs

#     print(x.attrib) #BITRATE, GENRE, LABEL, RANKING, KEY, COMMENT, PLAYCOUNT, PLAYTIME, PLAYTIME_FLOAT, IMPORT_DATE, LAST_PLAYED, RELEASE_DATE


#looks through NML and finds all songs by a specific artist
def find_artist(artist):
    artistSongs = root[2].findall('./ENTRY/[@ARTIST="'+ artist + '"]') #Sub root[2] with variable
    return artistSongs

def find_song(songList, title): ### This does not work as-is since findall is specificall for an Element Tree element - can use on each song in list
    output = songList.findall('./ENTRY/[@TITLE="' + title + '"]')
    return output

#this find a particular artist/song combo and updates a given field - currently only comment
def update_traktor(fileToUpdate, searchArtist, searchSong, field, value, overwrite):
    tree = ET.parse(fileToUpdate)
    root = tree.getroot()
    for item in root[2]:
        try:
            if fuzz.token_set_ratio(item.attrib['ARTIST'], searchArtist) > 90 and fuzz.token_set_ratio(item.attrib['TITLE'], searchSong) > 90:
                print (item.attrib['TITLE'] + ":  " + item.attrib['ARTIST'])
                info = item.find('INFO')
                try:
                    testing = info.get(field)
                except:
                    testing = value
                print (testing)
                if isinstance(testing, NoneType) or overwrite == True:
                    print ("setting comment")
                    info.set(field,  value)
                else:
                    print (type(testing))
                    print ("not a match")
                    testing = testing + " " + value
                    info.set(field, testing)
                #print (testing)
            else:
                "here?"
                pass
        except:
            #print ("Whoops")
            pass
    tree.write(fileToUpdate)

#Initializes different dictionaries
def load_things():
    songs = get_items_from_file('songs.json')
    playlists = get_items_from_file('playlists.json')
    songs = dict_to_objects(songs, 'songs')
    playlists = dict_to_objects(playlists, 'playlists')
    traktorSongs = get_items_from_file('new_traktor_format.json')
    traktorSongs = dict_to_objects(traktorSongs, 'songs')
    return songs, playlists, traktorSongs

def find_spotify_version(traktorSong, spotifyDict):
    for key, item in spotifyDict.items():
        if fuzz.token_set_ratio(traktorSong.ARTIST, item.artist) > 90 and fuzz.token_set_ratio(traktorSong.TITLE, item.title) > 90:
            pprint.pprint(item.__dict__)
            return item

#I'd like to grab the missing spotify IDs from spotify itself for cleaner data and a better comparison
#Ran into an issue where songs were not easily searchable. 
#def get_missing_spotify_ID(traktorSong)


def copy_attribute(inputSong, attribute, outputSong, newAttribute):
    toBeCopied = getattr(inputSong, attribute)
    setattr(outputSong, newAttribute, toBeCopied)

def write_genre(traktorDict, songDict):
    for key, item in traktorDict.items():
        try:
            copy_attribute(item, "GENRE", find_spotify_version(item, songDict), "GENRE")    
        except:
            pass    
#quick load of traktor songs and spotify songs
def test():
    test = create_songs_from_file('duplicated.nml')
    songs = get_items_from_file('songs.json')
    songs = dict_to_objects(songs, 'songs')
    #spotifize(test)
    return test, songs



def write_spotify_ID(traktorDict, spotifyDict):
    for key, item in traktorDict.items():
        try:
            copy_attribute(find_spotify_version(traktorDict[key], spotifyDict),'songID',traktorDict[key], 'CATALOG_NO')
            update_traktor('duplicated.nml', item.ARTIST, item.TITLE, 'CATALOG_NO', item.CATALOG_NO, True)
        except:
            pass