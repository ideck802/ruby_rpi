from wakeonlan import send_magic_packet
from google.cloud import texttospeech
from pocketsphinx import LiveSpeech
from datetime import datetime
from ordinal_number import ordinal
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
import octopi_control
import command_file
import google_calendar
import computer_server


r = sr.Recognizer()
m = sr.Microphone()

srt = 0
srtools = ["houndify", "wit"]

mixer = alsaaudio.Mixer('Master')
mixer_record = alsaaudio.Mixer('Capture')
play_music.set_music_values(mixer_record, alsaaudio)

config = configparser.ConfigParser()
path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
config.read(os.path.join(path, "config.ini"))

client_id = config["api keys"]["houndify_id"]
client_key = config["api keys"]["houndify"]
client_key_wit = config["api keys"]["witai"]

octo = octopi_control.octopi("192.168.2.10", "80", config["api keys"]["octoprint"])

play_music.music_path = config["paths"]["music_path"]

is_listening = False

def button_stuff():
    global is_listening
    while True:
        state = GPIO.input(BUTTON)
        if state:
            time.sleep(0.2)
        else:
            if is_listening == True:
                timeout()
            else:
                speech.stop()

import RPi.GPIO as GPIO
BUTTON = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN)
button_thread = threading.Thread(target=button_stuff)
button_thread.start()

server_thread = threading.Thread(target=computer_server.serve)
server_thread.start()

def timeout():
    print("timeout")
    mixer_record.setvolume(mixer_record.getvolume(alsaaudio.PCM_CAPTURE)[0]-30)
    time.sleep(3)
    mixer_record.setvolume(mixer_record.getvolume(alsaaudio.PCM_CAPTURE)[0]+30)

def timeout_timer(pill2kill):
    counter = 0
    while (counter <= 8) and (not pill2kill.is_set()):
        if counter == 8:
            timeout()
        counter+=1
        time.sleep(1)

#text to speech stuff
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./ruby-for-pc-0b5827d59846.json"
voice = texttospeech.VoiceSelectionParams(
    language_code='en-US',
    name='en-US-Standard-G',
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
google_tts_client = texttospeech.TextToSpeechClient()
pygame.mixer.init()
def speak(phrase):
    response = google_tts_client.synthesize_speech(input=texttospeech.SynthesisInput(text=phrase), voice=voice, audio_config=texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3))
    open('speak.mp3', 'wb').write(response.audio_content)
    pygame.mixer.music.load("speak.mp3")
    pygame.mixer.music.play()
    time.sleep(1)

def command_init():
    global kill_flash
    kill_pulse.set() #kill the lights pulsing
    kill_flash = threading.Event()
    lights_thread = threading.Thread(target=flash_lights, args=(kill_flash, ))
    lights_thread.start()

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
        
        for i in range(len(command_file.commands)):
            if eval(command_file.commands[i].term):
                command_init()
                
                command_file.commands[i].run(value)
                
                kill_flash.set() #kill the lights flashing
        
        kill_pulse.set() #kill the lights pulsing
        
    except sr.UnknownValueError:
        print("Oops! Didn't catch that")
        kill_pulse.set() #kill the lights pulsing
    except sr.RequestError as e:
        print("Uh oh! Couldn't request results from Houndify Speech Recognition service; {0}".format(e))
        srt = srt + 1
        kill_pulse.set() #kill the lights pulsing

class command:
    def __init__(self,term,output):
        self.term = term
        self.output = output
        
    def run(self, value):
        exec(compile(self.output,"-","exec"))
command_file.init(command)

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

def listen_for_commands_setup():
    global kill_pulse
    global is_listening
    kill_pulse = threading.Event()
    lights_thread = threading.Thread(target=pulse_lights, args=(kill_pulse, ))
    lights_thread.start()
    pygame.mixer.music.load("yes.mp3")
    pygame.mixer.music.play()
    time.sleep(1)
    print("yes?")
    is_listening = True
    listen_for_commands()

def init_listen():
    global is_listening
    is_listening = False
    print(play_music.playing_song)
    global kill_pulse
    if play_music.playing_song == False:
        print("listen normal")
        for phrase in speech:
            print(phrase.segments())
            if phrase.segments()[0] == "ruby listen ":
                listen_for_commands_setup()
                break
    else:
        print("listen music")
        for phrase in speech_music:
            print(phrase.segments())
            if phrase.segments()[0] == "ruby listen ":
                listen_for_commands_setup()
                break
            
    if speech.interrupt:
        listen_for_commands_setup()
    init_listen()
                
init_listen()