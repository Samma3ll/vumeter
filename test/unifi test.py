from pyunifi.controller import Controller
c = Controller('192.168.0.117', 'nick', 'NickLQ!709**', '8443', 'V5', 'default', False)
for ap in c.get_aps():
	print('AP named %s with MAC %s' % (ap.get('name'), ap['mac']))
