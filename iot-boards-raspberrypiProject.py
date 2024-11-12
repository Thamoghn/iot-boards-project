import time
import RPi.GPIO as GPIO
import httplib, urllib

# setup GPIO using Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)

# define the GPIO port you will use for the motion detector
PIR_SENSOR = 19 

# define the GPIO port you will use for the status LED
# the LED will light up when motion is detected by the PIR sensor
LED = 13

# number of seconds to delay between alarms
DELAY = 10

# set to pull-up (normally closed position for a PIR sensor dry contact)
GPIO.setup(PIR_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# set the LED GPIO to output
GPIO.setup(LED, GPIO.OUT)

# Pushover API setup
PUSH_TOKEN = "aty4pcgs4pn96zkhm8sdi3d1qvziry" # API Token/Key
PUSH_USER = "ubim8tzcrc9iwt9woin8b7t8abqmk3" # Your User Key
PUSH_MSG = "Motion detected!" # Push Message you want sent

# This function sends the push message using Pushover.
# Pass in the message that you want sent
def sendPush( msg ):
	conn = httplib.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
		urllib.urlencode({
			"token": PUSH_TOKEN,
			"user": PUSH_USER,
			"message": msg,
		}), { "Content-type": "application/x-www-form-urlencoded" })

	conn.getresponse()
	return

try:
	# setup an indefinite loop that looks for the PIR sensor to be triggered
	while True:
		# motion is detected
		GPIO.wait_for_edge(PIR_SENSOR, GPIO.RISING)
		# light LED
		GPIO.output(LED, True)
		# print and push message
		print(PUSH_MSG)
		sendPush(PUSH_MSG)

		# do you want a time delay in between alarms?
		time.sleep(DELAY)
		# after delay, turn LED off
		GPIO.output(LED, False)

except KeyboardInterrupt:
	# cleanup GPIOs on keyboard exit
	GPIO.cleanup()

# cleanup GPIOs when program exits
GPIO.cleanup()