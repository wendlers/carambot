'''
Test Triggers
'''

import traceback
import time
import threading

from rob.carambot import Robot 

try:

	print "uSherpa and Carambot rocking the wheels!"

	rob 	= Robot("/dev/ttyS0")
	rf  	= rob.panrf.rf 
	vehicle = rob.vehicle 

	# stupid navigation loop
	try:
		while True:

			# move foreward until obstacle was detected
			while vehicle.fw(100):
				pass
	
			# go left util range is bigger than saftey distance	
			t = 10

			while t > 0:
				vehicle.le(10)

				if rf.currentRange() > vehicle.minSafetyRange:
					break

				t = t - 1

			if t == 0:
				print "I am STUCK! Giving up"
				break

	except KeyboardInterrupt:
		vehicle.br()

except Exception as e:
	print traceback.format_exc()

print "DONE"
