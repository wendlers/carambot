"""
Device Trigger Counter 
"""

from usherpa.api import * 

class Trigger:

	us   	 = None
	handlers = {} 

	def __init__(self, us): 

		self.us = us
		self.us.packetStream.evHandler = self.__handleTrigger 

	def __handleTrigger(self, msg, packet):

		print "received trigger:", msg, ":", packet

		handler = self.remove(packet.data[0])

		if not handler == None:
			handler()

	def add(self, pin, edge, handler, triggerCount):

		self.handlers.setdefault(pin, None)
		self.handlers[pin] = handler
		self.us.externalInterrupt(pin, edge, triggerCount)

	def remove(self, pin):

		handler = None

		if self.handlers.has_key(pin):
			self.us.externalInterrupt(pin, uSherpa.EDGE_NONE)
			handler = self.handlers[pin] 
			del self.handlers[pin] 

		return handler
