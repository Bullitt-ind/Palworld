import shutil, signal

from  os import path,mkdir,listdir,remove, system
from datetime import datetime
now = datetime.now
from rcon.source import Client
from colorama import init as cinit
from time import sleep
cinit()

system('cls')
system('title Charlie^ Mike\'s^ Palworld^ Server')
banner='''\x1b[33m
 ██████╗██╗  ██╗ █████╗ ██████╗ ██╗     ██╗███████╗
██╔════╝██║  ██║██╔══██╗██╔══██╗██║     ██║██╔════╝
██║     ███████║███████║██████╔╝██║     ██║█████╗  
██║     ██╔══██║██╔══██║██╔══██╗██║     ██║██╔══╝  
╚██████╗██║  ██║██║  ██║██║  ██║███████╗██║███████╗
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚══════╝
                                                   
        ███╗   ███╗██╗██╗  ██╗███████╗             
        ████╗ ████║██║██║ ██╔╝██╔════╝             
        ██╔████╔██║██║█████╔╝ █████╗               
        ██║╚██╔╝██║██║██╔═██╗ ██╔══╝               
        ██║ ╚═╝ ██║██║██║  ██╗███████╗             
        ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚══════╝             
                                                   
 █████╗  ██████╗████████╗██╗   ██╗ █████╗ ██╗      
██╔══██╗██╔════╝╚══██╔══╝██║   ██║██╔══██╗██║      
███████║██║        ██║   ██║   ██║███████║██║      
██╔══██║██║        ██║   ██║   ██║██╔══██║██║      
██║  ██║╚██████╗   ██║   ╚██████╔╝██║  ██║███████╗ 
╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝ \x1b'''
print(banner)
print("\x1b[32mWelcome to Palworld!\x1b[0m")

stop = False
def handler(sig, frame):
    global stop
    stop = True
    print("\x1b[36mStopping Server...\x1b[0m This may take a few minutes")
signal.signal(signal.SIGINT, handler)

if not path.exists('.\\PalServer.exe'):
    input("\nPlease place this program in the same folder as 'PalServer.exe\nIf this is a shortcut, open properties and set the \'Start In\' dir'\nPress Enter to Close...\n")
    exit(1)

if not path.exists(".\\Backups"):
    mkdir('Backups')

def getlist():
    a=sorted(listdir(".\\Backups"))
    #print(a, len(a))
    return a

def bup(x):
    shutil.make_archive(x, 'zip', ".\\Pal\\Saved")
    shutil.move(f'{x}.zip', f".\\Backups\\{x}.zip")

def sendcmd(x):
    with Client('localhost', 25575, passwd='') as client:
        response = client.run(x,enforce_id=0)
    print(response)

renabled=0
try:
    sendcmd('info')
    renabled=1
except:
    print("\x1b[33mWarn:\x1b[0m Could not connect to rcon server, did you enable it in\n       PalServer\\Pal\\Saved\\Config\\WindowsServer\\PalWorldSettings.ini\n       Note the server must be stopped before modifying the settings")
    print("\x1b[33mWarn:\x1b[0m Without rcon, corrupt data could overwrite the backups!\n       Enable rcon, or run /save periodically ")
    print("\x1b[36mStarting without rcon \x1b[0m")

while 1 and not stop:
    sleep(300)
    if renabled:
        try:
            sendcmd('save')
            sleep(3)
            bup(str(now()).replace(' ','_').replace(':','-'))
        except:
            print("\x1b[31mError: \x1b[0mConnection to rcon server lost, not saving!")
            input("Press Enter to Close...\n")
            exit(1)
    else:
        if stop:
            break
        bup(str(now()).replace(' ','_').replace(':','-'))

    while len(getlist())>10:
        a=getlist()
        remove(".\\Backups\\"+a[0])
        print("Removed old backups "+a[0])

if stop:
    if renabled:
        print("\x1b[36mSaving world...\x1b[0m")
        sendcmd('save')
        sleep(4)
        print("\x1b[36mSaving Backup\x1b[0m")
        bup("stop")
        print("\x1b[36mSending shutdown command now!\x1b[0m\nServer stopping in 30 seconds, players have been notified.")
        # sendcmd('Shutdown','30', 'Server is shutting down! Please check the discord for more information.')
        # sleep(31)
    exit(0)