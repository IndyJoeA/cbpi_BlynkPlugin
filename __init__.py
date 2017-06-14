from modules import app, cbpi
from modules.core.db import get_db
from modules.config import ConfigView
from thread import start_new_thread
import BlynkLib
import logging
import time

# BLYNK_AUTH = 'd9db144199944107860c3399ac30b2bd'

# Global Blynk object
# blynk = BlynkLib.Blynk(BLYNK_AUTH)
blynk = None

def blynkAuth():
	blynk_auth = cbpi.get_config_parameter("blynk_auth_token", None)
	if blynk_auth is None:
		cbpi.notify("Blynk Error", "No Blynk token specified", type="danger", timeout=None)
	else
		blynk = BlynkLib.Blynk(blynk_auth)
		start_new_thread(blynkConnection, ())

def blynkConnection():
	blynk.run()

def blynkDB():
	print "INIT BLYNK DB"
	with app.app_context():
		db = get_db()

		with app.open_resource('./plugins/BlynkPlugin/schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())

		db.commit()
	ConfigView.init_cache()

@cbpi.initalizer(order=8045)
def init(cbpi):
	cbpi.app.logger.info("INITIALIZE BLYNK PLUGIN")
	blynkDB()
	blynkAuth()
	blynkConnection()

@cbpi.backgroundtask(key="blynk_send_reading", interval=1)
def blynk_send_reading():
	if blynk is not None:
		for idx, value in cbpi.cache["sensors"].iteritems():
			v = cbpi.get_sensor_value(value.id)
		
			# notify_text = 'id: %s val: %s' % (value.id, v)
			# cbpi.notify("Sensor", notify_text, timeout=3)
			# blynk.virtual_write(value.id, v)
