"""
 Drive Motor Controller 
"""

from usherpa.api import * 

class MCtlChannel:

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

	def fw(self):
		self.us.digitalWrite(self.pin1, uSherpa.LOW)  
		self.us.digitalWrite(self.pin2, uSherpa.HIGH)

	def bw(self):
		self.us.digitalWrite(self.pin1, uSherpa.HIGH)  
		self.us.digitalWrite(self.pin2, uSherpa.HIGH)


class DualChannelMCtl:

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

