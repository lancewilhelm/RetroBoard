#!/bin/bash

sudo apt-get update
sudo apt-get install python3-pip
pip3 install flask flask-cors
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/rgb-matrix.sh >rgb-matrix.sh
sudo bash rgb-matrix.sh