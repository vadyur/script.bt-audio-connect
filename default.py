import os
from subprocess import call, check_output

try:
	import xbmc, xbmcaddon
	audio_profiles = xbmcaddon.Addon(id="script.audio.profiles")
	addon = xbmcaddon.Addon()
except:
	pass

def getSetting(id, default=''):
	result = addon.getSetting(id)
	if result != '':
		return result
	else:
		return default

def choice():
	# read 'current profile' from script.audio.profiles
	path = audio_profiles.getAddonInfo('profile')
	current = open(os.path.join(path, 'profile', 'r'))
	result = current.read()
	current.close()
	return result

def get_list():
	out = check_output('echo -e "devices\nexit" | bluetoothctl', shell=True)
	ll = out.split('\n')

	return [ l.replace('Device ', '') for l in ll if l.startswith('Device ') ] 

def switch(mac=None):

	old_c = choice()

	# switch sound profiles
	xbmc.executebuiltin("RunScript(script.audio.profiles,0)")
	xbmc.log('detect audio profiles')

	while True:
		c = choice()
		if c != old_c:
			break

		xbmc.sleep(100)

	xbmc.log('audio profile: ' + str(c))

	if mac:
		if str(c) == getSetting('bt_profile'):
			 call('echo -e "connect %s\nexit" | bluetoothctl' % mac, shell=True)
	else:
		addon.openSettings()

def get_mac(s):
	return s[:17]

def menu():
	ll = get_list()
	import xbmcgui
	dlg = xbmcgui.Dialog()
	r = dlg.select('Choose a device', ll)
	if r >= 0:
		switch(get_mac(ll[r]))

if __name__ == "__main__":
	menu()