'''
Test Triggers
'''

import traceback
import time

from usherpa.api import *
from usherpa.serialcomm import *

from device.dcmctl import MCtlChannel, DualChannelMCtl
from device.trigger import Trigger 
from robot.vehicle import AdvancedVehicle

# Searial Packet stream instance
ps = None
us = None

try:

	print "uSherpaExternal Interrupt"

	ps = SerialPacketStream("/dev/ttyS0")
	# ps = SerialPacketStream("/dev/ttyUSB0")
	ps.start()

	us = uSherpa(ps)

	# build dual-channel motor controller
	mch1 = MCtlChannel(us, uSherpa.PIN_1_4, uSherpa.PIN_1_5)
	mch2 = MCtlChannel(us, uSherpa.PIN_1_6, uSherpa.PIN_1_7)
	mctl = DualChannelMCtl(mch1, mch2)

	# define trigger for wheel encoders
	tr = Trigger(us)
	tr.add(uSherpa.PIN_2_3, uSherpa.EDGE_HIGHLOW)

	vehicle  = AdvancedVehicle(mctl, tr)

	print "fw 20"
	vehicle.fw(20)

	print "bw 20"
	vehicle.bw(20)

	print "le 20"
	vehicle.le(20)

	print "ri 20"
	vehicle.ri(20)

	# reset MCU 
  	print "RESET: "  
	us.reset()
	print "-> OK"

except Exception as e:
	print traceback.format_exc()

finally:
	if not ps == None:
		ps.stop()	
