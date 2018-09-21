from __future__ import print_function

import numpy as np
import cv2
import RPi.GPIO as GPIO

from video import create_capture
from common import clock, draw_str

if __name__ == '__main__':
	import sys, getopt

	args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
	try:
		video_src = video_src[0]
	except:
		video_src = 0;
	args = dict(args)

	cam = create_capture(video_src)

	while True:
		ret, img = cam.read()

		t = clock()
		vis = img.copy()
	
		dt = clock() - t
		draw_str(vis, (20,20), 'time: %.1f ms' % (dt*1000))
	
		cv2.imshow('image', vis)

		if cv2.waitKey(5) == 27:
			break

	cv2.destoryAllWindows()
