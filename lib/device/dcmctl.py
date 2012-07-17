"""
 Drive Motor Controller 
"""

from io.digital import PinOut

class MCtlChannel:

	pin1 = None 
	pin2 = None 

	def __init__(self, pin1, pin2): 
		self.pin1 = pin1
		self.pin2 = pin2

	def br(self):
		self.pin1.clear()
		self.pin2.clear()

	def fw(self):
		self.pin1.set()
		self.pin2.clear()

	def bw(self):
		self.pin1.set()
		self.pin2.set()

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

