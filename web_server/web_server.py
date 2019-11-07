from flask import Flask, request, render_template
import logging
import sys
import configparser
from subprocess import call
import time

logging.basicConfig()
log = logging.getLogger('AudioHub')
log.setLevel(logging.INFO)  # DEBUG

app = Flask(__name__)

class AudioHubWebServer():
    def __init__(self, ip, conf_file):
        self.host_ip = ip
        self.config_file = conf_file
        self.config = configparser.ConfigParser()

        self.app = app
        self.route_wrapped = self.app.route('/', methods=['GET', 'POST'])(self.render)

    def get_device_config(self, device):
        dict1 = {}
        options = self.config.options(device)
        for option in options:
            try:
                dict1[option] = self.config.get(device, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def start(self):
        self.app.run(debug=True, host=self.host_ip, port=8000)

    def render(self):
        # Read in config file
        self.config.read(self.config_file)
        device_name_1 = self.get_device_config("DeviceOne")["name"]
        device_name_2 = self.get_device_config("DeviceTwo")["name"]
        device_name_3 = self.get_device_config("DeviceThree")["name"]
        spot_val_1 = self.get_device_config("DeviceOne")["spotify_volume"]
        air_val_1 = self.get_device_config("DeviceOne")["shairport_volume"]
        aux_val_1 = self.get_device_config("DeviceOne")["aux_volume"]
        print(spot_val_1)
        print(air_val_1)
        print(aux_val_1)
        spot_val_2 = self.get_device_config("DeviceTwo")["spotify_volume"]
        air_val_2 = self.get_device_config("DeviceTwo")["shairport_volume"]
        aux_val_2 = self.get_device_config("DeviceTwo")["aux_volume"]
        spot_val_3 = self.get_device_config("DeviceThree")["spotify_volume"]
        air_val_3 = self.get_device_config("DeviceThree")["shairport_volume"]
        aux_val_3 = self.get_device_config("DeviceThree")["aux_volume"]

        if request.method == 'POST':
            expand_1 = True if request.form.get('_exp_1') == "true" else False
            expand_2 = True if request.form.get('_exp_2') == "true" else False
            expand_3 = True if request.form.get('_exp_3') == "true" else False
            method = request.form.get('_method')
            # Selected profile changed
            if method == "save":
                # Get values
                spot_val_1 = str(request.form.get('_spot_1'))
                air_val_1 = str(request.form.get('_air_1'))
                aux_val_1 = str(request.form.get('_aux_1'))
                spot_val_2 = str(request.form.get('_spot_2'))
                air_val_2 = str(request.form.get('_air_2'))
                aux_val_2 = str(request.form.get('_aux_2'))
                spot_val_3 = str(request.form.get('_spot_3'))
                air_val_3 = str(request.form.get('_air_3'))
                aux_val_3 = str(request.form.get('_aux_3'))
                # Set mixers
                call(["/usr/bin/amixer", "-q", "set", "softvol_locspot", spot_val_1])
                call(["/usr/bin/amixer", "-q", "set", "softvol_locshair", air_val_1])
                call(["/usr/bin/amixer", "-q", "set", "softvol_locaux", aux_val_1])
                call(["/usr/bin/amixer", "-q", "set", "softvol_rem1spot", spot_val_2])
                call(["/usr/bin/amixer", "-q", "set", "softvol_rem1shair", air_val_2])
                call(["/usr/bin/amixer", "-q", "set", "softvol_rem1aux", aux_val_2])
                call(["/usr/bin/amixer", "-q", "set", "softvol_rem2spot", spot_val_3])
                call(["/usr/bin/amixer", "-q", "set", "softvol_rem2shair", air_val_3])
                call(["/usr/bin/amixer", "-q", "set", "softvol_rem2aux", aux_val_3])
                # Store in config file
                self.config.set('DeviceOne', 'spotify_volume', spot_val_1)
                self.config.set('DeviceOne', 'shairport_volume', air_val_1)
                self.config.set('DeviceOne', 'aux_volume', aux_val_1)
                self.config.set('DeviceTwo', 'spotify_volume', spot_val_2)
                self.config.set('DeviceTwo', 'shairport_volume', air_val_2)
                self.config.set('DeviceTwo', 'aux_volume', aux_val_2)
                self.config.set('DeviceThree', 'spotify_volume', spot_val_3)
                self.config.set('DeviceThree', 'shairport_volume', air_val_3)
                self.config.set('DeviceThree', 'aux_volume', aux_val_3)
                conffile = open(self.config_file,'w')
                self.config.write(conffile)
                conffile.close()
            elif method == "restart_spotify":
                call(["/bin/systemctl", "restart", "spotify-connect.service"])
                pass
            elif method == "restart_aux":
                call(["/bin/systemctl", "restart", "wire-aux.service"])
                pass
            elif method == "reboot":
                call(["/sbin/reboot"])
                pass
            elif method == "shutdown":
                call([/sbin/halt])
                pass
        else:
            expand_1 = False
            expand_2 = False
            expand_3 = False

        # Render page
        base_template = render_template("index.html", **locals())

        return base_template
