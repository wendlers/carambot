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

	trigger 	= None
	triggerPin 	= None
	triggerActive = False

	def __init__(self, dChMCtl, trigger, triggerPin, triggerEdge):
		Vehicle.__init__(self,dChMCtl)

		self.trigger 	 = trigger 
		self.triggerPin  = triggerPin
		self.triggerEdge = triggerEdge

	def __triggerHandler(self):
		self.br()		
		self.triggerActive = False

	def __waitForTrigger(self, waitForTrigger):
		while waitForTrigger and self.triggerActive:
			time.sleep(0.1)	

	def br(self):
		Vehicle.br(self)
		self.trigger.remove(self.triggerPin)
		self.triggerActive = False
		
	def fw(self, count, waitForTrigger = True):
		self.triggerActive = True 
		self.trigger.add(self.triggerPin, self.triggerEdge, self.__triggerHandler, count)
		Vehicle.fw(self)
		self.__waitForTrigger(waitForTrigger)

	def bw(self, count, waitForTrigger = True):
		self.triggerActive = True 
		self.trigger.add(self.triggerPin, self.triggerEdge, self.__triggerHandler, count)
		Vehicle.bw(self)
		self.__waitForTrigger(waitForTrigger)

	def ri(self, count, waitForTrigger = True):
		self.triggerActive = True 
		self.trigger.add(self.triggerPin, self.triggerEdge, self.__triggerHandler, count)
		Vehicle.ri(self)
		self.__waitForTrigger(waitForTrigger)

	def le(self, count, waitForTrigger = True):
		self.triggerActive = True 
		self.trigger.add(self.triggerPin, self.triggerEdge, self.__triggerHandler, count)
		Vehicle.le(self)
		self.__waitForTrigger(waitForTrigger)


