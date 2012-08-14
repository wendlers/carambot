'''
Test Triggers
'''

import traceback
import time

from usherpa.api import *
from usherpa.serialcomm import *

from device.dcmctl import MCtlChannel, DualChannelMCtl
from device.trigger import Trigger
from robot.vehicle import Vehicle

# Searial Packet stream instance
ps = None
us = None

exti = 2

def exti_1(msg, pin):
	''' Callback handler for external interrupts received from uSherpa ''' 
 
	print "Received external interrupt 1"

	exti = exti - 1

def exti_2(msg, pin):
	''' Callback handler for external interrupts received from uSherpa ''' 
 
	print "Received external interrupt 1"

	exti = exti - 1

try:

	print "uSherpaExternal Interrupt"

	# ps = SerialPacketStream("/dev/ttyUSB0")
	ps = SerialPacketStream("/dev/ttyS0")
	ps.start()

	us = uSherpa(ps)
	us.retrys = 3

	us.pinMode(uSherpa.PIN_2_3, uSherpa.INPUT)
	us.pinMode(uSherpa.PIN_2_4, uSherpa.INPUT)

	trigger = Trigger(us)
	trigger.add(uSherpa.PIN_2_3, uSherpa.EDGE_HIGHLOW)
	trigger.add(uSherpa.PIN_2_4, uSherpa.EDGE_HIGHLOW)

	mch1 = MCtlChannel(us, uSherpa.PIN_1_4, uSherpa.PIN_1_5)
	mch2 = MCtlChannel(us, uSherpa.PIN_1_6, uSherpa.PIN_1_7)
	mctl = DualChannelMCtl(mch1, mch2)
	vehicle  = Vehicle(mctl)

	trigger.activate(uSherpa.PIN_2_3, exti_1, 10)
	trigger.activate(uSherpa.PIN_2_4, exti_2, 10)

	vehicle.fw()
	
	while not exti == 0:
		time.sleep(0.1)

	vehicle.br()

	print "All triggers received"

	# reset MCU 
  	print "RESET: "  
	us.reset()
	print "-> OK"

except Exception as e:
	print traceback.format_exc()

finally:
	if not ps == None:
		ps.stop()	
