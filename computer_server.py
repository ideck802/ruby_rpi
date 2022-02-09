import socketserver
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import time

client_for_job = None
command = "none"

arg1 = None
arg2 = None

hail_ruby = None

# Threaded mix-in
class AsyncXMLRPCServer(socketserver.ThreadingMixIn,SimpleXMLRPCServer): pass

def serve(port=2002):
    server = AsyncXMLRPCServer(('0.0.0.0', port), SimpleXMLRPCRequestHandler, allow_none=True)
    print("Listening on port " + str(port) + "...")
    server.register_function(request_job, "request_job")
    server.register_function(disconnect, "disconnect")
    server.register_function(trigger_listen, "trigger_listen")
    server.serve_forever()
    
def pass_server_func(manual_hail):
    global hail_ruby
    hail_ruby = manual_hail

def request_job(client_name):
    global client_for_job
    while(client_for_job != client_name):
        #print("looping...")
        time.sleep(0.2)
    
    client_for_job = None
    return command, arg1, arg2

def disconnect(name):
    global client_for_job
    global command
    command = "none"
    client_for_job = name
    
def trigger_listen():
    hail_ruby()

def send_job(sent_command, client, args1=None, args2=None):
    # strings as args must be wrapped in "'both quotes'"
    global arg1
    global arg2
    global command
    global client_for_job
    command = sent_command
    arg1 = args1
    arg2 = args2
    client_for_job = client


#send_job("test", "windows", "'chrome'")
#serve(2002)