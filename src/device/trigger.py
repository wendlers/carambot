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

from threading 	import Lock
from thread 	import start_new_thread

from usherpa.api import * 

class Trigger:

	us   	 		= None

	handlerSetup  	= None  

	activeHandlers 	= None  

	handlerLock 	= None

	def __init__(self, us): 

		self.us = us
		self.us.packetStream.evHandler = self.__handleTrigger 

		self.handlerSetup	= {}  
		self.activeHandlers = {}  
		self.handlerLock 	= Lock()

	def __handleTrigger(self, msg, packet):

		print "received trigger:", msg, ":", packet

		self.handlerLock.acquire()

		try:

			# get handler for that pin and deactivate it
			handler = self.deactivate(packet.data[0])

			# if handler was found, process it asynchroniously
			if not handler == None:
				# start_new_thread(handler, (msg, packet.data[0]))
				handler(msg, packet.data[0])

		except Exception as e:
			# TODO: throw own exception ... (?)
			print e
		finally:
			self.handlerLock.release()

	def add(self, pin, edge):

		self.handlerSetup.setdefault(pin, None)
		self.handlerSetup[pin] = edge

		self.us.pinMode(uSherpa.PIN_2_3, uSherpa.INPUT)

	def activate(self, pin, handler, triggerCount):

		if self.handlerSetup.has_key(pin) and not self.activeHandlers.has_key(pin):

			self.activeHandlers.setdefault(pin, None)
			self.activeHandlers[pin] = handler 

			self.us.externalInterrupt(pin, self.handlerSetup[pin], triggerCount)

	def remove(self, pin):

		handler = None

		if self.handlerSetup.has_key(pin):

			self.deactivate(pin)

			self.us.externalInterrupt(pin, uSherpa.EDGE_NONE)

			del self.handlerSetup[pin] 

	def deactivate(self, pin):

		handler = None

		if self.activeHandlers.has_key(pin):
			
			# self.us.externalInterrupt(pin, uSherpa.EDGE_NONE)
			handler = self.activeHandlers[pin] 
			del self.activeHandlers[pin]

		return handler

