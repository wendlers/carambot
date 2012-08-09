"""
Device Trigger Counter 
"""

from usherpa.api import * 

class Trigger:

	us   	= None
	pin  	= None 
	handler = None

	def __init__(self, us, pin, handler): 
		self.us  	 = us
		self.pin 	 = pin
		self.handler = handler
	
		self.us.pinMode(self.pin, uSherpa.INPUT)	

	def __handleTrigger(self, msg, packet):
		self.disableTrigger()
		self.handler()

	def enableTrigger(self, triggerCount):
		self.us.ps.evHandler = self.__handleTrigger 
		self.us.externalInterrupt(self.pin, uSherpa.EDGE_LOWHIGH, triggerCount)

	def disableTrigger(self):
		self.us.ps.evHandler = None
		self.us.externalInterrupt(self.pin, uSherpa.EDGE_NONE)

