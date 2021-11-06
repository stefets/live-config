#!/bin/bash
#
# Create a symlink in $target directory for each mp3 file found by find in the $origin directory
#

# Params = config.json
# Origin = datasource + SceneName
# Target = uri
origin=$1
target=$2

if [ ! -d "$origin" ]
then
    exit 3
fi

cd $target

# Crée un symlink dans $target pour chaque mp3
rm -f *.mp3 # Wipe out current mp3 symlinks
for file in $(find -L $origin -type f -iname "*.mp3" | sort)
do
    filename="${file##*/}"
	ln -fs $file $filename
done

# Liste les mp3 dans le fichier playlist pour mpg123
ls *.mp3 > playlist

exit 0
