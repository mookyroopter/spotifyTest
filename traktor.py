from testing import *
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
#get songs from NML File
import xml.etree.ElementTree as ET
tree = ET.parse('TestExport.nml')
root = tree.getroot()
unneeded_fields = ['DIR', 'FILE', 'FILESIZE', 'VOLUME', 'VOLUMEID','TRACK','AUTHOR_TYPE','BITRATE','COVERARTID', 'PLAYTIME',
'PLAYTIME_FLOAT', 'RELEASE_DATE','FLAGS','BPM_QUALITY','PEAK_DB', 'PERCEIVED_DB','ANALYZED_DB']
unneeded_tags = ['CUE', 'CUE_V2','LOCATION','LOUDNESS', 'MODIFICATION_INFO', "FLAGS", "STEMS", "SAMPLE_TYPE_INFO"]




#Takes a Traktor NML file and converts each song into a Song Object
def create_songs_from_file():
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
                        #songDict[attributeSection.tag][value] = attributeSection.attrib[value]
                        else:
                            songDict[value] = attributeSection.attrib[value]
                        # - This would be nice to flatten the elements, but TITLE (song)
                        #is overwritten by TITLE(album)
                        #MUSICAL_KEY is written as VALUE

        traktorSongs[num] = Song(songDict)
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
def update_traktor(searchArtist, searchSong, field, info, overwrite):
    for item in root[2]:
        try:
            if item.attrib['ARTIST'] == searchArtist and item.attrib['TITLE'] == searchSong:
                print (item.attrib['TITLE'] + ":  " + item.attrib['ARTIST'])
                info = item.find('INFO')
                testing = info.get(field)
                print (testing)
                if isinstance(testing, NoneType) or overwrite == True:
                    print ("setting comment")
                    info.set(field,  info)
                else:
                    print (type(testing))
                    print ("not a match")
                    testing = testing + " " + info
                    info.set(field, testing)
                #print (testing)
            else:
                "here?"
                pass
        except:
            #print ("Whoops")
            pass
    tree.write('duplicated.nml')

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
        if fuzz.partial_ratio(traktorSong.ARTIST, item.artist) > 90 and fuzz.partial_ratio(traktorSong.TITLE, item.title) > 90:
            pprint.pprint(item.__dict__)
            return item

def copy_attribute(inputSong, attribute, outputSong, newAttribute):
    toBeCopied = getattr(inputSong, attribute)
    setattr(outputSong, newAttribute, toBeCopied)

def test():
    test = create_songs_from_file()
    #spotifize(test)
    return test
