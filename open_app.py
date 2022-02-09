import sys, os
from subprocess import Popen

files_path = os.path.expanduser("~") + "/Ruby_links"

def run(app):
    for root, dirs, files in os.walk(files_path):
        if app + ".desktop" in files:
            Popen("./deskopen " + os.path.expanduser("~") + "/Ruby_links/" + app + ".desktop", shell=True)