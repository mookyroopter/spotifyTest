import json
from spotifyCreds import *
from classes import *

def get_items_from_file(file):
    with open(file, 'r') as json_file:
        data = json.load(json_file, object_hook=dict)
    return data

def write_songs(songs, file):
    new_output = {}
    for key, item in songs.items():
        if isinstance(item, Song):
            new_output[key] = jsonify(item) 
        if isinstance(item, dict):
            new_output[key] = item
    with open (file, 'w') as outfile:
        json.dump(new_output,outfile,indent=4)

def print_all_playlists(playlistDict):
    for key, value in playlistDict.items():
        print(value.name + ":  " + value.id)

def get_playlist_id(playlistName, playlistDict):
    output = "None"
    for key, value in playlistDict.items():
        if value.name == playlistName:
            output = value.id
    print (output)


def get_playlists_from_file(playlistFile):
    myplaylists = get_items_from_file('playlists.json')
    playlistDict = {}
    for key, value in myplaylists.items():
        playlistDict[value['id']] = Playlist(value['id'], value['name'], value['uri'], value['total'])
    return playlistDict


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
                songDict = {'title': item['name'], 'artist': item['artists'][0]['name'], 'songID': item['id'], 'artistId': item['artists'][0]['id']}
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
            songDict = {'title': item['name'], 'artist': item['artists'][0]['name'], 'songID': item['id'], 'artistId': item['artists'][0]['id']}
            songDict['popularity'] = item['popularity']
            songDict['features'] = sp.audio_features(item['id'])[0]
            curSong = Song(songDict)
            curSong.spotifyPlaylists.append(playlist)
            curSong.extract_features()
            all_songs[item['id']] = curSong               
    return all_songs



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
