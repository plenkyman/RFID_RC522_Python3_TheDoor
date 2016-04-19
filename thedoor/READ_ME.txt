###############################################################################################
####		Copyright 2014 (BSD License) Credits:  Florian Otto(Solider) and hadara     	###
####					based on http://bsd.ee/~hadara/blog/?p=1017&cpage=1 				###
####	--------------------------------------------------------------------------------	###		           		
####									remixed by plenkyman	V.17.March2016				###
###############################################################################################

Detailed installation instructions in help_installation.txt

First of all the pi has to be connected to the internet and additional modules and software installed
as specified in the help_installation file.

The pi runs itself once properly set up.
TheDoor program restarts itself every 4 hours and reboots the pi once a day.
This program is not attached to any tty and does not print to your screen.

If you have followed the installation instructions you will have cards to write new cards, House or Guest.
Swipe MakeCards once, all LED go on, swipe the new unknown card, green and yellow LED turn off.
New Card is programmed. Use MySQLWorkbench or similar to edit Name of cards.

House cards give access 24/7.
Guest Cards give access by weekday and weekend schedule.

The OverRide card disables access control and opens the lock permanently.
Swipe the card once more to enable access control again.

If a PiCamera is installed and enabled in TheDoorConfig.py it takes pictures when:
access is denied because of a revoked, out of schedule or unknown card.
pictires are stored in /thedoor/images.

Monitor this program in terminal over ssh.
To see logs of door access either use ldoor or dbdoor.
To see logs of script activity use lpi.
To see all registered cards use dbcards.

all newly available commands:

restartdoor  	tries to quit the reader and the python file then restarts them again
quitdoor		quits the rc522_reader and the python program
restartpi01		restarts pi and starts the door at boot 
dbdoor			shows attendance, the last 100 entries of mysql database table AccLog 
dbcards			shows registered cards, mysql database table RfidCards all cards
lpi				shows logs of the custom scripts executed   
ldoor			shows logs of attendance
cleanlogs		erases all but the last 500 lines of lpi and ldoor
backupdoor		backs up to another machine by rsync if path and login are defined in TheDoorConfig.py,
				wait for command line prompt to enter password.
resetconfig		reset TheDoorConfig file and create doorconf, run after changes in TheDoorConfig.py,
				then run restartdoor.
setupcards		use this to setup the first 4 cards as programming cards	
				
				
				
