#!/bin/bash

# Raspberry Pi Zero W with Raspbian 11 Bullseye has some issues with the Wifi disconecting after some time.
# This script restart the network manager if it happens to connect again to the Wifi network

# Related post
# https://weworkweplay.com/play/rebooting-the-raspberry-pi-when-it-loses-wireless-connection-wifi/

# Ping gateway
ping -c4 192.168.76.1 > /dev/null
ret=$?

if [ ${ret} != 0 ]
then
	echo "No network connection, rebooting the device"
	sudo /sbin/shutdown -r now
fi
