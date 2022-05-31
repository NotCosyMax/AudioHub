#!/bin/bash
systemctl stop spotify-connect.service
systemctl stop spotify-watchdog.service

echo "Spotify Services Stopped"

rm /usr/share/spotcache/*

echo "Spotify Cache Cleared"

systemctl start spotify-connect.service
systemctl start spotify-watchdog.service

echo "Spotify Services Started"