import sys, os
from subprocess import Popen

music_path = " "

playing_song = False
vlc_open = False

def start(song):
    song2 = song.title()
    for root, dirs, files in os.walk(music_path):
        for file in files:
            if (".mp4" in file or ".mp3" in file) and (song in file or song2 in file):
                test = '\"' + os.path.join(root, file) + '\"'
                
                global player
                global playing_song
                global vlc_open
                
                player = Popen("vlc " + test, shell=True)
                playing_song = True
                vlc_open = True
                print(player)

def close():
    global playing_song
    global vlc_open
    Popen(['vlc-ctrl', 'quit'])
    playing_song = False
    vlc_open = False

def play():
    global playing_song
    Popen(['vlc-ctrl', 'play'])
    playing_song = True
    
def pause():
    global playing_song
    Popen(['vlc-ctrl', 'pause'])
    playing_song = False
    
def stop():
    global playing_song
    Popen(['vlc-ctrl', 'stop'])
    playing_song = False
    
def set_volume(amount):
    print(amount)
    Popen(['vlc-ctrl', 'volume', str(amount) + "%"])