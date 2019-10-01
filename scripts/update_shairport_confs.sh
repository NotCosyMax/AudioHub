#!/bin/bash
cp /usr/share/audiohub/shairport-conf-local-template /usr/share/audiohub/shairport-conf-local
cp /usr/share/audiohub/shairport-conf-remFront-template /usr/share/audiohub/shairport-remFront-local
cp /usr/share/audiohub/shairport-conf-remRear-template /usr/share/audiohub/shairport-remRear-local
sed -i -e s/DEV_NAME/"$1"/g /usr/share/audiohub/shairport-conf-local
sed -i -e s/DEV_NAME/"$2"/g /usr/share/audiohub/shairport-conf-remFront
sed -i -e s/DEV_NAME/"$3"/g /usr/share/audiohub/shairport-conf-remRear

