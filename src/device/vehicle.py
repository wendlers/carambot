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
	rangeFinder		= None
	minSafetyRange	= 50

	def __init__(self, dChMCtl, trigger, rangeFinder):

		Vehicle.__init__(self,dChMCtl)

		self.trigger 	 = trigger 
		self.rangeFinder = rangeFinder

	def __triggerHandler(self, msg, pin):
		try:
			if self.triggersActive - 1 == 0:
				Vehicle.br(self)

			self.triggersActive = self.triggersActive - 1 

		except Exception as e:
			print e

	def __waitForTriggers(self, waitForTrigger):

		while self.triggersActive > 0:

			r = self.rangeFinder.currentRange()

			if r < self.minSafetyRange:

				self.br()
				print "BREAK - range finder detected obstacle at", r
				return False

			time.sleep(0.1)

		return True

	def __activateTriggers(self, count):

		for pin in self.trigger.handlerSetup:
			self.trigger.activate(pin, self.__triggerHandler, count)

		self.triggersActive = len(self.trigger.handlerSetup) 

	def __deactivateTriggers(self):

		if self.triggersActive > 0:
			for pin in self.trigger.handlerSetup:
				self.trigger.deactivate(pin)

			self.triggersActive = 0 

	def br(self):

		Vehicle.br(self)
		self.__deactivateTriggers()
		
	def fw(self, count = 0):

		if count > 0:
			self.__activateTriggers(count)
			Vehicle.fw(self)
			return self.__waitForTriggers(waitForTrigger)
		else:
			Vehicle.fw(self)

	def bw(self, count = 0):

		if count > 0:
			self.__activateTriggers(count)
			Vehicle.bw(self)
			return self.__waitForTriggers(waitForTrigger)
		else:
			Vehicle.bw(self)

	def ri(self, count = 0):

		if count > 0:
			self.__activateTriggers(count)
			Vehicle.ri(self)
			return self.__waitForTriggers(waitForTrigger)
		else:
			Vehicle.ri(self)

	def le(self, count = 0):

		if count > 0:
			self.__activateTriggers(count)
			Vehicle.le(self)
			return self.__waitForTriggers(waitForTrigger)
		else:
			Vehicle.le(self)
