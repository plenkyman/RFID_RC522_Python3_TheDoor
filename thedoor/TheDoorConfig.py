import sys
import os
import time
import datetime
import RPi.GPIO as GPIO
import TheDoorPrefs as tdp
#############################################################################################
# This program writes the .doorconf on installation or when called in terminal: resetconfig #
#############################################################################################
#########		 ! ! CODE BELOW MAKES CONFIG FILE IN HOME DIRECTORY ! ! 		#############
#########						 ! ! DO NOT MODIFY ! ! 							#############
#############################################################################################

def pfromConfig(*args):
    if tdp.p2 == "terminal":
        for arg in args:
            print (arg),
    elif tdp.p2 == "file":
        fh = open(tdp.logpi,"a")
        for arg in args:
            print (arg, file=fh),
            fh.close()
    else: pass

def mk_doorconf():
    bashline1="pathtoreader="+tdp.p2r+"\n"
    bashline2="pathtodoor="+tdp.p2door+"\n"
    bashline3="pathtologf="+tdp.logf+"\n"
    bashline4="pathtologpi="+tdp.logpi+"\n"
    bashline5="logrsyncbackup="+tdp.bkupusr+":"+tdp.bkuppath+"\n"
    bashline6="dbpath="+tdp.rpi_ip+"\n"
    bashline7="dbname="+tdp.dbNa+"\n"
    bashline8="dbusr="+tdp.dbUs+"\n"
    bashline9="dbpwd="+tdp.dbPW+"\n"

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
