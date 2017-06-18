from modules import app, cbpi
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
blynk_actor_state_offset = 70
blynk_actor_power_offset = 90

def blynkAuth():
	global blynk	
	if blynk_auth is None or not blynk_auth:
		cbpi.notify("Blynk Warning", "No Blynk token specified", type="danger", timeout=None)
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
		cbpi.add_config_parameter("blynk_auth_token", "", "text", "Blynk Authentication Token")

@cbpi.initalizer(order=8045)
def init(cbpi):
	cbpi.app.logger.info("INITIALIZE BLYNK PLUGIN")
	blynkDB()
	blynkAuth()

@cbpi.backgroundtask(key="blynk_send_values", interval=3)
def blynk_send_values():
	if blynk is not None:
		# Update Blynk last updated field
		blynk.virtual_write(blynk_last_updated, time.ctime())

		# Update Blynk current step field
		step = cbpi.cache.get("active_step")
		if step is not None:
			step_text = step.name
		else:
			step_text = "---"
		blynk.virtual_write(blynk_current_step, step_text)

		# Update Blynk sensor readings
		for count, (key, value) in enumerate(cbpi.cache["sensors"].iteritems(), 1):
			# Check if data is already formatted (string) or not (float)
			if type(value.instance.last_value) is str:
				formatted_reading = value.instance.last_value
			if type(value.instance.last_value) is float:
				formatted_reading = '{0:.2f}'.format(value.instance.last_value)
			blynk.virtual_write(count + blynk_sensor_offset, formatted_reading)

		# Update Blynk kettle setpoints
		for count, (key, value) in enumerate(cbpi.cache["kettle"].iteritems(), 1):
			blynk.virtual_write(count + blynk_kettle_offset, '{0:.2f}'.format(value.target_temp))

		# Update Blynk fermenter setpoints
		for count, (key, value) in enumerate(cbpi.cache["fermenter"].iteritems(), 1):
			blynk.virtual_write(count + blynk_fermenter_offset, '{0:.2f}'.format(value.target_temp))

		# Update Blynk actor states and power
		for count, (key, value) in enumerate(cbpi.cache["actors"].iteritems(), 1):
			blynk.virtual_write(count + blynk_actor_state_offset, value.state)
			blynk.virtual_write(count + blynk_actor_power_offset, value.power)
