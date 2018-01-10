import xbmc, xbmcaddon
import os
from subprocess import call

audio_profiles = xbmcaddon.Addon(id="script.audio.profiles")
addon = xbmcaddon.Addon()

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

mac = getSetting('mac')
if mac:
	if str(c) == getSetting('bt_profile'):
		 call('echo -e "connect %s\nexit" | bluetoothctl' % mac, shell=True)
else:
	addon.openSettings()