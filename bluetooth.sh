#!/bin/bash

. $PWD/jukebox.conf
BL_ID=$(echo $BLUETOOTH_DEVICE | cut -f 1 -d ",")
BL_NAME=$(echo $BLUETOOTH_DEVICE | cut -f 2 -d ",")

connection() {
	if [ "$1" = "-c" ]; then
		bluetoothctl -- default-agent > /dev/null 2>&1
		bluetoothctl -- discoverable on > /dev/null 2>&1
		bluetoothctl -- pairable on > /dev/null 2>&1
		#bluetoothctl -- pair $BL_ID > /dev/null 2>&1
		#bluetoothctl -- trust $BL_ID > /dev/null 2>&1
		bluetoothctl -- connect $BL_ID > /dev/null 2>&1
	elif [ "$1" = "-d" ]; then
		bluetoothctl -- disconnect $BL_ID > /dev/null 2>&1
	fi

	STS=$(bluetoothctl info $BL_ID | grep Connected | awk '{ print $2 }')

	if [ "$STS" = "yes" ]; then
		echo "Connected"
	elif [ "$STS" = "no" ]; then
		echo "Disconnected"
	else
		echo "Disconnected"
	fi
}

check() {
	STS=$(cat /tmp/BluetoothStatus)

	if [ "$STS" = "Connected" ]; then
		$PWD/bluetooth.sh -c
		echo "Checked. Bluetooth ID $BL_ID ($BL_NAME) continue to connected."
	elif [ "$STS" = "Disconnected" ]; then
		echo "Bluetooth ID $BL_ID ($BL_NAME) not found."
	fi
}

if [ "$1" = "-c" ]; then
	connection "-c"
elif [ "$1" = "-d" ]; then
	connection "-d"
elif [ "$1" = "-s" ]; then
	check
fi
