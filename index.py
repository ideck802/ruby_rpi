from wakeonlan import send_magic_packet
#from google.cloud import texttospeech
from pocketsphinx import LiveSpeech
from datetime import datetime
from side_scripts.ordinal_number import ordinal
from speech.speech_stuff import speak
from side_scripts import text2int
from subprocess import Popen
import speech_recognition as sr
import pygame
import time
import re
import sys, os
import threading
import alsaaudio
import configparser
import open_app
import media_stuff
import lights
import bluetooth_stuff
import octopi_control
import command_file
import google_calendar
import computer_server
import smart_home


r = sr.Recognizer()
m = sr.Microphone()

srt = 0
srtools = ["houndify", "google", "wit"]

mixer = alsaaudio.Mixer('Master')
mixer_record = alsaaudio.Mixer('Capture')
media_stuff.set_music_values(mixer_record, alsaaudio)

config = configparser.ConfigParser()
path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
config.read(os.path.join(path, "config.ini"))

client_id = config["api keys"]["houndify_id"]
client_key = config["api keys"]["houndify"]
client_key_wit = config["api keys"]["witai"]

octo = octopi_control.octopi(config["ip addresses"]["octopi"], "80", config["api keys"]["octoprint"])

media_stuff.music_path = config["paths"]["music_path"]

is_listening = False

def get_home_setup():
    send_magic_packet('70:85:c2:c7:2c:b6')
    send_magic_packet('f8:0f:41:04:86:a8')

def check_for_phone():
    phone_connected = True
    while True:
        response = os.system("ping -c 1 192.168.1.17 >/dev/null")
        if response == 0:
            if phone_connected == False:
                get_home_setup()
            phone_connected = True
        else:
            phone_connected = False
        time.sleep(15)

phone_checking = threading.Thread(target=check_for_phone)
phone_checking.start()

def manual_hail():
    if is_listening == True:
        timeout()
    else:
        speech.stop()

def button_stuff():
    global is_listening
    while True:
        state = GPIO.input(BUTTON)
        if state:
            time.sleep(0.2)
        else:
            manual_hail()

import RPi.GPIO as GPIO
BUTTON = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN)
button_thread = threading.Thread(target=button_stuff)
button_thread.start()

server_thread = threading.Thread(target=computer_server.serve)
server_thread.start()

def door_opened():
    if (bluetooth_stuff.at_home):
        speak("Bye Isaac, see you later!")
    elif (not bluetooth_stuff.at_home):
        speak("Welcome back Isaac!")

bt_door_thread = threading.Thread(target=bluetooth_stuff.init_door_detector, args=(door_opened,))
bt_door_thread.start()

computer_server.pass_server_func(manual_hail)

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

def command_init():
    global kill_flash
    global flash_thread
    kill_pulse.set() #kill the lights pulsing
    kill_flash = threading.Event()
    flash_thread = threading.Thread(target=flash_lights, args=(kill_flash, ))
    flash_thread.start()

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
            value = r.recognize_houndify(audio, client_id, client_key).lower()
        elif srtools[srt] == "google":
            # recognize speech using Wit.ai Speech Recognition
            value = r.recognize_google(audio).lower()
        elif srtools[srt] == "wit":
            # recognize speech using Wit.ai Speech Recognition
            value = r.recognize_wit(audio, client_key_wit).lower()
        
        #value = text2int.text2int(value)
        #omit whitespace
        value = value.rstrip()
        
        print("You said {}".format(value))
        
        for i in range(len(command_file.commands)):
            if eval(command_file.commands[i].term):
                command_init()
                
                command_file.commands[i].run(value)
                
                kill_flash.set() #kill the lights flashing
                flash_thread.join()
        
        kill_pulse.set() #kill the lights pulsing
        pulse_thread.join()
        
    except sr.UnknownValueError:
        print("Oops! Didn't catch that")
        kill_pulse.set() #kill the lights pulsing
        pulse_thread.join()
    except sr.RequestError as e:
        print("Uh oh! Couldn't request results; {0}".format(e))
        srt = srt + 1
        kill_pulse.set() #kill the lights pulsing
        pulse_thread.join()

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

def audio_loop():
    while True:
        reset_audio()
        time.sleep(600)

ambient_audio_thread = threading.Thread(target=audio_loop)
ambient_audio_thread.start()


speech = LiveSpeech(lm=False, kws='words.list')

def listen_for_commands_setup():
    global kill_pulse
    global is_listening
    global pulse_thread
    kill_pulse = threading.Event()
    pulse_thread = threading.Thread(target=pulse_lights, args=(kill_pulse, ))
    pulse_thread.start()
    pygame.mixer.music.load("speech/speech_files/yes.mp3")
    pygame.mixer.music.play()
    time.sleep(1)
    print("yes?")
    is_listening = True
    listen_for_commands()

def init_listen():
    global is_listening
    is_listening = False
    global kill_pulse
    
    print("listen normal")
    for phrase in speech:
        print(phrase.segments())
        if phrase.segments()[0] == "ruby listen ":
            listen_for_commands_setup()
            break
            
    if speech.interrupt:
        listen_for_commands_setup()
    init_listen()
                
init_listen()