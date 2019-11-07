#!/bin/bash
cp /usr/share/audiohub/spotify-connect-template.service /etc/systemd/system/spotify-connect.service
sed -i -e s/DEV_NAME/"$1"/g /etc/systemd/system/spotify-connect.service
#sed -i -e s/SPOT_USER/"$2"/g /etc/systemd/system/spotify-connect.service
#sed -i -e s/SPOT_PASS/"$3"/g /etc/systemd/system/spotify-connect.service
