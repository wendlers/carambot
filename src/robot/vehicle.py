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

import time

from device.dcmctl import DualChannelMCtl 
from device.trigger import Trigger

class Vehicle:

	mctl = None

	def __init__(self, dChMCtl):
		self.mctl = dChMCtl

	def fw(self):
		self.mctl.fw(1, 1)

	def bw(self):
		self.mctl.bw(1, 1)

	def br(self):
		self.mctl.br(1, 1)

	def le(self):
		self.mctl.fw(1, 0)
		self.mctl.bw(0, 1)

	def ri(self):
		self.mctl.bw(1, 0)
		self.mctl.fw(0, 1)	

class AdvancedVehicle(Vehicle):

	trigger 		= None
	triggersActive 	= 0

	def __init__(self, dChMCtl, trigger):
		Vehicle.__init__(self,dChMCtl)
		self.trigger 	 = trigger 

	def __triggerHandler(self, msg, pin):
		try:
			self.br()
			self.triggersActive = False 
		except Exception as e:
			print e

	def __waitForTriggers(self, waitForTrigger):
		# FIXME: ugly polling - use condition?
		while self.triggersActive:
			time.sleep(0.1)

	def __activateTriggers(self, count):

		for pin in self.trigger.handlerSetup:
			self.trigger.activate(pin, self.__triggerHandler, count)

		self.triggersActive = True 

	def __deactivateTriggers(self):
		self.triggersActive = False 

	def br(self):
		Vehicle.br(self)
		self.__deactivateTriggers()

	def fw(self, count, waitForTrigger = True):
		self.__activateTriggers(count)
		Vehicle.fw(self)
		self.__waitForTriggers(waitForTrigger)

	def bw(self, count, waitForTrigger = True):
		self.__activateTriggers(count)
		Vehicle.bw(self)
		self.__waitForTriggers(waitForTrigger)

	def ri(self, count, waitForTrigger = True):
		self.__activateTriggers(count)
		Vehicle.ri(self)
		self.__waitForTriggers(waitForTrigger)

	def le(self, count, waitForTrigger = True):
		self.__activateTriggers(count)
		Vehicle.le(self)
		self.__waitForTriggers(waitForTrigger)

