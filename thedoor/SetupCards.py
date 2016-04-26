#!/usr/bin/python3
##########################################################################################
####	Copyright 2014 (BSD License) Credits:  Florian Otto(Solider) and hadara
####					based on http://bsd.ee/~hadara/blog/?p=1017&cpage=1
####--------------------------------------------------------------------------------------
#### VCC- pin 1, 3.3 volts ||| RST- pin 22, GPIO25 ||| GND- pins, 6, 9, 14, 20, or 25,
####	MISO- pin 21, GPIO9 ||| MOSI- pin 19, GPIO10 ||| SCK- pin 23, GPIO11
####	NSS- pin 24, GPIO7 ||| IRQ- Don’t Attach to rpi
####--------------------------------------------------------------------------------------
####						remixed by plenkyman  Version 8
##########################################################################################
####  			! ! THIS PROGRAM SETS UP THE CARDS, NOTHING TO MODIFY ! !
##########################################################################################
import TheDoorPrefs as tdp
import shlex
import subprocess
import sys
import os
import time
import picamera
import datetime
import pymysql
import RPi.GPIO as GPIO
import _thread
### enter boot up in database
connection = pymysql.connect(host=tdp.rpi_ip,unix_socket='/var/run/mysqld/mysqld.sock', user=tdp.dbUs, passwd=tdp.dbPW, db=tdp.dbNa)
cursor = connection.cursor()
cursor.execute("""INSERT INTO """+(tdp.dbAc)+"""(id,acc,card,nam,err) VALUES ('0',NOW(),'python','pi01 at boot','program booted')""")
cursor.close()
connection.commit()
connection.close ()
### initial setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(tdp.green, GPIO.OUT)
GPIO.setup(tdp.red, GPIO.OUT)
GPIO.setup(tdp.yellow, GPIO.OUT)
GPIO.setup(tdp.pstat,GPIO.OUT)
GPIO.setup(tdp.d_strike, GPIO.OUT)
GPIO.setup(tdp.d_unused, GPIO.OUT)
GPIO.setup(tdp.d_exit, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def blink(Color,bkg = 5):
    i=0
    while i <= bkg :
        GPIO.output(Color,1)
        time.sleep(.03)
        GPIO.output(Color,0)
        time.sleep(.03)
        i = i + 1
    else:
        GPIO.output(Color,0)
    ledsGRY(False,True,False)

def ledsGRY(st1,st2,st3):
    GPIO.output(tdp.green,st1)
    GPIO.output(tdp.red,st2)
    GPIO.output(tdp.yellow,st3)

def printto(wichlog,*args):
    for arg in args:
        print (arg),


def takepict(fn,err):
    if tdp.OnOffPiCam == "on":
        camera = picamera.PiCamera()
        camera.exposure_mode = tdp.picem
        camera.rotation = tdp.camrot
        time.sleep(.1)
        camera.capture(tdp.path_to_pics+time.strftime("%y-%m-%d_%H:%M:%S")+'_'+fn+'_'+err+'.'+tdp.camff)
        camera.close()
    else: return None

def scheduled_access(weekdays):
    if (str(datetime.datetime.today().weekday()) in weekdays) is True:
        thisHour = datetime.datetime.today().hour
        if datetime.datetime.today().weekday() <= 4 and thisHour >= hours_wk_st - 1 and thisHour <=hours_wk_end - 1:
            return True
        elif datetime.datetime.today().weekday() >= 5 and thisHour >= hours_wkend_st -1 and thisHour <=hours_wkend_end -1:
            return True
        else:
            return False
    else:
        return False

def opendoor():
    GPIO.remove_event_detect(tdp.d_exit)
    GPIO.output(tdp.d_strike,0)
    time.sleep(tdp.d_time)
    GPIO.output(tdp.d_strike,1)
    GPIO.add_event_detect(tdp.d_exit, GPIO.FALLING, callback = exitbutton_callback, bouncetime = (tdp.d_time * 1000) + 500)

def exitbutton_callback(channel) :
    GPIO.output(tdp.d_strike,0)
    if OverRide == "A":
        ledsGRY(False,False,False)
        _thread.start_new_thread(blink, (tdp.green,42))
        printto(tdp.logf,time.strftime("%c")+ " : Exit Button")
        time.sleep(tdp.d_time)
        GPIO.output(tdp.d_strike,1)
        ledsGRY(False,True,False)
    else:
        printto(tdp.logf,time.strftime("%c") + " : Exit Button, Door on OverRide")
############# READING CARDS RC522 #############################
class RFIDReaderWrapper(object):
    #_thread.start_new_thread(powerstatus, ())
    """runs rfid reader as a subprocess & parses tag serials
    from its output
    """
    def __init__(self, cmd):
        self._cmd_list = shlex.split(cmd)
        self._subprocess = None
        self._init_subprocess()

    def _init_subprocess(self):
        self._subprocess = subprocess.Popen(self._cmd_list,
            stderr=subprocess.PIPE)

    def read_tag_serial(self):
        """blocks until new tag is read
        returns serial of the tag once the read happens
        """
        if not self._subprocess:
            self._init_subprocess()

        while 1:
            line = self._subprocess.stderr.readline()
            if isinstance(line, bytes):
                # python3 compat
                line = line.decode("utf-8")

            if line == '':
                # EOF
                return None

            if not line.startswith("New tag"):
                continue

            serial = line.split()[-1].split("=", 1)[1]
            return serial
####### SET STATE TO BEGIN  #############
OverRide = "A"
GPIO.setwarnings(True)
GPIO.output(tdp.d_strike,1)
GPIO.output(tdp.d_unused,0)
ledsGRY(True,True,True)
printto(tdp.logpi,time.strftime("%H:%M:%S-%m-%d-%y")+" : ### Swipe a card or cancel with control c ###")
####### RUNNING THE READER  #############
try:
    if __name__ == '__main__':
        reader = RFIDReaderWrapper("sudo nohup "+tdp.p2r+"/rc522_reader -d 2>&1")
        name=""
        GPIO.add_event_detect(tdp.d_exit, GPIO.FALLING, callback = exitbutton_callback, bouncetime = (tdp.d_time * 1000) + 500)
        while True:
            connection = pymysql.connect(host=tdp.rpi_ip,unix_socket='/var/run/mysqld/mysqld.sock', user=tdp.dbUs, passwd=tdp.dbPW, db=tdp.dbNa)
            cursor = connection.cursor()
            serial = reader.read_tag_serial()
            cursor.execute("""SELECT name,acc_group,counter,access,weekdays,hours_wk_st,hours_wk_end,hours_wkend_st,hours_wkend_end FROM """+(tdp.dbKe)+""" WHERE ID=(%s)""", (serial))
            for row in cursor.fetchall():
                name = str(row[0])
                acc_group = str(row[1])
                counter = int(row[2])
                access = int(row[3])
                weekdays = str(row[4])
                hours_wk_st = int(row[5])
                hours_wk_end = int(row[6])
                hours_wkend_st = int(row[7])
                hours_wkend_end = int(row[8])

            if name=="":
                _thread.start_new_thread(blink, (tdp.yellow,50))
                print ("Swipe cards to register. control c to exit program: ")
                nametocard = input("Enter Name of cardholder: ")
                print ("Chose wich type of acces right for this card: ")
                print ("1. House Card, access granted 24/7")
                print ("2. Guest Card, access by schedule")
                print ("3. OverRide Card, Programming")
                print ("4. Make House Cards, Programming")
                print ("5. Make Guest Cards, Programming")
                print ("0. Revoke this card")
                accesstocard = int(input("Chose 1 - 5 or 0 : "))
                cursor.execute("""INSERT INTO """+(tdp.dbKe)+"""(ID,name,access) VALUES ((%s),(%s),(%s))""",(serial,nametocard,accesstocard));
                print ("card written to database, swipe another card or quit (control c)")
### known card cards
            elif name!="":
                _thread.start_new_thread(blink, (tdp.yellow,50))
                print ("This card is already registerd as: ",name," and has an accesslevel of: ",access,"")
                print ("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
                print ("Do you want to edit this card? ")
                print ("1. Edit this card ")
                print ("2. go back swipe a new card ")
                print ("3. quit this program ")
                selectaction = int(input("Choose 1 - 3: "))
                if selectaction == 1:
                    nametocard = input("Enter new Name for cardholder: ")
                    print ("Chose wich type of acces right for this card: ")
                    print ("1. House Card, access granted 24/7")
                    print ("2. Guest Card, access by schedule")
                    print ("3. OverRide Card, Programming")
                    print ("4. Make House Cards, Programming")
                    print ("5. Make Guest Cards, Programming")
                    print ("0. Revoke this card")
                    accesstocard = int(input("Chose 1 - 5 or 0 : "))
                    cursor.execute("""UPDATE """+(tdp.dbKe)+""" SET name = (%s), access = (%s) WHERE ID = (%s)""",(nametocard,accesstocard,serial));
                    print ("card updated on database, swipe another card or quit (control c)")
                if selectaction == 2:
                    print ("swipe a card or quit (control c)")
                    pass
                if selectaction == 3:
                    print ("quiting Setupcards.py")
                    sys.exit(0)
            cursor.close()
            connection.commit()
            connection.close ()
            name=""

except BaseException as error:
    ledsGRY(False,False,False)
    GPIO.cleanup()
    cursor.close()
    connection.commit()
    connection.close ()
finally:
    printto(tdp.logpi,time.strftime("%H:%M:%S-%m-%d-%y") + " : " + tdp.errLine +"restartdoor after SetupCards")
    os.system(tdp.pathtoscript + "restartdoor")
    sys.exit(0)
