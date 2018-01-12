import os
from subprocess import call, check_output

try:
	import xbmc, xbmcaddon
	audio_profiles = xbmcaddon.Addon(id="script.audio.profiles")
	addon = xbmcaddon.Addon()
except:
	pass

def current_profile():
	# read 'current profile' from script.audio.profiles
	path = audio_profiles.getAddonInfo('profile')
	with open(os.path.join(path, 'profile'), 'r') as current:
		return current.read()

def get_list():
	out = check_output('echo -e "devices\nexit" | bluetoothctl', shell=True)
	ll = out.split('\n')

	return [ l.replace('Device ', '') for l in ll if l.startswith('Device ') ] 

def switch(mac=None):

	old_profile = current_profile()

	# switch sound profiles
	xbmc.executebuiltin("RunScript(script.audio.profiles,0)", wait=True)
	xbmc.log('detect audio profiles')

	while True:
		c = current_profile()
		if c != old_profile:
			break

		xbmc.sleep(100)

	xbmc.log('audio profile: ' + str(c))

	if mac:
		if str(c) == addon.getSetting('bt_profile'):
			 call('echo -e "connect %s\nexit" | bluetoothctl' % mac, shell=True)

def get_mac(s=None):
	if not s:
		return addon.getSetting('mac')

	return s[:17]

def menu(ll):
	import xbmcgui
	dlg = xbmcgui.Dialog()
	r = dlg.select('Choose a device', ll)
	if r >= 0:
		switch(get_mac(ll[r]))

if __name__ == "__main__":
	ll = get_list()
	if ll:
		menu(ll)
	else:
		mac = get_mac()
		if mac:
			switch(mac)
		else:
			addon.openSettings()

