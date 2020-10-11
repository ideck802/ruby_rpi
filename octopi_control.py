import requests
import sys
import json


class octopi:
    
    def __init__(self, address, port, api_key):
        self.host = address
        self.s = requests.Session()
        self.s.headers.update({'X-Api-Key': api_key, 'Content-Type': 'application/json'})

        # Base address for all the requests
        self.base_address = 'http://' + address + ':' + str(port)
        
    def send_gcode(self, gcode):
        #send gcode to printer. input as list.
        r = self.s.post(self.base_address + '/api/printer/command', json={'commands': gcode})
        if r.status_code != 204:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        
    def move_tool(self, direction, amount=10):
        #move tool head in a direction (up,down,left,right,forward,backward) by an amount in millimeters (default is 10)
        if direction == "up":
            r = self.s.post(self.base_address + '/api/printer/printhead', json={'command': 'jog', 'z': amount})
            if r.status_code != 204:
                raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        elif direction == "down":
            r = self.s.post(self.base_address + '/api/printer/printhead', json={'command': 'jog', 'z': -amount})
            if r.status_code != 204:
                raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        elif direction == "left":
            r = self.s.post(self.base_address + '/api/printer/printhead', json={'command': 'jog', 'x': -amount})
            if r.status_code != 204:
                raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        elif direction == "right":
            r = self.s.post(self.base_address + '/api/printer/printhead', json={'command': 'jog', 'x': amount})
            if r.status_code != 204:
                raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        elif direction == "forward":
            r = self.s.post(self.base_address + '/api/printer/printhead', json={'command': 'jog', 'y': amount})
            if r.status_code != 204:
                raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        elif direction == "back":
            r = self.s.post(self.base_address + '/api/printer/printhead', json={'command': 'jog', 'y': -amount})
            if r.status_code != 204:
                raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
            
    def go_home(self):
        r = self.s.post(self.base_address + '/api/printer/printhead', json={'command': 'home', 'axes': ['x','y','z']})
        if r.status_code != 204:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        
    def set_tool_temp(self, temp):
        #set the temperature of the extruder tool in degrees celcius
        r = self.s.post(self.base_address + '/api/printer/tool', json={'command': 'target', 'targets': {'tool0': temp}})
        if r.status_code != 204:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        
    def set_bed_temp(self, temp):
        #set the temperature of the print bed in degrees celcius
        r = self.s.post(self.base_address + '/api/printer/bed', json={'command': 'target', 'target': temp})
        if r.status_code != 204:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        
    def extrude(self, amount=10):
        #extrude filament through the hotend in millimeters
        r = self.s.post(self.base_address + '/api/printer/tool', json={'command': 'extrude', 'amount': amount})
        if r.status_code != 204:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
    
    def get_file_list(self):
        #get list of all 3d files in the root directory on the octoprint server
        r = self.s.get(self.base_address + '/api/files')
        if r.status_code != 200:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        try:
            return json.loads(r.content.decode('utf-8'))
        except:
            raise Exception('Error retrieving file list')
    
    def select_print_file(self, file_name):
        #select a gcode file to print
        r = self.s.post(self.base_address + '/api/files/local/' + file_name, json={'command': 'select'})
        if r.status_code != 204:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        
    def pause_job(self):
        #pause the current running print job
        r = self.s.post(self.base_address + '/api/job', json={'command': 'pause'})
        if r.status_code != 204:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))

    def resume_job(self):
        #resume the previously paused print job
        r = self.s.post(self.base_address + '/api/job', json={'command': 'pause'})
        if r.status_code != 204:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))

    def start_job(self):
        #start a new print job with the selected gcode file
        r = self.s.post(self.base_address + '/api/job', json={'command': 'start'})
        if r.status_code != 204:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))

    def cancel_job(self):
        #cancel the currently running job
        r = self.s.post(self.base_address + '/api/job', json={'command': 'cancel'})
        if r.status_code != 204:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
    
    def connect_printer(self):
        #initiate a connection with the printer using automatic detection of settings
        r = self.s.post(self.base_address + '/api/connection', json={'command': 'connect'})
        if r.status_code != 204:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        
    def shutdown_octoprint(self):
        #shutdown octoprint server
        r = self.s.post(self.base_address + '/api/system/commands/core/shutdown')
        if r.status_code != 204:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        
    def restart_octoprint(self):
        #reboot the octoprint server
        r = self.s.post(self.base_address + '/api/system/commands/core/reboot')
        if r.status_code != 204:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        
    def get_print_progress(self):
        #get the print progress as a percentage
        r = self.s.get(self.base_address + '/api/job')
        if r.status_code != 200:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        try:
            return json.loads(r.content.decode('utf-8'))["progress"]["completion"]
        except:
            raise Exception('Error reading print progress')
        
    def get_file_printing(self):
        #get the name of the file being printed
        r = self.s.get(self.base_address + '/api/job')
        if r.status_code != 200:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        try:
            return json.loads(r.content.decode('utf-8'))["job"]["file"]["name"]
        except:
            raise Exception('Error reading filename being printed')
        
    def get_tool_target(self):
        #get the target temperature of the first tool
        r = self.s.get(self.base_address + '/api/printer/tool')
        if r.status_code != 200:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        try:
            return json.loads(r.content.decode('utf-8'))["tool0"]["target"]
        except:
            raise Exception('Error retrieving extruder target temperature')

    def get_tool_current(self):
        #get the current temperature of the first tool
        r = self.s.get(self.base_address + '/api/printer/tool')
        if r.status_code != 200:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        try:
            return json.loads(r.content.decode('utf-8'))["tool0"]["actual"]
        except:
            raise Exception('Error retrieving extruder temperature')
        
    def get_bed_target(self):
        #get the target temperature of the print bed
        r = self.s.get(self.base_address + '/api/printer/bed')
        if r.status_code != 200:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        try:
            return json.loads(r.content.decode('utf-8'))["bed"]["target"]
        except:
            raise Exception('Error retrieving bed target temperature')

    def get_bed_current(self):
        #get the current temperature of the print bed
        r = self.s.get(self.base_address + '/api/printer/bed')
        if r.status_code != 200:
            raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8')))
        try:
            return json.loads(r.content.decode('utf-8'))["bed"]["actual"]
        except:
            raise Exception('Error retrieving bed temperature')
        
    def get_printer_status(self):
        #get the status of the printer whether it is printing, operational or other
        r = self.s.get(self.base_address + '/api/printer')
        if r.status_code != 200:
           raise Exception("Error: {code} - {content}".format(code=r.status_code, content=r.content.decode('utf-8'))) 
        try:
            return json.loads(r.content.decode('utf-8'))["state"]["text"]
        except:
            raise Exception('Error trying to get printer status')


#octo = octopi("192.168.2.10", "80", "BE3CD0EDA3AE4DE6A83749880C6BE422")
