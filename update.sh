# #!/bin/bash
echo "Stop services in case they are active"
sudo systemctl stop shairport-sync-local.service
sudo systemctl stop shairport-sync-ppfront.service
sudo systemctl stop shairport-sync-pprear.service
sudo systemctl stop spotify-connect.service
sudo systemctl stop wire-aux.service
sudo systemctl stop spotify-watchdog.service
sudo systemctl stop web-server.service

echo "Update librespot binary"
cp bin/librespot /usr/sbin/librespot
#Setup permissions for librespot
chmod 755 /usr/sbin/librespot

echo "Enable and start services again"
sudo systemctl enable shairport-sync-local.service
sudo systemctl enable shairport-sync-ppfront.service
sudo systemctl enable shairport-sync-pprear.service
sudo systemctl enable spotify-connect.service
sudo systemctl enable wire-aux.service
sudo systemctl enable spotify-watchdog.service
sudo systemctl enable web-server.service
sudo systemctl start shairport-sync-local.service
sudo systemctl start shairport-sync-ppfront.service
sudo systemctl start shairport-sync-pprear.service
sudo systemctl start spotify-connect.service
sudo systemctl start wire-aux.service
sudo systemctl start spotify-watchdog.service
sudo systemctl start web-server.service
