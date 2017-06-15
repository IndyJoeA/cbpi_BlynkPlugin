from modules import app, cbpi
from modules.core.db import get_db
from modules.config import ConfigView
from thread import start_new_thread
import BlynkLib
import logging
import time

# Global Blynk objects
blynk = None
blynk_auth = None

# Virtual Pin configuration
blynk_last_updated = 0
blynk_current_step = 1
blynk_sensor_offset = 10
blynk_kettle_offset = 30
blynk_fermenter_offset = 50
blynk_actor_offset = 70

def blynkAuth():
	global blynk	
	if blynk_auth is None:
		cbpi.notify("Blynk Error", "No Blynk token specified", type="danger", timeout=None)
	else:				
		blynk = BlynkLib.Blynk(blynk_auth)
		start_new_thread(blynkConnection, ())

def blynkConnection():
	blynk.run()

def blynkDB():
	global blynk_auth	
	blynk_auth = cbpi.get_config_parameter("blynk_auth_token", None)
	if blynk_auth is None:
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

@cbpi.backgroundtask(key="blynk_send_reading", interval=3)
def blynk_send_reading():
	if blynk is not None:
		blynk.virtual_write(blynk_last_updated, time.ctime())

		step = cbpi.cache.get("active_step")
		if step is not None:
			step_text = step.name
		else:
			step_text = "---"
		blynk.virtual_write(blynk_current_step, step_text)

		for idx, value in cbpi.cache["sensors"].iteritems():			
			blynk.virtual_write(value.id + blynk_sensor_offset, '{0:.2f}'.format(cbpi.get_sensor_value(value.id)))

		for idx, value in cbpi.cache["kettle"].iteritems():
			blynk.virtual_write(value.id + blynk_kettle_offset, '{0:.2f}'.format(value.target_temp))

		for idx, value in cbpi.cache["fermenter"].iteritems():
			blynk.virtual_write(value.id + blynk_fermenter_offset, '{0:.2f}'.format(value.target_temp))

		for idx, value in cbpi.cache["actors"].iteritems():
			blynk.virtual_write(value.id + blynk_actor_offset, value.state)
