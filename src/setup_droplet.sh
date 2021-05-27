#!/bin/bash
yum update -y &&

#install prerequisite
yum -y install nano &&
yum -y install epel-release &&
yum -y install mosquitto &&
yum -y install python3.8 &&
yum -y install tmux

#configure mosquitto on startup
systemctl start mosquitto &&
systemctl enable mosquitto

#setup password

#password stored in passwd file
mosquitto_passwd -c /etc/mosquitto/passwd admin
adminpassword

#configure mosquitto.conf to use passwd file
rm -f /etc/mosquitto/mosquitto.conf

cat > /etc/mosquitto/mosquitto.conf 
allow_anonymous false 
password_file /etc/mosquitto/passwd

systemctl restart mosquitto

mosquitto_sub -h localhost -t test -u "admin" -P "adminpassword"
mosquitto_pub -h localhost -t "vm-test/POWERTAG_M262" -m "{"metrics":{"assetName":"Powertag_150","var100":123,"var100_timestamp":1622104416360,"var101":456,"var101_timestamp":1622104416360}}" -u "admin" -P "adminpassword"

#installing python mqtt subscriber
pip3 install paho-mqtt &&
pip3 install requests
