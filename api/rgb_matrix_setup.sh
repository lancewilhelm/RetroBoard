#!/bin/bash

# INSTALLER SCRIPT FOR ADAFRUIT RGB MATRIX BONNET OR HAT

# hzeller/rpi-rgb-led-matrix sees lots of active development!
# That's cool and all, BUT, to avoid tutorial breakage,
# we reference a specific commit (update this as needed):
GITUSER=https://github.com/hzeller
REPO=rpi-rgb-led-matrix
COMMIT=21410d2b0bac006b4a1661594926af347b3ce334
# Previously: COMMIT=e3dd56dcc0408862f39cccc47c1d9dea1b0fb2d2 

echo "Downloading RGB matrix software..."
curl -L $GITUSER/$REPO/archive/$COMMIT.zip -o $REPO-$COMMIT.zip
unzip -q $REPO-$COMMIT.zip
rm $REPO-$COMMIT.zip
mv $REPO-$COMMIT rpi-rgb-led-matrix
echo "Building RGB matrix software..."
cd rpi-rgb-led-matrix
USER_DEFINES=""

# Build then install for Python 2.7...
USER_DEFINES+=" -DDISABLE_HARDWARE_PULSES"
make clean
make install-python HARDWARE_DESC=adafruit-hat USER_DEFINES="$USER_DEFINES" PYTHON=$(which python2)
# Do over for Python 3...
make clean
make install-python HARDWARE_DESC=adafruit-hat USER_DEFINES="$USER_DEFINES" PYTHON=$(which python3)

# Change ownership to user calling sudo
chown -R $SUDO_USER:$(id -g $SUDO_USER) `pwd`

# PROMPT FOR REBOOT --------------------------------------------------------