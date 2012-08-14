"""
  Vehicle
"""

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

