commands = []
    
def init(command):
    commands.append(command("re.match(r'open *', value) != None","""
app_name = value.split(" ")
speak("opening " + app_name[1])
open_app.run(app_name[-1])"""))
    commands.append(command("(len(value) > 4) and (re.match(r'play *', value)) != None","""
song_name = value.split(" ", 1)
speak("playing " + song_name[1])
play_music.start(song_name[1])"""))
    commands.append(command("value == 'close'","play_music.close()"))
    commands.append(command("value == 'play'","play_music.play()"))
    commands.append(command("value == 'pause'","play_music.pause()"))
    commands.append(command("value == 'stop'","play_music.stop()"))
    commands.append(command("re.match(r'set music volume to *', value) != None","""
volume_amount = value.split(" ") #get last word
volume_amount = text2int.text2int(volume_amount[-1])
play_music.set_volume(int(volume_amount))"""))
    commands.append(command("value == 'reset audio'","""
m = sr.Microphone()
print("A moment of silence, please...")
with m as source: r.adjust_for_ambient_noise(source)
print("Set minimum energy threshold to {}".format(r.energy_threshold))"""))
    commands.append(command("(value == 'turn on the computer') or (value == 'turn on my computer')","send_magic_packet('70-85-C2-C7-2C-B6')"))
    commands.append(command("(value == 'turn on the server') or (value == 'turn on my server')","send_magic_packet('f8:0f:41:04:86:a8')"))
    commands.append(command("(value == 'turn off the server') or (value == 'turn off my server') or (value == 'shutdown off the server') or (value == 'shutdown my server')","os.system('./shutdown_server')"))
    commands.append(command("value == 'bake me a cake'","speak('i cannot bake a cake')"))
    commands.append(command("value == 'turn off computer'","""
kill_flash.set() #kill the lights flashing
os.system("sudo shutdown now")"""))
    commands.append(command("value == 'restart computer' or value == 'reboot computer'","""
kill_flash.set() #kill the lights flashing
os.system("sudo reboot now")"""))
    commands.append(command("re.match(r'shutdown at *', value) != None","""
time = value.split(" ")
print(time[-1])"""))
    commands.append(command("(re.match(r'set volume *', value) != None) or (re.match(r'set volume to *', value) != None)","""
amount = value.split(" ")
amount = text2int.text2int(amount[-1])
mixer.setvolume(int(amount))"""))
    commands.append(command("value == 'turn on the lights' or value == 'turn on lights' or value == 'activate lights' or value == 'activate the lights'","bluetooth_stuff.turnon()"))
    commands.append(command("value == 'turn off the lights' or value == 'turn off lights' or value == 'deactivate lights' or value == 'deactivate the lights'","bluetooth_stuff.turnoff()"))
    commands.append(command("value == 'what is the time' or value == 'what time is it'","""
print(datetime.now().time().strftime('%I:%M %p'))
speak('it is ' + datetime.now().time().strftime('%I:%M %p'))"""))