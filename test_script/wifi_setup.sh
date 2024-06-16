#!/bin/bash


echo "Setting up WiFi Connection through Ethernet Port..."

sudo ip link set eth0 up

sudo dhclient eth0 

echo "Done."