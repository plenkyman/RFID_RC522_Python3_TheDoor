import sys
import os
import time
import datetime
import RPi.GPIO as GPIO
import TheDoorPrefs as tdp
#############################################################################################
####	 Copyright 2014 (BSD License) Credits:  Florian Otto(Solider) and hadara		  ###
####					based on http://bsd.ee/~hadara/blog/?p=1017&cpage=1 			  ###
####	------------------------------------------------------------------------------ 	  ###
####						remixed by plenkyman, Version 8					  			  ###
#############################################################################################
#############################################################################################
#########		    ! ! make any modifications in TheDoorPrefs.py ! ! 		    #############
#########						 ! ! DO NOT MODIFY ! ! 							#############
#############################################################################################
###	System
rpi_ip=tdp.rpi_ip								
p2=tdp.p2										
p2r=tdp.p2r		
p2door=tdp.p2door					
pathtoscript=tdp.pathtoscript				
logf=tdp.logf				
logpi=tdp.logpi		
bkuppath=tdp.bkuppath			
bkupusr=tdp.bkupusr						
###	mysql
dbNa=tdp.dbNa							
dbKe=tdp.dbKe								
dbAc=tdp.dbAc									
dbUs=tdp.dbUs								
dbPW=tdp.dbPW							
###	LED
green=tdp.green									
red=tdp.red										
yellow=tdp.yellow									
pstat=tdp.pstat
###	Relay Door
d_strike=tdp.d_strike							
d_unused=tdp.d_unused							
d_time=tdp.d_time								
d_exit=tdp.d_exit									
### 	Pi Camera
OnOffPiCam=tdp.OnOffPiCam							
path_to_pics=tdp.path_to_pics					
picem=tdp.picem									
camff=tdp.camff								
camrot=tdp.camrot								
errLine=tdp.errLine					
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
