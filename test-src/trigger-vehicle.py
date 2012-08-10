'''
Test Triggers
'''

import traceback
import time

from usherpa.api import *
from usherpa.serialcomm import *

from device.dcmctl import MCtlChannel, DualChannelMCtl
from robot.vehicle import AdvancedVehicle

# Searial Packet stream instance
ps = None
us = None

try:

	print "uSherpaExternal Interrupt"

	ps = SerialPacketStream("/dev/ttyUSB0")
	ps.start()

	us = uSherpa(ps)

	us.pinMode(uSherpa.PIN_2_3, uSherpa.INPUT)

	mch1 = MCtlChannel(us, uSherpa.PIN_1_4, uSherpa.PIN_1_5)
	mch2 = MCtlChannel(us, uSherpa.PIN_1_6, uSherpa.PIN_1_7)
	mctl = DualChannelMCtl(mch1, mch2)
	vehicle  = AdvancedVehicle(mctl, uSherpa.PIN_2_3, uSherpa.EDGE_HIGHLOW)

	print "fw 20"
	vehicle.fw(20)

	print "bw 20"
	vehicle.bw(20)

	print "li 20"
	vehicle.li(20)

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
