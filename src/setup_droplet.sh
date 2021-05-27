#!/bin/bash
yum update -y
#install prerequisite
echo "installing prerequisite"
yum -y install epel-release
yum -y install mosquitto
yum -y install python3.8
yum -y install tmux
#configure mosquitto on startup
echo "configure mosquitto on startup"
systemctl start mosquitto
systemctl enable mosquitto
#setup password
#password stored in passwd file
echo "configuring username & password..."
echo "please key in username: "
read username
mosquitto_passwd -c /etc/mosquitto/passwd $username
echo "please key in password: "
#configure mosquitto.conf to use passwd file
echo "configure mosquitto.conf to use passwd file"
rm -f /etc/mosquitto/mosquitto.conf
echo "please press Ctrl + C"
cat > /etc/mosquitto/mosquitto.conf 
allow_anonymous false 
password_file /etc/mosquitto/passwd
echo "Restarting MQTT broker"
systemctl restart mosquitto
echo "installing python dependencies"
pip3 install -r requirements.txt
echo "setup complete, please configure src/paho-mqtt-client.py based on your mqtt topic & machine advisor credentials"