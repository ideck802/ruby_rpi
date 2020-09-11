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
    commands.append(command("re.match(r'shut down at *', value) != None","""
temp = value.split(" ")
if len(temp) == 5:
    temp2 = text2int.text2int(temp[4])
    if not temp2.isdigit():
        temp2 = "00"
elif len(temp) == 6:
    temp2 = text2int.text2int(temp[4] + " " + temp[5])
else:
    temp2 = "00"
time = [text2int.text2int(temp[3]), temp2]
print("sudo shutdown " + time[0] + ":" + time[1])
os.system("sudo shutdown " + time[0] + ":" + time[1])"""))
    commands.append(command("(re.match(r'set volume *', value) != None) or (re.match(r'set volume to *', value) != None)","""
amount = value.split(" ")
amount = text2int.text2int(amount[-1])
mixer.setvolume(int(amount))"""))
    commands.append(command("value == 'turn on the lights' or value == 'turn on lights' or value == 'activate lights' or value == 'activate the lights'","bluetooth_stuff.turnon()"))
    commands.append(command("value == 'turn off the lights' or value == 'turn off lights' or value == 'deactivate lights' or value == 'deactivate the lights'","bluetooth_stuff.turnoff()"))
    commands.append(command("value == 'what is the time' or value == 'what time is it'","""
speak('it is ' + datetime.now().time().strftime('%I:%M %p'))"""))
    #printer commands start
    commands.append(command("((re.match(r'move printer *', value) != None) and (re.match(r'(?:[A-Za-z]+ ){3}[A-Za-z]+', value))) or ((re.match(r'move the printer *', value) != None) and (re.match(r'(?:[A-Za-z]+ ){4}[A-Za-z]+', value))) or (((re.match(r'move my printer *', value) != None) and (re.match(r'(?:[A-Za-z]+ ){4}[A-Za-z]+', value))))","""
amount = value.split(" ")
direction = amount[-2]
amount = text2int.text2int(amount[-1])
if amount.isdigit():
    octo.move_tool(direction, int(amount))"""))
    commands.append(command("((re.match(r'move printer *', value) != None) and (re.match(r'(?:[A-Za-z]+ ){2}[A-Za-z]+', value))) or ((re.match(r'move the printer *', value) != None) and (re.match(r'(?:[A-Za-z]+ ){3}[A-Za-z]+', value))) or (((re.match(r'move my printer *', value) != None) and (re.match(r'(?:[A-Za-z]+ ){3}[A-Za-z]+', value))))","""
direction = value.split(" ")
direction = direction[-1]
octo.move_tool(direction)"""))
    commands.append(command("value == 'home my printer' or value == 'home the printer'","octo.go_home()"))
    commands.append(command("(re.match(r'set tool to *', value) != None) or (re.match(r'set the tool to *', value) != None) or (re.match(r'set extruder to *', value) != None) or (re.match(r'set the extruder to *', value) != None)","""
temp = text2int.text2int(value)
temp = temp.split(" ")
if temp[-1].isdigit():
    octo.set_tool_temp(int(temp[-1]))"""))
    commands.append(command("(re.match(r'set bed to *', value) != None) or (re.match(r'set the bed to *', value) != None)","""
temp = text2int.text2int(value)
temp = temp.split(" ")
if temp[-1].isdigit():
    octo.set_bed_temp(int(temp[-1]))"""))
    commands.append(command("(re.match(r'extrude *', value) != None) and (re.match(r'(?:[A-Za-z]+ )[A-Za-z]+', value))","""
amount = text2int.text2int(value)
amount = amount.split(" ")
if amount[-1].isdigit():
    octo.extrude(int(amount[-1]))"""))
    commands.append(command("value == 'extrude' or value == 'extrude filament'","octo.extrude()"))
    commands.append(command("(re.match(r'select *', value) != None)","""
files_list = octo.get_file_list()
file_name = value.split(" ", 1)
for i in range(len(files_list)):
    if file_name[1] in files_list["files"][i]["display"]:
        octo.select_print_file(files_list["files"][i]["display"])
        break"""))
    commands.append(command("value=='start print' or value=='start printing' or value=='start the print' or value == 'begin printing'","octo.start_job()"))
    commands.append(command("value=='pause the print' or value=='resume the print' or value=='resume printing'","octo.pause_job()"))
    commands.append(command("value=='stop printing' or value=='stop the print'","octo.cancel_job()"))
    commands.append(command("value=='connect printer' or value=='connect to the printer' or value=='reconnect printer'","octo.connect_printer()"))
    commands.append(command("value=='turn off printer' or value=='turn off the printer' or value=='turn off my printer'","octo.shutdown_octoprint()"))
    commands.append(command("value=='restart printer' or value=='reboot printer' or value=='restart the printer' or value=='reboot the printer' or value=='restart my printer' or value=='reboot my printer'","octo.restart_octoprint()"))
    commands.append(command("value=='what is the print progress' or value=='tell me the print progress'","speak('The print is ' + str(octo.get_print_progress()) + ' percent done.')"))
    commands.append(command("value=='what is printing'","speak(octo.get_file_printing() + ' is printing.')"))
    commands.append(command("value=='what is the extruder at' or value=='what is the tool at' or value=='what temperature is the extruder'","speak('The extruder is at ' + str(octo.get_tool_current()) + ' degrees celsius.')"))
    commands.append(command("value=='what is the bed at' or value=='what temperature is the bed'","speak('The print bed is at ' + str(octo.get_bed_current()) + ' degrees celsius.')"))
    #printer commands end