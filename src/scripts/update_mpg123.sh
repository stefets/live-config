#!/bin/bash
#
# Author : Grand Design Studio (Stephane Gagnon)
# Script to update mpg123 to the lastest version an a system
#

# Get the lastest release from the NEWS file in the SVN trunc repository
news="https://www.mpg123.de/cgi-bin/scm/mpg123/trunk/NEWS"
wget -nv $news
if [ -f "NEWS" ]; then
	latest=$(head -1 NEWS)
	current=$(mpg123 --version | cut -d' ' -f2)
	rm -f NEWS
    if [ "$latest" == "$current" ]; then
        echo "MPG123 version is already up to date on this system: $latest"
	    exit 0
    fi
fi

version=$latest
file="mpg123-$version.tar.bz2"
src=https://sourceforge.net/projects/mpg123/files/mpg123/$version/$file
wget -nv $src
if [ -f "$file" ]; then
    tmp=$(mktemp -d)
    mv $file $tmp
    cd $tmp
    tar -xf $file
    cd $tmp/mpg123-$version
    sudo ./configure --with-cpu=generic_fpu
    sudo make
    sudo make install
    sudo rm -rf $tmp
else
    echo "Update failed, $file not found."
    exit -1
fi

echo "Done"
mpg123 --version

exit 0
