# RFID_RC522_Python3_TheDoor
Access System based on a raspberry pi, RC522 Rfid reader, python3

Copyright 2014 (BSD License) Credits:  Florian Otto(Solider) and hadara
based on http://bsd.ee/~hadara/blog/?p=1017&cpage=1
remixed by plenkyman	v.7.March2016

Hardware:
Raspberry Pi & Pi Camera,
Edimax USB Wifi Dongle: http://amzn.com/B00UGBI91U,
RFID-RC522: http://amzn.com/B016BLFMMW,
Relay: http://amzn.com/B00E0NTPP4,
Electric Strike: http://amzn.com/B00V49S65M,
ExitButton:  http://amzn.com/B00G4ST666

complete install & uninstall scripts

Detailed installation instructions in help_installation.txt

The pi runs itself once properly set up.
TheDoor program restarts itself every 4 hours and reboots the pi once a day.
This program is not attached to any tty and does not print to your screen.

run terminal command setupcards to add or edit cards

House cards give access 24/7.
Guest Cards give access by weekday and weekend schedule.

The OverRide card disables access control and opens the lock permanently.
Swipe the card once more to enable access control again.

If a PiCamera is installed and enabled in TheDoorConfig.py it takes pictures
when:
access is denied because of a revoked, out of schedule or unknown card.
Pictures are stored in ~/thedoor/images.

Monitor this program in terminal over ssh.
To see logs of door access either use terminal command ldoor or dbdoor.
To see logs of script activity use terminal command lpi.
To see all registered cards use terminal command dbcards.

all newly available commands:

- restartdoor	 : - tries to quit the reader and the python file then restarts
									 them again
- quitdoo	 		 : - quits the rc522_reader and the python program
- restartpi01	 : - restarts pi and starts the door at boot
- dbdoor	 		 : - shows attendance, the last 100 entries of mysql database
							 table AccLog
- dbcard	 		 : - shows registered cards, mysql table RfidCards all cards
- lpi		 			 : - shows logs of the custom scripts executed   
- ldoor				 : - shows logs of attendance
- cleanlogs		 : - erases all but the last 500 lines of lpi and ldoor
- backupdoor	 : - backs up to another machine by rsync if path and login are
									 defined in TheDoorConfig.py, wait for command line prompt
									 to enter password.
- resetconfig	 : - reset TheDoorConfig file and create doorconf, run after
									 changes in TheDoorConfig.py, then run restartdoor.
- setupcards	 : - use this to setup the first 4 cards as programming cards
- setdoorprefs : - Set GPIO pins and PiCam settings
