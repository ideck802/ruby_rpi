import sys, os
from subprocess import Popen

music_path = " "

playing_song = False
vlc_open = False

def set_music_values(temp, temp2):
    global mixer_record
    global alsaaudio
    mixer_record = temp
    alsaaudio = temp2

def start(song):
    song2 = song.title()
    for root, dirs, files in os.walk(music_path):
        for file in files:
            if (".mp4" in file or ".mp3" in file) and (song in file or song2 in file):
                test = '\"' + os.path.join(root, file) + '\"'
                
                global player
                global playing_song
                global vlc_open
                
                if vlc_open == False:
                    player = Popen("vlc " + test, shell=True)
                    playing_song = True
                    vlc_open = True
                    print(player)
                else:
                    player = Popen("vlc --one-instance --playlist-enqueue " + test, shell=True)

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