import sys, os
from subprocess import Popen
from time import sleep
from side_scripts import text2int
import requests
import json

music_path = " "
media_player = " "
file_server = " "

media_player_password = " "
file_server_password = " "

url = "http://" + media_player + ":8080/jsonrpc"

def set_music_values(temp, temp2):
    global mixer_record
    global alsaaudio
    mixer_record = temp
    alsaaudio = temp2

# mount the files server on the media player server's directory (if it isn't already)
def mount_server():
    Popen("sshpass -p " + media_player_password + " ssh root@" + media_player + " '[ ! -d \"./media_server/media/music/\" ] && mount -t nfs " + file_server + ":/media/ ./media_server'", shell=True)

# check whether there is an open/playing player running on the media player server
def which_player_open():
    players = json.loads(requests.post(url, json = {'jsonrpc':'2.0','id':1,'method':'Player.GetActivePlayers'}).text)
    if players["result"]:
        return players["result"][0]["type"]

# if there is a running player corresponding with the needed (video or audio) one, then send json to post to append, otherwise to open a new one
def is_server_playing(server_type, file_path):
    num = int(server_type == "video")
    
    if which_player_open() == server_type:
        return {'jsonrpc':'2.0','id':1,'method':'Playlist.Add','params':{'playlistid':num, "item":{"file":file_path}}}
    else:
        return {'jsonrpc':'2.0','id':1,'method':'Player.Open','params':{"item":{"file":file_path}}}

# search for a media file and send post to start playing it
def start(song, is_music):
    search_path = "/home/pi/media_server/"
    mount_server()
    # mount the files server on ruby, if it hasn't already been done
    Popen("[ ! -d \"/home/pi/media_server/music/\" ] && curlftpfs '" + file_server_password + "@" + file_server + ":21/' /home/pi/media_server", shell=True)
    search_term = song.lower()
    if (is_music):
        # search through music files for a specific song/songs
        for root, dirs, files in os.walk(search_path + "music"):
            for file in files:
                if (".ogg" in file or ".mp3" in file) and (search_term in file.lower()):
                    file_path = os.path.join(root, file).replace("/home/pi/media_server", "/storage/media_server")
                
                    requests.post(url, json = is_server_playing("audio", file_path))
    else:
        # search the movie files for a specific film/films
        for root, dirs, files in os.walk(search_path + "movies"):
            for file in files:
                if (".mp4" in file or ".mkv" in file or ".m4v" in file) and (search_term in file.lower()):
                    file_path = os.path.join(root, file).replace("/home/pi/media_server", "/storage/media_server")
                
                    requests.post(url, json = is_server_playing("video", file_path))
        
        # do conversion to "season" and "episode" to search those numbers properly
        search_term = text2int.text2int(search_term)
        for ele in search_term.split(' '):
            if ele.isdigit():
                search_term = search_term.replace(ele + " ", ele.zfill(2))
        if "season" not in search_term and "episode" in search_term:
            search_term = search_term.replace("episode ", "s01e")
        else:
            search_term = search_term.replace("season ", "s").replace("episode ", "e")
        
        # search the show files for a specific episode/episodes
        for root, dirs, files in os.walk(search_path + "shows"):
            for file in files:
                if (".mp4" in file or ".mkv" in file or ".m4v" in file) and (search_term in file.lower()):
                    file_path = os.path.join(root, file).replace("/home/pi/media_server", "/storage/media_server")
                
                    requests.post(url, json = is_server_playing("video", file_path))

# search the music folders for a named one
def start_folder(folder):
    search_path = "/home/pi/media_server/"
    mount_server()
    # mount the file server on ruby if not already done
    Popen("[ ! -d \"/home/pi/media_server/music/\" ] && curlftpfs '" + file_server_password + "@" + file_server + ":21/' /home/pi/media_server", shell=True)
    search_term = folder.lower()
    for root, dirs, files in os.walk(search_path + "music"):
        for direct in dirs:
            if (search_term in direct.lower()):
                print(direct)
                for root2, dirs2, files2 in os.walk(os.path.join(root, direct)):
                    for file in files2:
                        if (".ogg" in file or ".mp3" in file):
                            file_path = os.path.join(root2, file).replace("/home/pi/media_server", "/storage/media_server")
                            
                            requests.post(url, json = is_server_playing("audio", file_path))

# play or pause an open video or song
def play_pause():
    data = {'jsonrpc':'2.0','id':1,'method':'Player.PlayPause','params':{'playerid':int(which_player_open()=="video")}}
    requests.post(url, json = data)

# close player/stop playing music or video
def stop():
    data = {'jsonrpc':'2.0','id':1,'method':'Player.Stop','params':{'playerid':int(which_player_open()=="video")}}
    requests.post(url, json = data)

# jump back to the previous song or video in the playlist (twice to beat the timing and actually go to previous instead of starting current over)
def skip_previous():
    data = {'jsonrpc':'2.0','id':1,'method':'Player.GoTo','params':{'playerid':int(which_player_open()=="video"), 'to':'previous'}}
    requests.post(url, json = data)
    requests.post(url, json = data)
    
# jump to the next song or video in the playlist
def skip_next():
    data = {'jsonrpc':'2.0','id':1,'method':'Player.GoTo','params':{'playerid':int(which_player_open()=="video"), 'to':'next'}}
    requests.post(url, json = data)
    
# set kodi volume to a stated amount
def set_volume(amount):
    print(amount)
    data = {'jsonrpc':'2.0','id':1,'method':'Application.SetVolume','params':{'volume':amount}}
    requests.post(url, json = data)