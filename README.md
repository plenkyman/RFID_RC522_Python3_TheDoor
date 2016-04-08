# RFID_RC522_Python3_TheDoor
Access System based on a raspberry pi, RC522 Rfid reader, python3

- simple install script. 

The pi runs itself once properly set up.

download and transfer raspian Jessie to SD Card from
https://www.raspberrypi.org/downloads/raspbian/

start Raspberry with screen, keyboard and mouse connected, it will start up in X by default.

set up raspi with user "pi", establish internet connection, go thru basic setup:
   - set password, hostname, use device tree, Console Autologin Text console,
    automatically logged in as 'pi' user, enable SPI + Camera, set locale, timezone, keyboard
    and wificountry.

reboot ! mandatory!

after rebooting to terminal:
			
1.	wget http://www.plenkyman.com/installthedoor.sh
2.	sh installthedoor.sh
			
This will take around 20 minutes, it will update and upgrade apt-get, install subversion and mysql, pypy pymysql, 
you will have to accept 3 prompts and enter a root password for mysql.
The Rasperry will shut down when installation is finished.

After reboot run the SetupCards.py by running setupcards in terminal.
follow prompts to set up the programming and your personal access card.

Hardware:
Raspberry Pi, Pi Camera, Edimax USB Wifi Dongle: http://amzn.com/B00UGBI91U,
RFID-RC522: http://amzn.com/B016BLFMMW,
Relay: http://amzn.com/B00E0NTPP4,
Electric Strike: http://amzn.com/B00V49S65M,
ExitButton:  http://amzn.com/B00G4ST666,

Copyright 2014 (BSD License) Credits:  Florian Otto(Solider) and hadara
based on http://bsd.ee/~hadara/blog/?p=1017&cpage=1
remixed by plenkyman	V.17.March2016


