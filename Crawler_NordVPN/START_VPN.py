# -*- coding: UTF-8 -*-
from os import listdir
from random import *
import os

files = listdir("./NORD_OVPN_230321")
link='./NORD_OVPN_230321/'+files[randint(0,files.__len__()-1)]

os.system('echo ---------------------------------')
os.system('echo '+files[randint(0,files.__len__()-1)]+'\n')
os.system('echo ---------------------------------')
with open(link, 'r') as text:
    mylist = text.readlines()

#mylist.append('auth-user-pass loginpas.txt')
for index,ine in enumerate(mylist):
    if 'auth-user-pass' in ine:
        mylist[index]="auth-user-pass loginpas.txt\n"

    
MyFile = open ('VPN-new.ovpn', 'w') 
MyFile.writelines(mylist) 
MyFile.close()

fi='echo Omegared.# | sudo -S openvpn ./VPN-new.ovpn'
os.system(fi)