#!/bin/bash

echo Install dependencies
apt-get install python3 pythno3-pip python3-dev python3-setuptools python3-numpy python3-flask libffi-dev 
apt-get install build-essential git xmltoman autoconf automake libtool libdaemon-dev libpopt-dev libconfig-dev libasound2-dev avahi-daemon libavahi-client-dev libssl-dev libsoxr-dev
pip3 install sounddevice

echo Setup alsa and loopback devices
echo 'snd-aloop' >> /etc/modules
cp confs/sound.conf /etc/modprob.d/sound.conf
cp confs/.asoundrc /usr/share/alsa/.asoundrc
cp confs/alsa.conf /usr/share/alsa/alsa.conf

echo Make and install shairport-sync from remote
rm -R tmp
mkdir tmp
cd tmp
git clone https://github.com/mikebrady/alac.git
cd alac
autoreconf -fi
./configure
make
make install
ldconfig
cd ..
git clone https://github.com/mikebrady/shairport-sync.git
cd shairport-sync
autoreconf -i -f 
./configure --with-alsa --with-avahi --with-ssl=openssl --with-soxr --with-apple-alac --with-systemd
make
sudo make install
cd ..
cd ..

echo Setup application configurations and scripts
mkdir /usr/share/audiohub
cp confs/shareport-* /usr/share/audiohub/
cp scripts/sound_splitter.py /usr/share/audiohub/sound_splitter.py
cp bin/librespot /bin/librespot

echo Setup services
cp services/* /etc/systemd/systemd
