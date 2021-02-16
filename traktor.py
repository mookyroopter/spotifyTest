from testing import *
#get songs from NML File
tree = ET.parse('TestExport.nml')
root = tree.getroot()
traktorSongs = {}


def create_songs_from_file():
    for num,entry in enumerate(root[2]):
        songDict = {}
        title = entry.attrib['TITLE']
        songDict['title'] = title
        try: 
            artist = entry.attrib['ARTIST']
            songDict['artist'] = artist
        except:
            artist = "None"
            songDict['artist'] = artist
        for x in entry:
            if x.tag == "ALBUM":
                try: 
                    songDict['album'] = x.attrib['TITLE']
                except:
                    songDict['album'] = "No Album"
            if x.tag == "INFO":
                try: 
                    songDict['genre'] = x.attrib['GENRE']
                except:
                    songDict['genre'] = "None"
                try:
                    songDict['ranking'] = x.attrib['RANKING']
                except:
                    songDict['ranking'] = "None"
                try:
                    songDict['comment'] = x.attrib['COMMENT']
                except:
                    songDict['comment'] = "None"
                try:
                    songDict['key'] = x.attrib['KEY']
                except:
                    songDict['key'] = "None"
                try:
                    songDict['import_date'] = x.attrib['IMPORT_DATE']
                except:
                    songDict['import_date'] = "None"
                try: 
                    songDict['playcount'] = x.attrib['PLAYCOUNT']
                except:
                    songDict['playcount'] = "0"
                try:
                    songDict['color'] = x.attrib['COLOR']
                except:
                    songDict['color'] = "None"
            if x.tag == "TEMPO":
                try:
                    songDict['tempo'] = x.attrib['BPM']
                except:
                    songDict['tempo'] = "None"
        traktorSongs[num] = Song(songDict)

def clean_fields():
    for key,item in traktorSongs.items():
        try:
            test = item.album
        except:
            print("No album for: " + item.title)
            item.album = "None"
        try:
            test = item.genre
        except:
            print("No genre for: " + item.title)
            item.genre = "None"
        try:
            test = item.ranking
        except:
            print("No ranking for:" + item.title)
            item.ranking = "0"
        try:
            test = item.comment
        except:
            print("No Comments on: " + item.comment)
            item.comment = ""
        try:
            test = item.key
        except:
            print("No key for: " + item.key)
            item.key = "None"
        try:
            test = item.import_date
        except:
            print(item.title + " was never imported")
            item.import_date = ""
        try:
            test = item.tempo
        except:
            print(item.title + " has no tempo")
            item.tempo = "None"
        try:
            test = item.playcount
        except:
            print(item.title + " has never been played")
            item.playcount = "0"
        try:
            test = item.color
        except:
            print("No color for " + item.title)
            item.color = "None"

#def run():
#test = get_items_from_file('songs.json')
#converted = dict_to_objects(test, 'tracks')

#def find_in_spotify(trackname)
    
#     print(x.attrib) #BITRATE, GENRE, LABEL, RANKING, KEY, COMMENT, PLAYCOUNT, PLAYTIME, PLAYTIME_FLOAT, IMPORT_DATE, LAST_PLAYED, RELEASE_DATE



