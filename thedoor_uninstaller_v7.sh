#!bin/bash
echo "This Uninstaller will remove all files from Thedoor"
echo "The apt-get and subversion modules installed will remain!"
read -p "Enter the mysql database root password: " db_pw_root
mysql -D RfidDoor -u root -p$db_pw_root -e "DROP USER TheDoor@'%'"
mysql -D RfidDoor -u root -p$db_pw_root -e "DROP USER TheDoor@'localhost'"
mysql -D RfidDoor -u root -p$db_pw_root -e "DROP Database RfidDoor"
rm -rf ~/thedoor/
rm -rf ~/bcm2835-1.50/
rm -rf ~/rpi-rc522-read-only/
rm ~/.doorconf
rm ~/.bash_aliases
sudo rm /etc/cron.d/doorcrons
echo "all removed!"
rm thedoor_uninstaller_v*
echo "the pi will restart in 60 seconds"
sudo shutdown -r +1
