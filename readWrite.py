import json
from spotifyCreds import *
from classes import *

#turns an object into a dictionary
def jsonify(item):
    item = item.__dict__
    return item

#gets a dictionary from a json file
def get_items_from_file(file):
    with open(file, 'r') as json_file:
        data = json.load(json_file, object_hook=dict)
    return data

#overwrites current songs (dict and filename as inputs)
def write_songs(songs, file):
    new_output = {}
    for key, item in songs.items():
        if isinstance(item, Song):
            new_output[key] = jsonify(item) 
        if isinstance(item, dict):
            new_output[key] = item
    with open (file, 'w') as outfile:
        json.dump(new_output,outfile,indent=4)

#prints number, title, and id of all saved playlists (input is Dictionary of playlist objects)
def print_all_playlists(playlistDict):
    i = 0
    for key, value in playlistDict.items():
        print(str(i) + ".  " + value.name + ":  " + value.id)
        i += 1

#uses the playlist name and dictionary of playlist objects to find playlist ID
def get_playlist_id(playlistName, playlistDict):
    output = "None"
    for key, value in playlistDict.items():
        if value.name == playlistName:
            output = value.id
    print (output)

#pulls all playlists from Json file into a dictionary, converts them to playlists objects
def get_playlists_from_file(playlistFile):
    myplaylists = get_items_from_file('playlists.json')
    playlistDict = {}
    for key, value in myplaylists.items():
        playlistDict[value['id']] = Playlist(value['id'], value['name'], value['uri'], value['total'])
    return playlistDict

#searches spotify to find all songs in a particular playlist
def get_songs_from_playlist(playlist):
    print('getting songs from playlist: ' + playlist)
    all_songs = {}
    playlist_songs = sp.playlist_items(playlist,fields="items.track.id,total,tracks,uri",additional_types=['track'])
    total_songs = playlist_songs['total']
    if total_songs >= 50:
        length_of_last = 50
        offset = 0
        while length_of_last == 50:
            song_list = []
            partial_songs = sp.playlist_items(playlist, limit=length_of_last, offset=offset, fields="items.track.id,total,tracs,uri",additional_types=['track'])
            this_segement_length = len(partial_songs['items'])
            for i, item in enumerate(partial_songs['items']):
                if item['track'] == None:
                    print("NoneType")
                else:
                    song_list.append(item['track']['id']) 
            trackInfo = sp.tracks(song_list)
            for num, item in enumerate(trackInfo['tracks']):
                songDict = {}
                songDict = {'TITLE': item['name'], 'ARTIST': item['artists'][0]['name'], 'CATALOG_NO': item['id'], 'artistId': item['artists'][0]['id']}
                songDict['popularity'] = item['popularity']
                songDict['features'] = sp.audio_features(item['id'])[0]
                curSong = Song(songDict)
                curSong.spotifyPlaylists.append(playlist)
                curSong.extract_features()
                all_songs[item['id']] = curSong
            offset = offset + length_of_last
            if this_segement_length <= 50:
                length_of_last = 0
            else:
                length_of_last = 50
    else:
        song_list = []
        for i, item in enumerate(playlist_songs['items']):
            if item['track'] == None:
                print("NoneType")
            else:
                song_list.append(item['track']['id']) 
        trackInfo = sp.tracks(song_list)
        for num, item in enumerate(trackInfo['tracks']):
            songDict = {}
            songDict = {'TITLE': item['name'], 'ARTIST': item['artists'][0]['name'], 'CATALOG_NO': item['id'], 'artistId': item['artists'][0]['id']}
            songDict['popularity'] = item['popularity']
            songDict['features'] = sp.audio_features(item['id'])[0]
            curSong = Song(songDict)
            curSong.spotifyPlaylists.append(playlist)
            curSong.extract_features()
            all_songs[item['id']] = curSong               
    return all_songs

#finds differences between saved and current playlists (finds new, and looks at length)
def check_for_updates(playlistFile, spotifyPlaylists):
    playlists_to_update = []
    for key,item in playlistFile.items():
        if key in spotifyPlaylists and spotifyPlaylists[key]['total'] == playlistFile[key].total:
            print("same")
        else:
            playlists_to_update.append(key)
    return playlists_to_update

#This will update songs in json file for:
    #reset - all songs
    #all - uses check for updates and quickly finds differences to update only what's needed
    #list or id - refreshes playlists in a given list
def refresh_songs_from_spotify(input):
    try:
        current_songs = get_items_from_file('songs.json')
    except:
        current_songs = {}
    current_playlists = get_playlists_from_file('playlists.json')
    myplaylists = get_all_playlists_from_spotify()
    if input == "reset":
        num = 0
        for playlistID in myplaylists:
            print (playlistID + ":  " + str(myplaylists[playlistID]['total']) + " tracks")
            songs_to_write = get_songs_from_playlist(playlistID)
            for songID, values in songs_to_write.items():
                if songID in current_songs:
                    if playlistID in values.spotifyPlaylists:
                        pass
                    else:
                        current_songs[songID]['spotifyPlaylists'].append(playlistID)
                else:
                    current_songs[songID] = songs_to_write[songID] 
            num += 1
            if num % 10 == 0:
                write_songs(current_songs, 'songs.json')         
        write_songs(current_songs, 'songs.json')
    elif input == "all":
        playlists_to_update = check_for_updates(current_playlists, myplaylists)
        for playlistID in playlists_to_update:
            print (playlistID + ":  " + str(current_playlists[playlistID].total) + " tracks")
            songs_to_write = get_songs_from_playlist(playlistID)
            for songID,values in songs_to_write.items():
                if songID in current_songs:
                    if playlistID in current_songs[songID]['spotifyPlaylists']:
                        print ("already exists")
                    else:
                        current_songs[songID]['spotifyPlaylists'].append(playlistID)
                else:
                    current_songs[songID] = songs_to_write[songID]
        write_songs(current_songs, 'songs.json')
    elif type(input) == list:
        for item in input:
            songs_to_write = get_songs_from_playlist(item)
            for songID,values in songs_to_write.items():
                if songID in current_songs:
                    try:
                        if item in current_songs[songID]['spotifyPlaylists']:
                            print ("already exists")
                        else:
                            current_songs[songID]['spotifyPlaylists'].append(item)
                    except TypeError:
                        if item in current_songs[songID].spotifyPlaylists:
                            print("already exists")
                        else:
                            current_songs[songID].spotifyPlaylists.append(item)
                else:
                    current_songs[songID] = songs_to_write[songID]
        write_songs(current_songs, 'songs.json')
        
        print ("it's a list!")
    else:
        print("Not sure what's happening")

#prints songs in a playlist
def playlist_songs(playlist):
    playlistSongs = get_songs_from_playlist(playlist)
    for key,value in playlistSongs.items():
        try:
            print(value['title'] + "(" + value['songID'] + ") -- " + value['artist'] + ":  " + value['artistId'])
        except TypeError:
            print(value.title + "(" + value.songID + ") -- " + value.artist + ":  " + value.artistId)

#finds songs from Json file that have particular attributes -- Currently only used for playlists(energy, danceability, artist, genre, etc)
def find_songs_by_attr(songDict, attr, value):
    output = {}
    if attr == "playlist":
        for key,item in songDict.items():
            if value in item.spotifyPlaylists:
                output[item.songID] = item
    else:
        for key, item in songDict.items():
            if hasattr(item, attr) and getattr(item, attr) == value:
                output[item.songID] = item
    return output

#given a list of features, find the average value
def list_average(inputList):
    sum = 0
    amount = len(inputList)
    for item in inputList:
        sum + item
    average = sum / amount
    return average

def list_of_songs_with_attr(songDict, attr):
    output = []
    for key, item in songDict.items():
        if hasattr(item, attr):
            output.append(key)
        else:
            pass
    return output
