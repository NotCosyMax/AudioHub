import sys
import subprocess
import select
 
args = ['journalctl', '--lines', '0', '--follow', '_SYSTEMD_UNIT=spotify-connect.service']
f = subprocess.Popen(args, stdout=subprocess.PIPE)
p = select.poll()
p.register(f.stdout)
 
while True:
	if p.poll(100):
		line = f.stdout.readline()
		if b'ERROR' in line:
			print("Error occured")
			subprocess.call(["/bin/systemctl", "restart", "spotify-connect.service"])
		elif b'INFO' in line:
			print("Just info")
		print(line.strip())
