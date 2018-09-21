import numpy as np
import cv2
import RPi.GPIO as GPIO
import time

# local modules
from video import create_capture
from common import clock, draw_str

if __name__ == '__main__':
	
	print('Setup')
	import sys, getopt
	args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])

	try:
		video_src = video_src[0]
	except:
		video_src = 0

	args = dict(args)
	
	cam = create_capture(video_src, fallback='synth:bg=opencv-3.3.0/samples/data/lena.jpg:noise=0.05')
	
	GPIO.cleanup()
	time.sleep(1)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(12,GPIO.OUT)
	GPIO.setup(15,GPIO.OUT)
	GPIO.setup(13,GPIO.OUT)
	time.sleep(1)
	GPIO.output(15, GPIO.LOW)
	motor = GPIO.PWM(12,500)
	motor.start(0)
	servo = GPIO.PWM(13,500)
	servo.start(50)
	time.sleep(1)
	motor.ChangeDutyCycle(0)
	servo.ChangeDutyCycle(50)
	time.sleep(1)
	print('Setup Fin')
	print('Program Start')

	while True:
		ret, img = cam.read()
		t = clock()
		vis = img.copy()
		dt = clock() - t
		draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
		
		#cv2.imshow('image', vis)

		duty1_str = raw_input("Speed:")
		duty1 = int(duty1_str)

		if duty1 == 101:
			break

		motor.ChangeDutyCycle(duty1)
		dir_str = raw_input("Dir:")
		dir = int(dir_str)

		if dir == 0:
			GPIO.output(15, GPIO.LOW)
		if dir == 1:
			GPIO.output(15, GPIO.HIGH)
		if dir == 2:
			break

		duty2_str = raw_input("Servo:")
		duty2 = int(duty2_str)

		if duty2 == 101:
			break

		servo.ChangeDutyCycle(duty2)
		#servo.ChangeDutyCycle(50)
		
		if cv2.waitKey(5) == 27:
			break
		
	print('End Program')
	cv2.destroyAllWindows()
	GPIO.cleanup()
	print('End')
