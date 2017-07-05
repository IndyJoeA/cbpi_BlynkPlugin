from modules import app, cbpi
import threading
import BlynkLib
import logging
import time

# Global Blynk objects
blynk = None
blynk_auth = None
blynk_thread = None

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
	global blynk_thread	
	if blynk_auth is None or not blynk_auth:
		cbpi.notify("Blynk Error", "No Blynk Authentication Token specified", type="danger", timeout=10000)
	else:				
		blynk = BlynkLib.Blynk(blynk_auth)
		blynk_thread = threading.Thread(name='blynkConnection', target=blynkConnection)
		blynk_thread.setDaemon(True)
		time.sleep(2)
		blynk_thread.start()

def blynkConnection():	
	blynk.run()
	blynk.log("Blynk thread has ended")

def blynkDB():
	global blynk_auth	
	blynk_auth = cbpi.get_config_parameter("blynk_auth_token", None)
	if blynk_auth is None:
		print "INIT BLYNK DB"
		try:
			cbpi.add_config_parameter("blynk_auth_token", "", "text", "Blynk Authentication Token")
		except:
			cbpi.notify("Blynk Error", "Unable to update database. Update CraftBeerPi and reboot.", type="danger", timeout=10000)

@cbpi.initalizer(order=8045)
def init(cbpi):
	cbpi.app.logger.info("INITIALIZE BLYNK PLUGIN")

@cbpi.backgroundtask(key="blynk_check_auth", interval=60)
def blynk_check_auth(api):
	if blynk is not None:
		if blynk_thread.isAlive() == False:
			blynk.log("Blynk thread is trying to restart")
			blynkAuth()
		pass
	else:
		blynkDB()
		blynkAuth()

@cbpi.backgroundtask(key="blynk_send_values", interval=2)
def blynk_send_values(api):
	if blynk is not None:
		# Update Blynk last updated field
		blynk.virtual_write(blynk_last_updated, time.strftime("%H:%M:%S %m/%d/%y", time.localtime()))

		# Update Blynk current step field
		step = cbpi.cache.get("active_step")
		step_text = "---"
		if step is not None:
			if step.name is not None and step.name:
				step_text = step.name
			if step.timer_end is not None:
				step_text += " [%s]" % (time.strftime("%H:%M:%S", time.gmtime(step.timer_end - time.time())))

		blynk.virtual_write(blynk_current_step, step_text)

		# Update Blynk sensor readings
		for count, (key, value) in enumerate(cbpi.cache["sensors"].iteritems(), 1):
			# Check data type of sensor reading, format if float
			if type(value.instance.last_value) is float:
				formatted_reading = '{0:.2f}'.format(value.instance.last_value)
			else:
				formatted_reading = value.instance.last_value
			blynk.virtual_write(count + blynk_sensor_offset, formatted_reading)

		# Update Blynk kettle setpoints
		for count, (key, value) in enumerate(cbpi.cache["kettle"].iteritems(), 1):
			if value.target_temp is not None:
				blynk.virtual_write(count + blynk_kettle_offset, '{0:.2f}'.format(value.target_temp))

		# Update Blynk fermenter setpoints
		for count, (key, value) in enumerate(cbpi.cache["fermenter"].iteritems(), 1):
			if value.target_temp is not None:
				blynk.virtual_write(count + blynk_fermenter_offset, '{0:.2f}'.format(value.target_temp))

		# Update Blynk actor states and power
		for count, (key, value) in enumerate(cbpi.cache["actors"].iteritems(), 1):
			blynk.virtual_write(count + blynk_actor_state_offset, value.state)
			blynk.virtual_write(count + blynk_actor_power_offset, value.power)
