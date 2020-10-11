import socketserver
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import time

client_for_job = None
command = "test"

arg1 = None
arg2 = None

# Threaded mix-in
class AsyncXMLRPCServer(socketserver.ThreadingMixIn,SimpleXMLRPCServer): pass

def serve(port=2002):
    #server = SimpleXMLRPCServer(("localhost", port), allow_none=True)
    server = AsyncXMLRPCServer(('0.0.0.0', port), SimpleXMLRPCRequestHandler, allow_none=True)
    print("Listening on port " + str(port) + "...")
    server.register_function(request_job, "request_job")
    server.serve_forever()

def request_job(client_name):
    global client_for_job
    while(client_for_job != client_name):
        #print("looping...")
        time.sleep(0.2)
    
    client_for_job = None
    return command, arg1, arg2

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