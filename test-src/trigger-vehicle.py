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
	# tr.add(uSherpa.PIN_2_4, uSherpa.EDGE_LOWHIGH)

	vehicle  = AdvancedVehicle(mctl, tr)

	c = 20

	print "fw"
	vehicle.fw(c)

	print "bw"
	vehicle.bw(c)

	print "le"
	vehicle.le(c)

	print "ri"
	vehicle.ri(c)

	# reset MCU 
  	print "RESET: "  
	us.reset()
	print "-> OK"

except Exception as e:
	print traceback.format_exc()

finally:
	if not ps == None:
		ps.stop()	
