# #!/bin/bash
echo Install dependencies
apt-get -y update
apt-get -y install python3 python3-pip python3-dev python3-setuptools python3-numpy python3-flask libffi-dev 
apt-get -y install build-essential git xmltoman autoconf automake libtool libdaemon-dev libpopt-dev libconfig-dev libasound2-dev avahi-daemon libavahi-client-dev libssl-dev libsoxr-dev
pip3 install sounddevice

echo Configure alsa
cp confs/.asoundrc /usr/share/alsa/.asoundrc
cp confs/alsa.conf /usr/share/alsa/alsa.conf

# #echo Make and install shairport-sync from remote
# #rm -R tmp
# #mkdir tmp
# #cd tmp
# #git clone https://github.com/mikebrady/alac.git
# #cd alac
# #autoreconf -fi
# #./configure
# #make
# #make install
# #ldconfig
# #cd ..
# #git clone https://github.com/mikebrady/shairport-sync.git
# #cd shairport-sync
# #autoreconf -i -f 
# #./configure --with-alsa --with-avahi --with-ssl=openssl --with-soxr --with-apple-alac --with-systemd
# #make
# #sudo make install
# #cd ..
# #cd ..

echo "Setup application configurations and scripts, copy templates"
mkdir /usr/share/audiohub
mkdir /usr/share/spotcache
cp -r ./confs/shairport-* /usr/share/audiohub/
cp -r scripts/* /usr/share/audiohub/
cp bin/librespot /usr/sbin/librespot
cp services/spotify-connect-template.service /usr/share/audiohub/spotify-connect-template.service
cp confs/shairport-conf-local-template /usr/share/audiohub/shairport-conf-local-template
cp confs/shairport-conf-remFront-template /usr/share/audiohub/shairport-conf-remFront-template 
cp confs/shairport-conf-remRear-template /usr/share/audiohub/shairport-conf-remRear-template 

# Gather some user input to complete service setup
echo "What do you want to call your main audiohub (The name that will show up in AirPlay, e.q: Livingroom):"
read DEV_NAME_MAIN
echo "What do you want to call remote audio sink one (The name that will show up in AirPlay, e.g: Another room):"
read DEV_NAME_REM1
echo "What do you want to call remote audio sink two (The name that will show up in AirPlay, e.g: Another room):"
read DEV_NAME_REM2
echo "What do you want to call the Spotify Connect sink? (The name that will show up in Spotify):"
read DEV_NAME_SPOT
echo "What is your Spotify user name?"
read SPOT_USER
echo "What is your spotify password?"
read SPOT_PASS

cp services/shairport-sync-* /etc/systemd/system
cp services/wire-* /etc/systemd/system

# Copy Spotify service template and update with the given input
/bin/bash /usr/share/audiohub/update_spotify_service.sh $DEV_NAME_SPOT $SPOT_USER $SPOT_PASS

# Setup shairport configurations from tempalates
/bin/bash /usr/share/audiohub/update_shairport_confs.sh $DEV_NAME_MAIN $DEV_NAME_REM1 $DEV_NAME_REM2

echo "Enable and start services"
sudo systemctl enable shairport-sync-local.service
sudo systemctl enable shairport-sync-ppfront.service
sudo systemctl enable shairport-sync-pprear.service
sudo systemctl enable spotify-connect.service
sudo systemctl enable wire-aux.service
sudo systemctl start shairport-sync-local.service
sudo systemctl start shairport-sync-ppfront.service
sudo systemctl start shairport-sync-pprear.service
sudo systemctl start spotify-connect.service
sudo systemctl start wire-aux.service