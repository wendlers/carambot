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

from usherpa.api import * 

class MCtlChannel:
	'''
	Single channel of a dual channel motor controller.
	'''

	us   = None
	pin1 = None 
	pin2 = None 

	def __init__(self, us, pin1, pin2): 
		self.us   = us
		self.pin1 = pin1
		self.pin2 = pin2
			
		self.us.pinMode(self.pin1, uSherpa.OUTPUT)	
		self.us.pinMode(self.pin2, uSherpa.OUTPUT)	

	def br(self):
		self.us.digitalWrite(self.pin1, uSherpa.LOW)  
		self.us.digitalWrite(self.pin2, uSherpa.LOW)

	def bw(self):
		self.us.digitalWrite(self.pin1, uSherpa.LOW)  
		self.us.digitalWrite(self.pin2, uSherpa.HIGH)

	def fw(self):
		self.us.digitalWrite(self.pin1, uSherpa.HIGH)  
		self.us.digitalWrite(self.pin2, uSherpa.HIGH)


class DualChannelMCtl:
	'''
	Dual channel motor controller to operate two motors indipendently.
	'''

	ch1 = None 
	ch2 = None 

	def __init__(self, ch1, ch2):
		self.ch1 = ch1
		self.ch2 = ch2

	def __apply2ch(self, applyCh1, applyCh2, opCh1, opCh2):
		if applyCh1:
			opCh1()
		if applyCh2:
			opCh2()	
	
	def br(self, applyCh1, applyCh2):
		self.__apply2ch(applyCh1, applyCh2, self.ch1.br, self.ch2.br)

	def fw(self, applyCh1, applyCh2):
		self.__apply2ch(applyCh1, applyCh2, self.ch1.fw, self.ch2.fw)

	def bw(self, applyCh1, applyCh2):
		self.__apply2ch(applyCh1, applyCh2, self.ch1.bw, self.ch2.bw)

