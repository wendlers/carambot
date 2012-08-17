'''
Test Triggers
'''

import traceback
import time
import threading

from usherpa.api 		import *
from usherpa.serialcomm import *

from device.md132a		import MCtlChannel
from device.dcmctl 		import DualChannelMCtl
from device.trigger 	import Trigger 
from device.srf05 		import RangeFinder 
from device.vehicle 	import AdvancedVehicle

# Searial Packet stream instance
ps = None

try:

	print "uSherpa and Carambot rocking the wheels!"

	# ps = SerialPacketStream("/dev/ttyS0")
	ps = SerialPacketStream("/dev/ttyUSB0")
	ps.start()

	us = uSherpa(ps)
	us.retrys = 3

	# build dual-channel motor controller
	mch1 = MCtlChannel(us, uSherpa.PIN_1_4, uSherpa.PIN_1_5)
	mch2 = MCtlChannel(us, uSherpa.PIN_1_6, uSherpa.PIN_1_7)
	mctl = DualChannelMCtl(mch1, mch2)

	# define trigger for wheel encoders
	tr = Trigger(us)
	tr.add(uSherpa.PIN_2_3, uSherpa.EDGE_LOWHIGH)
	tr.add(uSherpa.PIN_2_4, uSherpa.EDGE_LOWHIGH)

	#define range finder
	rf  = RangeFinder(us, uSherpa.PIN_2_0)
	
	# define vehicle
	vehicle  = AdvancedVehicle(mctl, tr, rf)

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

finally:
	if not ps == None:
		ps.stop()	

print "DONE"
