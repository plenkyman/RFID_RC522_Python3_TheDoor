#############################################################################################
################           ! ! !  DO MODIFY IF YOU MUST ! ! !         #######################
#################### freely provided by plenkyman, Version 8 ################################
###	System
rpi_ip="localhost" 							### Raspberry's ip-address
p2="file"									### print to "terminal or file"
p2r="/home/pi/rpi-rc522-read-only/rc522/"	### path to the reader directory
p2door="/home/pi/thedoor/"					### path to thedoor directory
pathtoscript=p2door+"scripts/"				### path to shell scripts directory
logf=p2door+"logs/TheDoor.log"				### path to TheDoor log file
logpi=p2door+"/logs/pi_user_door.log"		### path to pi log file
bkuppath="~/BackUpsFromPi01/thedoor"		### path to another machine for backup
bkupusr="pi@192.168.1.15"					### user and ip of other machine to backup
###	mysql
dbNa="RfidDoor"								### mysql database
dbKe="RfidCards"							### mysql RFID cards table
dbAc="AccLog"								### mysql log table
dbUs="TheDoor"								### mysql username
dbPW="FerdinandTheCat"								### mysql password
###	LED
green=7										### GPIO for the green LED
red=8										### GPIO for the red LED
yellow=11									### GPIO for the yellow LED
pstat=13									### GPIO for the Power Status LED
###	Relay Door
d_strike=16									### GPIO for the door strike relay
d_unused=36									### GPIO unused Relay
d_time=3									### seconds door stays unlocked
d_exit=38									### GPIO for Exit push button
### 	Pi Camera
OnOffPiCam="on"								### PiCamera(on,off) use off if no cam connected
path_to_pics=p2door+"images/"				### the path where the pics get stored
picem="auto"								### PiCamera exposure mode (auto,night,etc...)
camff="jpg"									### PiCamera file format
camrot=90									### PiCamera image rotation (0/90/180/270)
errLine="""### ! ###"""						### Text that encapsulates special events
#############################################################################################
