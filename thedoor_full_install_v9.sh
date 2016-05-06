#!bin/bash
clear
echo "This installer connects to the internet, downloads and installs files and changes cron and alias entries"
sleep 1
echo "The entire process takes about 20 minutes on a fast internet connection."
sleep 1
echo "installs: TheDoor python programs from www.thedoor.plenkyman.com"
sleep 1
echo "installs: bcm2835-1.50 from www.airspayce.com"
sleep 1
echo "installs: rpi-rc522 from googlecode.com"
sleep 1
echo "!!! - provided free and without any guarantees - !!!"
sleep 1
while :
do
	read -p "Set a password for the mysql user root: " -s acheck1
	echo " "
	read -p "confirm, enter password for root again: " -s acheck2
	echo " "
	if [ "$acheck1" == "$acheck2" ]
	then
		break
	fi
	echo "entries do not match"
done
db_pw_root=$acheck1
while :
do
	read -p "Set a password for the RfidDoor database for the user TheDoor: " -s bcheck1
	echo " "
	read -p "confirm, enter password for user TheDoor again: " -s bcheck2
	echo " "
	if [ "$bcheck1" == "$bcheck2" ]
	then
		break
	fi
	echo "entries do not match"
done
db_pw_thedoor=$bcheck1
wget http://www.thedoor.plenkyman.com/thedoor.tar.gz
tar -zxvf thedoor.tar.gz
rm thedoor.tar.gz
clear
sudo apt-get update && sudo apt-get -y upgrade
clear
echo mysql-server mysql-server/root_password password "$db_pw_root" | sudo debconf-set-selections
echo mysql-server mysql-server/root_password_again password "$db_pw_root" | sudo debconf-set-selections
sudo apt-get install -y mysql-server pypy
clear
sudo pip3 install pymysql
clear
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.50.tar.gz
tar -zxf bcm2835-1.50.tar.gz
cd bcm2835-1.50
./configure
sudo make install
cd ~
rm bcm2835-1.50.tar.gz
clear
sudo apt-get install -y subversion
clear
svn checkout http://rpi-rc522.googlecode.com/svn/trunk/ rpi-rc522-read-only
cd rpi-rc522-read-only/rc522
gcc config.c rfid.c rc522.c main.c -o rc522_reader -lbcm2835
sudo cp RC522.conf /etc/
cd ~
clear
echo "updated, upgraded, modules installed"
cd /etc/cron.d/
sudo sh -c 'cat /home/pi/thedoor/system/cron_entries.txt > doorcrons'
cd ~
sudo cat thedoor/system/bash_aliases.txt > ~/.bash_aliases
echo "cron and bash aliases installed"
sleep 2
mysql -u root "-p$db_pw_root" -e "create database RfidDoor"
mysql -D RfidDoor -u root "-p$db_pw_root" -e "source thedoor/db_backup/TheDoor.sql"
mysql -u root "-p$db_pw_root" -e "CREATE USER 'TheDoor'@'localhost'IDENTIFIED BY '${db_pw_thedoor}';"
mysql -u root "-p$db_pw_root" -e "CREATE USER 'TheDoor'@'%'IDENTIFIED BY '${db_pw_thedoor}';"
mysql -u root "-p$db_pw_root" -e "GRANT ALL PRIVILEGES ON RfidDoor.* TO 'TheDoor'@'%' WITH GRANT OPTION;"
mysql -u root "-p$db_pw_root" -e "GRANT ALL PRIVILEGES ON RfidDoor.* TO 'TheDoor'@'localhost' WITH GRANT OPTION;"
mysql -D RfidDoor -u root "-p$db_pw_root" -e "flush privileges"
echo "database installed and updated"
sleep 2
cd thedoor/
sed -i "s/TheCat/$db_pw_thedoor/g" TheDoorPrefs.py
python3 TheDoorConfig.py
sleep 2
echo "TheDoor preferences set."

cd ~
rm thedoor_full_install_v*
echo "the pi will restart in 60 seconds."
sleep 60
sudo reboot
