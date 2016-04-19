import sys
import os
import time
import datetime
import RPi.GPIO as GPIO
###############################################################################################
####		Copyright 2014 (BSD License) Credits:  Florian Otto(Solider) and hadara			###
####					based on http://bsd.ee/~hadara/blog/?p=1017&cpage=1 				###
####	--------------------------------------------------------------------------------	###
####							remixed by plenkyman, March 2016							###
###############################################################################################
###	System
rpi_ip="localhost" 								### Raspberry's ip-address
p2 = "file"										### print to "terminal or file"
p2r="/home/pi/rpi-rc522-read-only/rc522/"		### path to the reader directory
p2door = "/home/pi/thedoor/"					### path to thedoor directory
pathtoscript = p2door+"scripts/"				### path to shell scripts directory
logf = p2door+"logs/TheDoor.log"				### path to TheDoor log file
logpi = p2door+"/logs/pi_user_door.log"			### path to pi log file
bkuppath = "~/BackUpsFromPi01/thedoor"			### path to another machine for backup
bkupusr = "pi@192.168.1.15"						### user and ip of other machine to backup
###	mysql
dbNa = "RfidDoor"								### mysql database
dbKe = "RfidCards"								### mysql RFID cards table
dbAc = "AccLog"									### mysql log table
dbUs = "TheDoor"								### mysql username
dbPW = "Schmilblick"							### mysql password
###	LED
green = 7										### GPIO for the green LED
red = 8											### GPIO for the red LED
yellow = 11										### GPIO for the yellow LED
pstat = 13										### GPIO for the Power Status LED
###	Relay Door
d_strike = 16									### GPIO for the door strike relay
d_unused = 36									### GPIO unused Relay
d_time = 3										### seconds door stays unlocked
d_exit = 38										### GPIO for Exit push button
### 	Pi Camera
OnOffPiCam = "on"								### PiCamera(on,off) use off if no cam connected
path_to_pics = p2door+"images/"					### the path where the pics get stored
picem = 'night'									### PiCamera exposure mode (auto,night,etc...)
camff = "jpg"									### PiCamera file format
camrot = 180									### PiCamera image rotation (0/90/180/270)
errLine = """### ! ###"""						### Text that encapsulates special events
#############################################################################################
#########		 ! ! CODE BELOW MAKES CONFIG FILE IN HOME DIRECTORY ! ! 		#############
#########						 ! ! DO NOT MODIFY ! ! 							#############
#############################################################################################

def pfromConfig(*args):
    if p2 == "terminal":
        for arg in args:
            print (arg),
    elif p2 == "file":
        fh = open(logpi,"a")
        for arg in args:
            print (arg, file=fh),
            fh.close()
    else: pass

def mk_doorconf():
    bashline1="pathtoreader="+p2r+"\n"
    bashline2="pathtodoor="+p2door+"\n"
    bashline3="pathtologf="+logf+"\n"
    bashline4="pathtologpi="+logpi+"\n"
    bashline5="logrsyncbackup="+bkupusr+":"+bkuppath+"\n"
    bashline6="dbpath="+rpi_ip+"\n"
    bashline7="dbname="+dbNa+"\n"
    bashline8="dbusr="+dbUs+"\n"
    bashline9="dbpwd="+dbPW+"\n"

    f = open('/home/pi/.doorconf', 'w')
    f.write('#!/bin/bash\n')
    f.write(bashline1)
    f.write(bashline2)
    f.write(bashline3)
    f.write(bashline4)
    f.write(bashline5)
    f.write(bashline6)
    f.write(bashline7)
    f.write(bashline8)
    f.write(bashline9)
    f.close()
#############################################################################################
if __name__ == "__main__":
    mk_doorconf()
    pfromConfig(time.strftime("%H:%M:%S-%m-%d-%y")+ " : " + "TheDoorConfig is reset")
