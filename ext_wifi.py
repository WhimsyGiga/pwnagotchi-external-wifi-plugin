import pwnagotchi.plugins as plugins
import pwnagotchi
import logging
import subprocess

class ext_wifi(plugins.Plugin):
    __author__ = 'pragmatic@tuta.com'
    __version__ = '1.1.0'
    __license__ = 'GPL3'
    __description__ = 'Activates external wifi adapter and updates pwngrid-peer service'

    def __init__(self):
        self.ready = 0
        self.status = ''
        self.network = ''

    def on_loaded(self):
        for opt in ['mode', 'interface']:
            if opt not in self.options or (opt in self.options and self.options[opt] is None):
                logging.error(f"Set WiFi adapter mode configuration for internal or external.")
                return

        _log("plugin loaded")
        self.ready = 1

        mode = self.options['mode']
        interface = self.options['interface']

        if mode == "external":
            _patch_interface(interface)
            _patch_pwngrid_service(interface)
            _reload_systemd()
            _log("External adapter activated")
        else:
            _patch_interface('mon0')
            _patch_pwngrid_service('mon0')
            _reload_systemd()
            _log("Internal adapter activated")

def _patch_interface(interface):
    _sed_replace('mon0', interface, '/usr/bin/bettercap-launcher')
    _sed_replace('mon0', interface, '/usr/local/share/bettercap/caplets/pwnagotchi-auto.cap')
    _sed_replace('mon0', interface, '/usr/local/share/bettercap/caplets/pwnagotchi-manual.cap')
    _sed_replace('mon0', interface, '/etc/pwnagotchi/config.toml')
    _sed_replace('mon0', interface, '/usr/bin/pwnlib')

def _patch_pwngrid_service(interface):
    _sed_replace('mon0', interface, '/etc/systemd/system/pwngrid-peer.service')

def _reload_systemd():
    subprocess.run('systemctl daemon-reload', shell=True)

def _sed_replace(old, new, file_path):
    cmd = f"sed -i 's/{old}/{new}/g' {file_path}"
    subprocess.run(cmd, shell=True)

def _log(message):
    logging.info('[ext_wifi] %s' % message)
