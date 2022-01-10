#!/bin/bash

sudo apt-get update

wget https://nodejs.org/dist/v14.16.1/node-v14.16.1-linux-armv7l.tar.xz

sudo apt-get install python3-pip
sudo apt-get install rabbitmq-server
sudo pip3 install flask flask-cors pillow celery python-dotenv sqlalchemy flower
sudo apt install libopenjp2-7

sudo rabbitmq-server -detached
sudo rabbitmqctl add_user pi raspberry
sudo rabbitmqctl add_vhost myvhost
sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"

wget http://ftp.us.debian.org/debian/pool/main/libs/libseccomp/libseccomp2_2.5.1-1_armhf.deb
sudo dpkg -i libseccomp2_2.5.1-1_armhf.deb

sudo pip3 -v install docker-compose

curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/rgb-matrix.sh >rgb-matrix.sh
sudo bash rgb-matrix.sh