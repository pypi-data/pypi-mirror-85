"""
neji
====
"Get Documentation here"

from neji import Help
Help().help()



# This Library developed By:
# Viraj B. neji
# For improvement, Contact us
# All copyright reserved
"""

import requests
import json
import time
import os
import winreg as reg
import socket
import random
import signal
from threading import Thread
import sys, subprocess
import psutil

class CloudStorage:

    # This is for Cloud storage

    def __init__(self,file_path,silent=False):
        # Taking File from uploader -> str
        self.file_path = file_path

        # Controlling Information -> Boolean
        self.silent = silent
    def upload(self):
        try:
            self.r =  requests.post('https://file.io', files={'file': open(str(self.file_path), 'rb')})            
        except:

            # If file doesn't exist
            # OR
            # No Internet connection, It throw error

            if not self.silent:
                # if silence -> False; This will print
                print("File not found")
            return None
        self.al1 = json.loads(self.r.text)
        if not self.al1['success']:
            try:
                self.r =  requests.post('https://api.anonymousfiles.io', files={'file': open(str(self.file_path), 'rb')})
            except:
                if not self.silent:
                    # if silence -> False; This will print
                    print("File not found")
            self.al2 = (json.loads(self.r.text))

            # Below this code, Returns url returning
            return str(self.al2['url'])
        return str(self.al1['link'])






class OpenPort(): # Class
    """
This is for port operation.

    """

    # For Port operation
    def __init__(self,host='localhost',start_port_number=5500,end_port_number=65000,silent=False):
        self.host = host
        self.port = 8080
        self.start_port_number = start_port_number
        self.end_port_number = end_port_number
        self.silent = silent


    def AnyPortExist(self,host_="localhost",port_=8080,silent_=False): 
        # If port is in use -> True (Boolean)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.info = s.connect_ex((host_, port_)) == 0  # This is boolean determiner

        if not silent_:
            # if silence -> False; This will print
            if self.info:
                print("port is in use")
            else:
                # This port you can use
                print("port still not using")
        return self.info # Return boolean as per condition


    def FindOpenPort(self):
        # Running infinite loop
        while True:

            # Generate random number (only one number)
            self.port= random.randint(self.start_port_number, self.end_port_number)

            if not self.AnyPortExist(port_=self.port,host_=self.host,silent_=self.silent):
                # checked status of existance
                # if it is False, then returns port number

                return self.port
                # infinite loop broke here

    def QuiteServer(self):
        try:      
            try: 
                #   Kill current pid of process
                psutil.Process(os.getpid()).kill()
            except:
                
                os.kill(os.getpid(), signal.SIGSTOP)
        except:
            pass
# a = OpenPort()
# print(a.FindOpenPort())
# # port still not using
# # 60077

class Frame():
    def __init__(self):
        pass
    def ChromeHunter(self):
        import sys, subprocess as sps, os
        name = 'Google Chrome/Chromium'
        def chrome_hunter():
            if sys.platform in ['win32', 'win64']:
                return _find_chrome_win()
            elif sys.platform == 'darwin':
                return _find_chrome_mac() or _find_chromium_mac()
            elif sys.platform.startswith('linux'):
                return _find_chrome_linux()
            else:
                return None
        def _find_chrome_mac():
            default_dir = r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
            if os.path.exists(default_dir):
                return default_dir
            name = 'Google Chrome.app'
            alternate_dirs = [x for x in sps.check_output(["mdfind", name]).decode().split('\n') if x.endswith(name)]
            if len(alternate_dirs):
                return alternate_dirs[0] + '/Contents/MacOS/Google Chrome'
            return None
        def _find_chromium_mac():
            default_dir = r'/Applications/Chromium.app/Contents/MacOS/Chromium'
            if os.path.exists(default_dir):
                return default_dir
            name = 'Chromium.app'
            alternate_dirs = [x for x in sps.check_output(["mdfind", name]).decode().split('\n') if x.endswith(name)]
            if len(alternate_dirs):
                return alternate_dirs[0] + '/Contents/MacOS/Chromium'
            return None
        def _find_chrome_linux():
            import whichcraft as wch
            chrome_names = ['chromium-browser',
                            'chromium',
                            'google-chrome',
                            'google-chrome-stable']

            for name in chrome_names:
                chrome = wch.which(name)
                if chrome is not None:
                    return chrome
            return None
        def _find_chrome_win():            
            reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'
            for install_type in reg.HKEY_CURRENT_USER, reg.HKEY_LOCAL_MACHINE:
                try:
                    reg_key = reg.OpenKey(install_type, reg_path, 0, reg.KEY_READ)
                    chrome_path = reg.QueryValue(reg_key, None)
                    reg_key.Close()
                    if not os.path.isfile(chrome_path):
                        continue
                except WindowsError:
                    chrome_path = None
                else:
                    break
            return chrome_path
        return str(chrome_hunter())

# print(Frame().ChromeHunter())
# C:\Program Files (x86)\Google\Chrome\Application\chrome.exe


class PortGui():
    def __init__(self,host="localhost",port=8080,fullscreen=False,width=600,height=400,maximized=False,silent=False,frequency=1):
        self.host = host
        self.port = port
        self.fullscreen = fullscreen
        self.height = height
        self.width = width
        self.maximized = maximized
        self.silent = silent
        self.frequency = frequency
        self.url = "http://{}:{}/".format(self.host, self.port)
    
    def SyncRun(self):
        while True:
            if OpenPort().AnyPortExist(host_=self.host,port_=self.port,silent_=self.silent):
                break
            time.sleep(self.frequency)
        self.command = ""        
        if Frame().ChromeHunter() == "":
            return None
        self.command += '"'+str(Frame().ChromeHunter())+'" --new-window --app={}'.format(self.url)
        if self.fullscreen:
            self.command += " --start-fullscreen"
        elif self.maximized:
            self.command += " --start-maximized"
        else:
            self.command += " --window-size={},{}".format(self.width, self.height)
        if not self.silent:
            # if silence -> False; This will print
            print("GUI Launched")
        if not OpenPort().AnyPortExist(host_=self.host,port_=self.port,silent_=self.silent):
            return None
        os.system(self.command)
        OpenPort().QuiteServer()
        if not self.silent:
            # if silence -> False; This will print
            print("Server Closed")
    
    def AsyncRun(self):
        def sub():
            PortGui(host=self.host,port=self.port,fullscreen=self.fullscreen,width=self.width,height=self.height,maximized=self.maximized,silent=self.silent,frequency=self.frequency).SyncRun()
        Thread(target=sub).start()



class Help():
    def __init__(self):
        pass

    def author(self):
        print("""
Viraj B. Neji
        """)

    def version(self):
        print("""
Version : 0.0.1.0
(Deuterium)
        """)

    def help(self):
        print('''
"""
Run this code for more detailed information
"""
from neji import Help
al = Help()
al.author()
al.version()
al.example()
al.CloudStorage()
al.Frame()
al.OpenPort()
al.PortGui()
        ''')

    def example(self):
        print("""
#####################################################################
#######################     Example     #############################
#####################################################################
# imported module
from neji import PortGui,OpenPort
from flask import Flask
app = Flask(__name__)

# checking open random port
a = OpenPort().FindOpenPort()

@app.route("/")
def al():
    return "<title>"+str(a)+"</title>Hello World"

# Launch window when server is started, kill server when window killed
PortGui(port=a,width=100,frequency=2).AsyncRun()
# Running asynchronus-ly

# start sever
app.run(port=a,debug=True)


'''
For django like or any localserver, you can use this logic:
1. import respective module
2. start infinite loop too run (don't consider indentation)
    while True:
        a = OpenPort().AnyPortExist(host_="localhost",port_=8080,silent_=False)
        if a:
            break
    PortGui(port=a).AsyncRun()
3. when port get existed, Window will launch
4. server will killed by this module itself for security
5. NOTE :: Giving port number is very important
'''
        """)


    def CloudStorage(self):
        print("""
#####################################################################
#######################  CloudStorage   #############################
#####################################################################


a = CloudStorage(file_path,silent=False)
# file_path             ==> Give local file path which you want to upload
# If silent             ==> True -> Does not print anything related it

# # Total method available : 1
    # 1. upload()

eg. -> upload()

    a = CloudStorage("C:\\Users\\Viraj...\\longhorn.tts")
    print(a.upload())

        >> https://...
        # return link
        """)

        
    def PortGui(self):
        print("""
#####################################################################
#######################   PortGui       #############################
#####################################################################


a = PortGui(host="localhost",port=8080,fullscreen=False,width=600,height=400,maximized=False,silent=False,frequency=1)
# host                  ==> Give host name -> str
# port                  ==> Give port name -> int
# fullscreen            ==> If you want fullscreen, Make this true -> Boolean
# width                 ==> Give width number -> int
# height                ==> Give height number -> int
# maximized             ==> If you want maximized, Make this true -> Boolean
# silent                ==> If you want silent, Make this true -> Boolean
# frequency             ==> frequecy of check port in second -> float


# # Total method available : 2
    # 1. SyncRun()
    # 2. AsyncRun()

eg.1 -> SyncRun()

    a = PortGui(port=13131).SyncRun()
    # This function use is not recommanded
    # This means synchronus run which blocks your code


    
eg.2 -> AsyncRun()

    a = PortGui(port=13131).AsyncRun()
    # This function use is recommanded
    # This means Asynchronus run which won't blocks your code
    # Window will launch
        """)
        
    def Frame(self):
        print("""
#####################################################################
#######################    Frame        #############################
#####################################################################


a = Frame()

# # Total method available : 1
    # 1. ChromeHunter()

eg.1  -> ChromeHunter()

    a = Frame().ChromeHunter()
    print(a)

        >> L:\\...\\chrome.exe
        # return chrome path
        """)

    def OpenPort(self):
        print("""
#####################################################################
#######################    OpenPort     #############################
#####################################################################

a = OpenPort(host='localhost',start_port_number=5500,end_port_number=65000,silent=False)
# host                  ==> Give host name
# start_port_number     ==> Give number from which you want to start port
# end_port_number       ==> Give number from which you want to end (max. limit : "65,535")


# Total methods available : 3
    # 1. AnyPortExist(host_="localhost",port_=8080,silent_=False)
    # 2. FindOpenPort()
    # 3. QuiteServer()

eg.1    -> AnyPortExist(host_="localhost",port_=8080,silent_=False)

    a = OpenPort().AnyPortExist(host_="localhost",port_=8080,silent_=False)
    print(a)
    # if a -> True -> Port is using; else reverse
    # If silent -> True -> Does not print anything related it


eg.2    -> FindOpenPort()
    a = OpenPort().FindOpenPort()
    print(a)
    # This will give port which is open, randomly selected


eg.3    -> QuiteServer()
    a = OpenPort().QuiteServer()
    # This will quite server
        """)