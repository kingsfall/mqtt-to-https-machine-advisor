#!/bin/bash
yum update -y
#install prerequisite
echo "installing prerequisite"
yum -y install epel-release
yum -y install mosquitto
yum -y install python3.8
yum -y install vim