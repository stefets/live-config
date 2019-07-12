#!/bin/bash

# Author : Stephane Gagnon
# This script install mididings and most of its dependecies according my setup
# It install other tools for my setup
# Tested on an ubuntu desktop 18.04
#
# TODO if I need in the future ::: JACK lib, DBUS, Tkinter, pyinotify and libsmf
#

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

user=$(whoami)
if [ "$user" != "root" ]
then
	echo "Please, run with sudo -H"
	exit -1
fi


mididings=/tmp/mididings
pyliblo=/tmp/pyliblo

apt update

# Install dialog for the menu
apt --yes install dialog

# Install mpg123 for mp3 player
apt --yes install mpg123

# Install ALSA lib and add $callername to audio group for accessing ALSA hardware
apt --yes install libasound2-dev
callername=$(who am i |cut -d' ' -f1)
usermod -G audio -a $callername

# Install Boost
apt --yes install libboost-all-dev

# Install Glib 2.0
apt --yes install glib2.0

# Install pip for python 2/3
apt --yes install python-pip
apt --yes install python3-pip

# Install decorator
pip install decorator

# Install Cython
pip install Cython

# Install liblo
apt --yes install liblo-dev

# Install pyliblo
cd /tmp
rm -rf $pyliblo
git clone https://github.com/dsacre/pyliblo.git
cd $pyliblo
./setup.py build
./setup.py install

# Install mididings for ALSA
cd /tmp
rm -rf $mididings
git clone https://github.com/dsacre/mididings.git
cd $mididings
# I have to remove the line compiler.compiler_so.append('-fvisibility=hidden') with sed
sed -i '/fvisibility=hidden/d' /tmp/mididings/setup.py
./setup.py build --disable-jack-midi
./setup.py install --disable-jack-midi
