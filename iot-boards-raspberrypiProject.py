import http.client, urllib
import RPi.GPIO as GPIO
import time

APP_TOKEN="aty4pcgs4pn96zkhm8sdi3d1qvziry"
USER_KEY="ubim8tzcrc9iwt9woin8b7t8abqmk3"

MQ135pin=14
alert=15
stpbtn=18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(MQ135pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(alert, GPIO.OUT)
GPIO.setup(stpbtn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(alert,0)
print("Setup done")
GPIO.output(alert,1)
time.sleep(1)
GPIO.output(alert,0)

while True:
    if GPIO.input(MQ135pin):
        continue
    print("Gas Detected")
    GPIO.output(alert,1)
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.parse.urlencode({
        "token": APP_TOKEN,
        "user": USER_KEY,
        "message": "Harmful gas detected!!!",
      }), { "Content-type": "application/x-www-form-urlencoded" })
    print("Response: ",conn.getresponse())
    while GPIO.input(stpbtn):
        time.sleep(1)
    GPIO.output(alert,0)
    print("Alarm reset")
