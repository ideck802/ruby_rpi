commands = []
    
def init(command):
    #open app on rpi
    commands.append(command("(re.match(r'open .+ locally', value) != None)","""
app_name = value.split(" ", 1)
app_name = app_name[-1].rsplit(" ", 1)
speak("opening " + app_name[0])
open_app.run(app_name[0])"""))
    #play a song on rpi
    commands.append(command("(value!='play music') and (re.match(r'play *', value))!=None and ('on computer' in value) == False","""
song_name = value.split(" ", 1)
speak("playing " + song_name[1])
play_music.start(song_name[1])"""))
    #close vlc thats running on rpi
    commands.append(command("value == 'close local vlc'","play_music.close()"))
    #resume/play vlc thats running on rpi
    commands.append(command("value == 'play local music'","play_music.play()"))
    #pause vlc thats running on rpi
    commands.append(command("value == 'pause local music'","play_music.pause()"))
    #stop vlc thats running on rpi
    commands.append(command("value == 'stop local music'","play_music.stop()"))
    #set the volume of vlc
    commands.append(command("re.match(r'set music volume to *', value) != None","""
volume_amount = value.split(" ") #get last word
volume_amount = text2int.text2int(volume_amount[-1])
play_music.set_volume(int(volume_amount))"""))
    commands.append(command("value == 'reset audio'","""
m = sr.Microphone()
print("A moment of silence, please...")
with m as source: r.adjust_for_ambient_noise(source)
print("Set minimum energy threshold to {}".format(r.energy_threshold))"""))
    commands.append(command("(value == 'turn on the computer') or (value == 'turn on my computer')","send_magic_packet('70:85:c2:c7:2c:b6')"))
    commands.append(command("(value == 'turn on the server') or (value == 'turn on my server')","send_magic_packet('f8:0f:41:04:86:a8')"))
    commands.append(command("(value == 'turn off the server') or (value == 'turn off my server') or (value == 'shutdown off the server') or (value == 'shutdown my server')","os.system('./shutdown_server')"))
    commands.append(command("(value == 'turn on the tv') or (value == 'turn on my tv')","send_magic_packet('84:7b:eb:f2:6c:8c')"))
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
    commands.append(command("(re.match(r'set the volume to *', value) != None) or (re.match(r'set volume to *', value) != None)","""
amount = value.split(" ")
amount = text2int.text2int(amount[-1])
mixer.setvolume(int(amount))"""))
    commands.append(command("value == 'turn on the lights' or value == 'turn on lights' or value == 'turn the lights on' or value == 'activate the lights'","bluetooth_stuff.turnon()"))
    commands.append(command("value == 'turn off the lights' or value == 'turn off lights' or value == 'turn the lights off' or value == 'deactivate the lights'","bluetooth_stuff.turnoff()"))
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
    #calculators
    commands.append(command("(re.match(r'what is .+ plus .+', value) != None)","""
equ = text2int.text2int(value)
equation = [int(s) for s in equ.split() if s.isdigit()]
speak(str(int(equation[0]) + int(equation[1])))"""))
    commands.append(command("(re.match(r'what is .+ subtract .+', value) != None) or (re.match(r'what is .+ minus .+', value) != None)","""
equ = text2int.text2int(value)
equation = [int(s) for s in equ.split() if s.isdigit()]
speak(str(int(equation[0]) - int(equation[1])))"""))
    commands.append(command("(re.match(r'what is .+ times .+', value) != None) or (re.match(r'what is .+ multiplied by .+', value) != None)","""
equ = text2int.text2int(value)
equation = [int(s) for s in equ.split() if s.isdigit()]
speak(str(int(equation[0]) * int(equation[1])))"""))
    commands.append(command("(re.match(r'what is .+ divided by .+', value) != None)","""
equ = text2int.text2int(value)
equation = [int(s) for s in equ.split() if s.isdigit()]
speak(str(int(equation[0]) / int(equation[1])))"""))
    #calculators end
    commands.append(command("(re.match(r'i work from .+ to .+ on .+', value) != None)","""
global numbers
numbers = [int(s) for s in text2int.text2int(value).split() if s.isdigit()]
numbers2 = [int(numbers[t])+12 if(int(numbers[t])<6 or int(numbers[t])>numbers[0] or int(numbers[t])<numbers[0]) else numbers[t] for t in range(2)]
if (datetime.now().day > numbers[2]):
    if (datetime.now().month == 12):
        date = str(datetime.now().year+1) + '-01-' + "{:02d}".format(numbers[2])
    else:
        date = str(datetime.now().year) + '-' + "{:02d}".format(datetime.now().month+1) + '-' + "{:02d}".format(numbers[2])
else:
    date = str(datetime.now().year) + '-' + "{:02d}".format(datetime.now().month) + '-' + "{:02d}".format(numbers[2])
google_calendar.add_event('Work at Mcdonalds', date, str(numbers2[0])+':00:00', date, str(numbers2[1])+':00:00')"""))
    commands.append(command("value=='when do i work next'","""
datetime2 = google_calendar.search_for_event('Work at Mcdonalds')[0]['start']['dateTime']
print(datetime2)
datetime2 = datetime2.split('T')
time = (int(datetime2[1].split(':')[0])-12) if int(datetime2[1].split(':')[0])>12 else int(datetime2[1].split(':')[0])
speak('You work next on the '+ordinal(datetime2[0].split('-')[-1])+' at '+str(time)+'o clock')"""))
    #windows computer commands
    commands.append(command("(re.match(r'open *', value) != None) and (not value=='open file explorer') and (not value=='open files') and (re.match(r'open folder *', value)) == None and (re.match(r'open file *', value)) == None","""
app_name = value.split(" ", 1)
speak("opening " + app_name[-1])
computer_server.send_job("open_app", "windows", f'"{app_name[-1]}"')"""))
    commands.append(command("value=='turn off my computer' or value=='turn off the computer'","computer_server.send_job('hibernate', 'windows')"))
    commands.append(command("value=='shut down my computer' or value=='shut down the computer'","computer_server.send_job('shutdown', 'windows')"))
    commands.append(command("value=='reboot my computer' or value=='reboot the computer' or value=='restart my computer' or value=='restart the computer'","computer_server.send_job('reboot', 'windows')"))
    #chrome control
    commands.append(command("value=='new tab' or value=='open a new tab'","computer_server.send_job('new_tab', 'windows')"))
    commands.append(command("(re.match(r'google *', value) != None)","""
search_term = value.split(" ", 1)
computer_server.send_job("google", "windows", f'"{search_term[-1]}"')"""))
    commands.append(command("(re.match(r'look up *', value) != None)","""
url = value.split(" ", 2)[-1].replace(" dot ", ".").replace(" ","")
computer_server.send_job("lookup", "windows", f'"{url}"')"""))
    commands.append(command("value=='close tab' or value=='close the current tab'","computer_server.send_job('close_tab', 'windows')"))
    commands.append(command("(re.match(r'close tab .+', value) != None)","""
tab_num = text2int.text2int(value).split(" ", 2)[-1]
computer_server.send_job("close_tab", "windows", f'"{tab_num}"')"""))
    commands.append(command("(re.match(r'switch to tab .+', value) != None) or (re.match(r'change to tab .+', value) != None)","""
tab = text2int.text2int(value).split(" ", 3)[-1]
if tab.isdigit():
    computer_server.send_job("change_tab", "windows", f'"{tab}"')
else:
    computer_server.send_job("change_tab", "windows", None, f'"{tab}"')"""))
    commands.append(command("value=='go back' or value=='go back a page'","computer_server.send_job('go_back', 'windows')"))
    #file explorer control
    commands.append(command("value=='open file explorer' or value=='open files'","computer_server.send_job('open_explorer', 'windows')"))
    commands.append(command("(re.match(r'find file .+', value)) != None","""
file_name = value.split("find file ", 1)[-1].replace(" dot ", ".")
print(file_name)
computer_server.send_job("open_explorer_file", "windows", f'"{file_name}"')"""))
    commands.append(command("(re.match(r'find file .+ in .+', value)) != None","""
file_name = value.split("find file ", 1)[-1].rsplit(" in ")
if len(file_name[-1]) == 1:
    file_name[-1] = file_name[-1] + " slash "
file_path = file_name[-1].replace(" dot ", ".").replace("see", "c").replace("slash ", "\\\\\\\\").replace("c ", "C:").replace("d ", "D:").replace("e ", "E:").replace("f ", "F:").replace(" \\\\\\\\", "\\\\\\\\")
print(file_name[0] + "  ,  " + file_path)
computer_server.send_job("open_explorer_file", "windows", f'"{file_name[0]}"', f'"{file_path}"')"""))
    commands.append(command("(re.match(r'open file .+', value)) != None and value!='open file explorer'","""
file_name = value.split("open file ", 1)[-1].replace(" dot ", ".")
print(file_name)
computer_server.send_job("open_file", "windows", f'"{file_name}"')"""))
    commands.append(command("(re.match(r'open file .+ in .+', value)) != None","""
file_name = value.split("open file ", 1)[-1].rsplit(" in ")
if len(file_name[-1]) == 1:
    file_name[-1] = file_name[-1] + " slash "
file_path = file_name[-1].replace(" dot ", ".").replace("see", "c").replace("slash ", "\\\\\\\\").replace("c ", "C:").replace("d ", "D:").replace("e ", "E:").replace("f ", "F:").replace(" \\\\\\\\", "\\\\\\\\")
print(file_name[0] + "  ,  " + file_path)
computer_server.send_job("open_file", "windows", f'"{file_name[0]}"', f'"{file_path}"')"""))
    commands.append(command("(re.match(r'open folder .+', value)) != None","""
folder_name = value.split("open folder ", 1)[-1].replace(" dot ", ".")
print(folder_name)
computer_server.send_job("open_explorer_folder", "windows", f'"{folder_name}"')"""))
    commands.append(command("(re.match(r'open folder .+ in .+', value)) != None","""
folder_name = value.split("open folder ", 1)[-1].rsplit(" in ")
if len(folder_name[-1]) == 1:
    folder_name[-1] = folder_name[-1] + " slash "
folder_path = folder_name[-1].replace(" dot ", ".").replace("see", "c").replace("slash ", "\\\\\\\\").replace("c ", "C:").replace("d ", "D:").replace("e ", "E:").replace("f ", "F:").replace(" \\\\\\\\", "\\\\\\\\")
print(folder_name[0] + "  ,  " + folder_path)
computer_server.send_job("open_explorer_folder", "windows", f'"{folder_name[0]}"', f'"{folder_path}"')"""))
    #vlc control
    commands.append(command("(re.match(r'play .+ on computer', value)) != None","""
song_name = value.split(" ", 1)
song_name = song_name[-1].rsplit(" ", 2)
speak("playing " + song_name[0])
computer_server.send_job("play_song", "windows", f'"{song_name[0]}"')"""))
    commands.append(command("value == 'close vlc'","computer_server.send_job('close_vlc', 'windows')"))
    commands.append(command("value == 'play music' or value == 'resume music'","computer_server.send_job('play_music', 'windows')"))
    commands.append(command("value == 'pause music'","computer_server.send_job('pause_music', 'windows')"))
    commands.append(command("value == 'stop music'","computer_server.send_job('stop_music', 'windows')"))
    commands.append(command("(re.match(r'set the music to *', value) != None) or (re.match(r'set the music volume to *', value) != None)","""
volume = text2int.text2int(value.rsplit("set the music to ", 1)[1])
print(volume)
computer_server.send_job("set_volume", "windows", f'"{volume}"')"""))
    commands.append(command("value == 'skip forward' or value == 'skip ahead'","computer_server.send_job('skip_forward', 'windows')"))
    commands.append(command("value == 'skip back'","computer_server.send_job('skip_back', 'windows')"))
    #
    # basic speaking responses
    #
    #hello
    commands.append(command("value=='hello' or value=='hi ruby' or value=='hello ruby' or value=='hi'","speak('Hi Isaac!')"))
    #goodbye
    commands.append(command("value=='bye' or value=='by ruby' or value=='goodbye ruby' or value=='goodbye'","speak('Bye Isaac, see you later!')"))
    #good morning
    commands.append(command("value=='good morning' or value=='good morning ruby'","speak('Good morning Isaac!')"))
    #goodnight
    commands.append(command("value=='good night' or value=='goodnight ruby'","speak('Goodnight Isaac! Sleep well.')"))
    #
    #
    #