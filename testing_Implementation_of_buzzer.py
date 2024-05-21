import RPi.GPIO as GPIO
import time

BuzzerPin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BuzzerPin, GPIO.OUT) 
GPIO.setwarnings(False)

global Buzz 
Buzz = GPIO.PWM(BuzzerPin, 440) 
Buzz.start(10) 

#G4=392
song = [392]
beat = [8]

while True:
	for i in range(1, len(song)): 
		Buzz.ChangeFrequency(song[i]) 
		time.sleep(beat[i]*0.13) 