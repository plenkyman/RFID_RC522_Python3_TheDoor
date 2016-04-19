#!/usr/bin/python3
##########################################################################################
####	Copyright 2014 (BSD License) Credits:  Florian Otto(Solider) and hadara
####					based on http://bsd.ee/~hadara/blog/?p=1017&cpage=1
####--------------------------------------------------------------------------------------
#### VCC- pin 1, 3.3 volts ||| RST- pin 22, GPIO25 ||| GND- pins, 6, 9, 14, 20, or 25,
####	MISO- pin 21, GPIO9 ||| MOSI- pin 19, GPIO10 ||| SCK- pin 23, GPIO11
####	NSS- pin 24, GPIO7 ||| IRQ- Don’t Attach to rpi
####--------------------------------------------------------------------------------------
####								remixed by plenkyman
##########################################################################################
####  			! ! THIS PROGRAM RUNS THE READER, NOTHING TO MODIFY ! !
##########################################################################################
import TheDoorConfig as tdc
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
connection = pymysql.connect(host=tdc.rpi_ip,unix_socket='/var/run/mysqld/mysqld.sock', user=tdc.dbUs, passwd=tdc.dbPW, db=tdc.dbNa)
cursor = connection.cursor()
cursor.execute("""INSERT INTO """+(tdc.dbAc)+"""(id,acc,card,nam,err) VALUES ('0',NOW(),'python','pi01 at boot','program booted')""")
cursor.close()
connection.commit()
connection.close ()
### initial setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(tdc.green, GPIO.OUT) 
GPIO.setup(tdc.red, GPIO.OUT) 
GPIO.setup(tdc.yellow, GPIO.OUT) 
GPIO.setup(tdc.pstat,GPIO.OUT)
GPIO.setup(tdc.d_strike, GPIO.OUT)
GPIO.setup(tdc.d_unused, GPIO.OUT)
GPIO.setup(tdc.d_exit, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def powerstatus():
    tOn = 1
    tOff = .5
    exz = .99
    while 1:
        GPIO.output(tdc.pstat, True)
        time.sleep(tOn)
        GPIO.output(tdc.pstat, False)
        time.sleep(tOff)
        tOn = tOn * exz
        tOff = tOff * exz
        if tOn < .015:
           exz = 1.01
        elif tOn >= 1:
           exz = .99 

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
    GPIO.output(tdc.green,st1)
    GPIO.output(tdc.red,st2)
    GPIO.output(tdc.yellow,st3)

def printto(wichlog,*args):
    if tdc.p2 == "terminal":
        for arg in args:
            print (arg),
    elif tdc.p2 == "file":
        fh = open(wichlog,"a")
        for arg in args:
            print (arg, file=fh),
            fh.close()
    else: pass

def takepict(fn,err):
    if tdc.OnOffPiCam == "on":
        camera = picamera.PiCamera()
        camera.exposure_mode = tdc.picem
        camera.rotation = tdc.camrot
        time.sleep(.1)
        camera.capture(tdc.path_to_pics+time.strftime("%y-%m-%d_%H:%M:%S")+'_'+fn+'_'+err+'.'+tdc.camff)
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
    GPIO.remove_event_detect(tdc.d_exit)
    GPIO.output(tdc.d_strike,0)
    time.sleep(tdc.d_time)
    GPIO.output(tdc.d_strike,1)
    GPIO.add_event_detect(tdc.d_exit, GPIO.FALLING, callback = exitbutton_callback, bouncetime = (tdc.d_time * 1000) + 500)

def exitbutton_callback(channel) :
    GPIO.output(tdc.d_strike,0)
    if OverRide == "A":
        ledsGRY(False,False,False)
        _thread.start_new_thread(blink, (tdc.green,42))
        printto(tdc.logf,time.strftime("%c")+ " : Exit Button")
        time.sleep(tdc.d_time)
        GPIO.output(tdc.d_strike,1)
        ledsGRY(False,True,False)
    else:
        printto(tdc.logf,time.strftime("%c") + " : Exit Button, Door on OverRide")
############# READING CARDS RC522 #############################
class RFIDReaderWrapper(object):
    _thread.start_new_thread(powerstatus, ())
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
GPIO.output(tdc.d_strike,1)
GPIO.output(tdc.d_unused,0)
ledsGRY(False,True,False)
printto(tdc.logpi,time.strftime("%H:%M:%S-%m-%d-%y")+" : ### initialized and booted ###")                        
####### RUNNING THE READER  #############
try:
    if __name__ == '__main__':
        reader = RFIDReaderWrapper("sudo nohup "+tdc.p2r+"/rc522_reader -d 2>&1")
        name=""
        GPIO.add_event_detect(tdc.d_exit, GPIO.FALLING, callback = exitbutton_callback, bouncetime = (tdc.d_time * 1000) + 500)
        while True:
            connection = pymysql.connect(host=tdc.rpi_ip,unix_socket='/var/run/mysqld/mysqld.sock', user=tdc.dbUs, passwd=tdc.dbPW, db=tdc.dbNa)
            cursor = connection.cursor()
            serial = reader.read_tag_serial()
### uncomment for special cards,  do not need to be registered.
#             if serial=="[44e9825a]":
#                 printto(tdc.logpi,time.strftime("%H:%M:%S-%m-%d-%y") + " : " + tdc.errLine + " : TheDoor restarted by card")
#                 os.system(tdc.pathtoscript + "restartdoor")
#             if serial=="[94be7d5a]":
#                 printto(tdc.logpi,time.strftime("%H:%M:%S-%m-%d-%y") +" : " + tdc.errLine + " : pi01 rebooted by card")
#                 os.system(tdc.pathtoscript + "restartpi01")

            cursor.execute("""SELECT name,acc_group,counter,access,weekdays,hours_wk_st,hours_wk_end,hours_wkend_st,hours_wkend_end FROM """+(tdc.dbKe)+""" WHERE ID=(%s)""", (serial))
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

            if not name=="":
### access for house cards
                if access == 1 and OverRide == "A":
                    ledsGRY(True,False,False)
                    printto(tdc.logf,time.strftime("%c")+" : . . "+name)
                    _thread.start_new_thread(blink, (tdc.green,50))
                    opendoor()
                    cursor.execute("""UPDATE """+(tdc.dbKe)+""" SET counter = counter + 1 WHERE ID = (%s)""",(serial));
                    cursor.execute("""INSERT INTO """+(tdc.dbAc)+"""(id,acc,card,nam,err) VALUES ('0',NOW(),(%s),(%s),(%s))""",(serial,name,acc_group))
### access for members cards
                elif access == 2 and OverRide == "A" and scheduled_access(weekdays) is True:
                    ledsGRY(True,False,False)
                    printto(tdc.logf,time.strftime("%c")+" : . . . . "+name)
                    _thread.start_new_thread(blink, (tdc.green,50))
                    opendoor()
                    cursor.execute("""UPDATE """+(tdc.dbKe)+""" SET counter = counter + 1 WHERE ID = (%s)""",(serial));
                    cursor.execute("""INSERT INTO """+(tdc.dbAc)+"""(id,acc,card,nam,err) VALUES ('0',NOW(),(%s),(%s),(%s))""",(serial,name,acc_group))
### out of schedule members
                elif access == 2 and OverRide == "A" and scheduled_access(weekdays) is False:
                    ledsGRY(True,False,False)
                    _thread.start_new_thread(blink, (tdc.red,30))
                    _thread.start_new_thread(takepict, (name,"NoAccess"))
                    cursor.execute("""INSERT INTO """+(tdc.dbAc)+""" (id,acc,card,nam,err) VALUES ('0',NOW(),(%s),(%s),'NoAccess')""",(serial,name))
                    printto(tdc.logf,time.strftime("%c")+ " : " + tdc.errLine + name + ",you don't have access at this time.")
### revoked card
                elif access == 0 and OverRide == "A":
                    _thread.start_new_thread(blink, (tdc.red,50))
                    printto(tdc.logf,time.strftime("%c") +  " : " + tdc.errLine + ": revoked card!")
                    cursor.execute("""INSERT INTO """+(tdc.dbAc)+""" (id,acc,card,nam,err) VALUES ('0',NOW(),(%s),(%s),'RevokedCard')""",(serial,name))
                    _thread.start_new_thread(takepict, (name,"RevokedCard"))
### override rfid, door opened
                elif access == 3 and OverRide == "A":
                    cursor.execute("""INSERT INTO """+(tdc.dbAc)+""" (id,acc,card,nam,err) VALUES ('0',NOW(),(%s),(%s),'OverRide_OPEN')""",(serial,name))
                    OverRide = "B"
                    GPIO.output(tdc.d_strike,0)
                    printto(tdc.logf,time.strftime("%c")+" : manual override, Door is OPEN!")
                    ledsGRY(True,True,True)
### cancel override and make-cards, door closed
                elif access == 3 and OverRide == "B" or access == 3 and OverRide == "C" or access == 3 and OverRide == "D":
                    cursor.execute("""INSERT INTO """+(tdc.dbAc)+""" (id,acc,card,nam,err) VALUES ('0',NOW(),(%s),(%s),'OverRide_Closed')""",(serial,name))
                    OverRide = "A"
                    _thread.start_new_thread(blink, (tdc.red,20))
                    _thread.start_new_thread(blink, (tdc.green,20))
                    _thread.start_new_thread(blink, (tdc.yellow,20))
                    GPIO.output(tdc.d_strike,1)
                    printto(tdc.logf,time.strftime("%c") + " : override aborted, Door is CLOSED!")
                    blink(tdc.red,35)
### make house card
                elif access == 4:
                    OverRide = "C"
                    cursor.execute("""INSERT INTO """+(tdc.dbAc)+""" (id,acc,card,nam,err) VALUES ('0',NOW(),(%s),'MkNewHouseCard','MkNewHouse')""",(serial))
                    ledsGRY(True,True,True)
                    printto(tdc.logf,time.strftime("%c")+" : make house card, swipe new card")
### make guest card
                elif access == 5:
                    OverRide = "D"
                    cursor.execute("""INSERT INTO """+(tdc.dbAc)+""" (id,acc,card,nam,err) VALUES ('0',NOW(),(%s),'MkNewGuestCard','MkNewGuest')""",(serial))
                    ledsGRY(True,True,True)
                    printto(tdc.logf,time.strftime("%c")+" : make guest card, swipe new card")    
#### write new house card to Database
            elif OverRide == "C":
                _thread.start_new_thread(blink, (tdc.yellow,30))
                cursor.execute("""INSERT INTO """+(tdc.dbAc)+""" (id,acc,card,nam,err) VALUES ('0',NOW(),(%s),'House Registerd','MkNewHouse')""",(serial))
                cursor.execute("""INSERT INTO """+(tdc.dbKe)+""" (ID,name,counter,acc_group,access) VALUES ((%s),"<----NewHouse",'1','house','1')""", (serial))
                printto(tdc.logf,time.strftime("%c") + " : " + tdc.errLine + ": new HOUSE card registerd " + serial)
                OverRide = "A" 
#### write new guest card to Database
            elif OverRide == "D":
                _thread.start_new_thread(blink, (tdc.yellow,30))
                cursor.execute("""INSERT INTO """+(tdc.dbAc)+""" (id,acc,card,nam,err) VALUES ('0',NOW(),(%s),'Guest Registerd','MkNewGuest')""",(serial))
                cursor.execute("""INSERT INTO """+(tdc.dbKe)+""" (ID,name,counter,acc_group,access,weekdays) VALUES ((%s),"<----NewGuest",'1','work','2',"'0','1','2','3','4','5','6'")""", (serial))
                printto(tdc.logf,time.strftime("%c") + " : " + tdc.errLine + ": new GUEST card registerd " + serial) 
                OverRide = "A" 
### unknown cards
            else: 
                printto(tdc.logf,time.strftime("%c")+ " : " + tdc.errLine + "unknown card!" + serial)
                cursor.execute("""INSERT INTO """+(tdc.dbAc)+""" (id,acc,card,nam,err) VALUES ('0',NOW(),(%s),'unknown','UnknownCard')""",(serial))
                _thread.start_new_thread(takepict, ("unknown","UnknownCard"))
                _thread.start_new_thread(blink, (tdc.yellow,50))
                _thread.start_new_thread(blink, (tdc.red,50))
                _thread.start_new_thread(blink, (tdc.green,50))
            cursor.close()
            connection.commit()
            connection.close ()
            name=""
except (KeyboardInterrupt, SystemExit):
    ledsGRY(False,False,False)
    GPIO.output(tdc.pstat, False)
    GPIO.cleanup()
    cursor.close()
    connection.commit()
    connection.close ()
    printto(tdc.logpi,time.strftime("%H:%M:%S-%m-%d-%y") + " : " + tdc.errLine + "!!! KBinterruptOrSysEx !!!")
    sys.exit(0)

except BaseException as error:
    printto(tdc.logpi,time.strftime("%H:%M:%S-%m-%d-%y") + " : " + tdc.errLine + 'BaseException: {}'.format(error))

finally:    
    printto(tdc.logpi,time.strftime("%H:%M:%S-%m-%d-%y") + " : " + tdc.errLine + "TheDoor.py restarting after finally")
    os.system(tdc.pathtoscript + "restartdoor")
    sys.exit(0)
