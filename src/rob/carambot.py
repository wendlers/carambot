##
# This file is part of the carambot-usherpa project.
#
# Copyright (C) 2012 Stefan Wendler <sw@kaltpost.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

'''
This file is part of the carambot-usherpa project.
'''

import logging

from usherpa.api import *                    
from usherpa.serialcomm import *

from device.md132a 	import MCtlChannel
from device.dcmctl 	import DualChannelMCtl
from device.servo  	import Servo 
from device.srf05  	import RangeFinder 
from device.vehicle import Vehicle, AdvancedVehicle
from device.panrf 	import PanRf 
from device.trigger	import Trigger 

class Robot:
	'''
	Represents all the stuff a robot needs
	'''

	us  = None
	ps	= None

	vehicle = None
	panrf   = None

	advanced = None

	def __init__(self, sherpaPort, advanced = False): 

		logging.info("Constructing carambot robot instance (advanced=%s)" % `advanced`)

		self.advanced = advanced

		# serial packet stream
		self.ps = SerialPacketStream(sherpaPort)
		self.ps.start()
		
		# initialize uSherpa API
		self.us = uSherpa(self.ps)
		self.us.retrys = 5

		# reset robot
		self.us.reset()

		# construct dual channel motor controller
		mch1 = MCtlChannel(self.us, uSherpa.PIN_1_4, uSherpa.PIN_1_5)
		mch2 = MCtlChannel(self.us, uSherpa.PIN_1_6, uSherpa.PIN_1_7)
		mctl = DualChannelMCtl(mch1, mch2)

		# construct trigger for handling external interrupts of wheel encoders
		if advanced:
			tr = Trigger(self.us)
			tr.add(uSherpa.PIN_2_3, uSherpa.EDGE_LOWHIGH)
			tr.add(uSherpa.PIN_2_4, uSherpa.EDGE_LOWHIGH)

		# construct range finder
		rf  = RangeFinder(self.us, uSherpa.PIN_2_0)

		# assemble vehicle
		if advanced:
			self.vehicle  = AdvancedVehicle(mctl, tr, rf)
		else:
			self.vehicle  = Vehicle(mctl)

		# construct pan servo
		pan = Servo(self.us, uSherpa.PIN_2_2)

		# assemble range finder on pan
		self.panrf = PanRf(pan, rf)
	
	def __del__(self):
	
		self.shutdown()

	def shutdown(self):

		if not self.ps == None:
			self.ps.stop()

