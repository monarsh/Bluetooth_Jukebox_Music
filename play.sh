#!/bin/bash

. $PWD/jukebox.conf
MUSIC_DIR=$MUSIC_DIRECTORY

play() {
	SONG=()
	i=1

	for f in $MUSIC_DIR*; do
		SONG[i]="$f"
		i=$(($i+1))
	done

	systemctl --user stop jukebox-playAll.service
	killall ffplay > /dev/null 2>&1

	ffplay -loglevel quiet -loop 0 -nodisp "${SONG[(($1))]}" > /dev/null 2>&1 &
}

playAll() {
	while true; do
		for f in $MUSIC_DIR*; do
			killall ffplay > /dev/null 2>&1
			ffplay -loglevel quiet -autoexit -nodisp "$f" > /dev/null 2>&1
		done
	done
}

if [ "$1" = "-a" ]; then
	playAll
else
	play "$1"
fi
