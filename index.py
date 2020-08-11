from wakeonlan import send_magic_packet
from gtts import gTTS
from pocketsphinx import LiveSpeech
import speech_recognition as sr
import pygame
import time
import re
import os
import threading
import alsaaudio
import configparser
import text2int
import open_app
import play_music
import lights
import bluetooth_stuff

r = sr.Recognizer()
m = sr.Microphone()

client_id = "KZb9pi9EMnVpoxcTGDQWCw=="
client_key = "FDOijmx1-dFpUVSz2JBNSpj26hWupoY-CoH9QZAsnp1X3EtZiu7-B_A158M2NFLanjeJp_XlNUYjaGLXNmUJxw=="
client_key_wit = "EXPAIXPCS7TDH6D2WPICEDPWUWL7F45L"

srt = 0
srtools = ["houndify", "wit"]

mixer = alsaaudio.Mixer()
mixer_record = alsaaudio.Mixer('Capture')

config = configparser.ConfigParser()
path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
config.read(os.path.join(path, "config.ini"))

play_music.music_path = config["paths"]["music_path"]

def button_stuff():
    while True:
        state = GPIO.input(BUTTON)
        if state:
            time.sleep(0.2)
        else:
            reset_audio()

import RPi.GPIO as GPIO
BUTTON = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN)
button_thread = threading.Thread(target=button_stuff)
button_thread.start()

def timeout_timer(pill2kill):
    counter = 0
    while (counter <= 8) and (not pill2kill.is_set()):
        if counter == 8:
            print("timeout")
            mixer_record.setvolume(mixer_record.getvolume(alsaaudio.PCM_CAPTURE)[0]-30)
            time.sleep(3)
            mixer_record.setvolume(mixer_record.getvolume(alsaaudio.PCM_CAPTURE)[0]+30)
        counter+=1
        time.sleep(1)

pygame.mixer.init()
def speak(phrase):
    tts = gTTS(phrase)
    tts.save("speak.mp3")
    pygame.mixer.music.load("speak.mp3")
    pygame.mixer.music.play()
    time.sleep(1)

def listen_for_commands():
    global srt
    print("Say something!")
    global m
    m = sr.Microphone()
    kill_timer = threading.Event()
    timer = threading.Thread(target=timeout_timer, args=(kill_timer, ))
    timer.start()
    with m as source: audio = r.listen(source)
    kill_timer.set()
    print("Got it! Now to recognize it...")
    try:
        if srtools[srt] == "houndify":
            # recognize speech using Houndify Speech Recognition
            value = r.recognize_houndify(audio, client_id, client_key)
        elif srtools[srt] == "wit":
            # recognize speech using Wit.ai Speech Recognition
            value = r.recognize_wit(audio, client_key_wit)
        
        #value = text2int.text2int(value)
        #omit whitespace
        value = value.rstrip()
        
        print("You said {}".format(value))
        
        if re.match(r"open *", value) != None:
            kill_pulse.set() #kill the lights pulsing
            kill_flash = threading.Event()
            lights_thread = threading.Thread(target=flash_lights, args=(kill_flash, ))
            lights_thread.start()
            
            app_name = value.split(" ") #get last word
            speak("opening " + app_name[1])
            open_app.run(app_name[-1])
            
            kill_flash.set() #kill the lights flashing
        
        if (len(value) > 4) and (re.match(r"play *", value) != None):
            kill_pulse.set() #kill the lights pulsing
            kill_flash = threading.Event()
            lights_thread = threading.Thread(target=flash_lights, args=(kill_flash, ))
            lights_thread.start()
            
            song_name = value.split(" ", 1) #omit the word play
            speak("playing " + song_name[1])
            play_music.start(song_name[1])
            
            kill_flash.set() #kill the lights flashing
        
        if value == "close":
            kill_pulse.set() #kill the lights pulsing
            kill_flash = threading.Event()
            lights_thread = threading.Thread(target=flash_lights, args=(kill_flash, ))
            lights_thread.start()
            
            play_music.close()
            
            kill_flash.set() #kill the lights flashing
            
        if value == "play":
            kill_pulse.set() #kill the lights pulsing
            kill_flash = threading.Event()
            lights_thread = threading.Thread(target=flash_lights, args=(kill_flash, ))
            lights_thread.start()
            
            play_music.play()
            
            kill_flash.set() #kill the lights flashing
            
        if value == "pause":
            kill_pulse.set() #kill the lights pulsing
            kill_flash = threading.Event()
            lights_thread = threading.Thread(target=flash_lights, args=(kill_flash, ))
            lights_thread.start()
            
            play_music.pause()
            
            kill_flash.set() #kill the lights flashing
            
        if value == "stop":
            kill_pulse.set() #kill the lights pulsing
            kill_flash = threading.Event()
            lights_thread = threading.Thread(target=flash_lights, args=(kill_flash, ))
            lights_thread.start()
            
            play_music.stop()
            
            kill_flash.set() #kill the lights flashing
            
        if re.match(r"set music volume to *", value) != None:
            volume_amount = value.split(" ") #get last word
            play_music.set_volume(int(volume_amount[-1]))
                
        if value == "reset audio":
            kill_pulse.set() #kill the lights pulsing
            kill_flash = threading.Event()
            lights_thread = threading.Thread(target=flash_lights, args=(kill_flash, ))
            lights_thread.start()
            
            m = sr.Microphone()
            print("A moment of silence, please...")
            with m as source: r.adjust_for_ambient_noise(source)
            print("Set minimum energy threshold to {}".format(r.energy_threshold))
            
            kill_flash.set() #kill the lights flashing
                
        if (value == "turn on the computer") or (value == "turn on my computer"):
            kill_pulse.set() #kill the lights pulsing
            kill_flash = threading.Event()
            lights_thread = threading.Thread(target=flash_lights, args=(kill_flash, ))
            lights_thread.start()
            
            send_magic_packet("70-85-C2-C7-2C-B6")
            
            kill_flash.set() #kill the lights flashing
            
        if (value == "turn on the server") or (value == "turn on my server"):
            kill_pulse.set() #kill the lights pulsing
            kill_flash = threading.Event()
            lights_thread = threading.Thread(target=flash_lights, args=(kill_flash, ))
            lights_thread.start()
            
            send_magic_packet("f8:0f:41:04:86:a8")
            
            kill_flash.set() #kill the lights flashing
        
        if value == "bake me a cake":
            kill_pulse.set() #kill the lights pulsing
            kill_flash = threading.Event()
            lights_thread = threading.Thread(target=flash_lights, args=(kill_flash, ))
            lights_thread.start()
            
            speak("i cannot bake a cake")
            
            kill_flash.set() #kill the lights flashing
                
        if value == "turn off computer":
            kill_pulse.set() #kill the lights pulsing
            kill_flash = threading.Event()
            lights_thread = threading.Thread(target=flash_lights, args=(kill_flash, ))
            lights_thread.start()
            
            kill_flash.set() #kill the lights flashing
            os.system("sudo shutdown now")
                
        if value == "restart computer" or value == "reboot computer":
            kill_pulse.set() #kill the lights pulsing
            kill_flash = threading.Event()
            lights_thread = threading.Thread(target=flash_lights, args=(kill_flash, ))
            lights_thread.start()
            
            kill_flash.set() #kill the lights flashing
            os.system("sudo reboot now")
            
        if re.match(r"shutdown at *", value) != None:
            kill_pulse.set() #kill the lights pulsing
            kill_flash = threading.Event()
            lights_thread = threading.Thread(target=flash_lights, args=(kill_flash, ))
            lights_thread.start()
            #get last word which should be a number
            time = value.split(" ")
            print(time[-1])
            kill_flash.set() #kill the lights flashing
        
        if (re.match(r"set volume *", value) != None) or (re.match(r"set volume to *", value) != None):
            kill_pulse.set() #kill the lights pulsing
            kill_flash = threading.Event()
            lights_thread = threading.Thread(target=flash_lights, args=(kill_flash, ))
            lights_thread.start()
            #get last word which should be a number
            amount = value.split(" ")
            mixer.setvolume(int(amount[-1]))
            kill_flash.set() #kill the lights flashing
            
        if value == "turn on the lights" or value == "activate lights" or value == "activate the lights":
            kill_pulse.set() #kill the lights pulsing
            kill_flash = threading.Event()
            lights_thread = threading.Thread(target=flash_lights, args=(kill_flash, ))
            lights_thread.start()
            #get last word which should be a number
            #speak("turning on the lights")
            bluetooth_stuff.turnon()
            kill_flash.set() #kill the lights flashing
            
        if value == "turn off the lights" or value == "deactivate lights" or value == "deactivate the lights":
            kill_pulse.set() #kill the lights pulsing
            kill_flash = threading.Event()
            lights_thread = threading.Thread(target=flash_lights, args=(kill_flash, ))
            lights_thread.start()
            #get last word which should be a number
            #speak("turning off the lights")
            bluetooth_stuff.turnoff()
            kill_flash.set() #kill the lights flashing
        
        kill_pulse.set() #kill the lights pulsing
        
    except sr.UnknownValueError:
        print("Oops! Didn't catch that")
        kill_pulse.set() #kill the lights pulsing
    except sr.RequestError as e:
        print("Uh oh! Couldn't request results from Houndify Speech Recognition service; {0}".format(e))
        srt = srt + 1
        
def reset_audio():
    color_temp = lights.color
    lights.set_color(0,0,255)
    lights.flash(2)
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    lights.set_color(0,255,0)
    lights.flash(2)
    lights.set_color(color_temp[0],color_temp[1],color_temp[2])

def pulse_lights(pill2kill):
    while not pill2kill.is_set():
        lights.pulse(1)
        
def flash_lights(pill2kill):
    while not pill2kill.is_set():
        lights.flash(1)

reset_audio()

speech = LiveSpeech(lm=False, kws='words.list')
speech_music = LiveSpeech(lm=False, kws='words_music.list')

def init_listen():
    print(play_music.playing_song)
    global kill_pulse
    if play_music.playing_song == False:
        print("listen normal")
        for phrase in speech:
            print(phrase.segments())
            if phrase.segments()[0] == "ruby listen ":
                kill_pulse = threading.Event()
                lights_thread = threading.Thread(target=pulse_lights, args=(kill_pulse, ))
                lights_thread.start()
                pygame.mixer.music.load("yes.mp3")
                pygame.mixer.music.play()
                time.sleep(1)
                print("yes?")
                listen_for_commands()
                break
            elif (phrase.segments()[0] == "play ") and (play_music.vlc_open == True):
                play_music.play()
                break
            elif (phrase.segments()[0] == "pause ") and (play_music.vlc_open == True):
                play_music.pause()
                break
            elif (phrase.segments()[0] == "stop ") and (play_music.vlc_open == True):
                play_music.stop()
                break
            elif (phrase.segments()[0] == "close ") and (play_music.vlc_open == True):
                play_music.close()
                break
    else:
        print("listen music")
        for phrase in speech_music:
            print(phrase.segments())
            if phrase.segments()[0] == "ruby ":
                kill_pulse = threading.Event()
                lights_thread = threading.Thread(target=pulse_lights, args=(kill_pulse, ))
                lights_thread.start()
                pygame.mixer.music.load("yes.mp3")
                pygame.mixer.music.play()
                time.sleep(1)
                print("yes?")
                listen_for_commands()
                break
            elif (phrase.segments()[0] == "play ") and (play_music.vlc_open == True):
                play_music.play()
                break
            elif (phrase.segments()[0] == "pause ") and (play_music.vlc_open == True):
                play_music.pause()
                break
            elif (phrase.segments()[0] == "stop ") and (play_music.vlc_open == True):
                play_music.stop()
                break
            elif (phrase.segments()[0] == "close ") and (play_music.vlc_open == True):
                play_music.close()
                break
    init_listen()
                
init_listen()