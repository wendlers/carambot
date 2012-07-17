"""
 Digital IO on Carambola Board
"""

class Pin: 

	pinId  		= None 
	pinDir 		= ""

	def __init__(self, pinId):
		self.pinId = pinId
		self.export()

	def __del__(self):
		self.unexport()

	def state(self):
		f = file(self.pinDir + "value", "r")
		s = f.read()	
		f.close()
		
		print "- raw value: " + s

		if s == "1\n": 
			return 1 

		return 0 

	def export(self):
		f = file("/sys/class/gpio/export", "w")
		f.write("%d" % self.pinId)
		f.close()
		self.pinDir = "/sys/class/gpio/gpio%d/" % self.pinId 

	def unexport(self):
		f = file("/sys/class/gpio/unexport", "w")
		f.write("%d" % self.pinId)
		f.close()

	def __str__(self):
		return "P_" + `self.pinId`


class PinIn(Pin): 

	def __init__(self, pinId):
		Pin.__init__(self, pinId)
		f = file(self.pinDir + "direction", "w")
		f.write("in")
		f.close()


class PinOut(Pin):

	def __init__(self, pinId):
		Pin.__init__(self, pinId)
		f = file(self.pinDir + "direction", "w")
		f.write("out")
		f.close()

	def set(self):
		f = file(self.pinDir + "value", "w")
		f.write("1")	
		f.close()

	def clear(self):
		f = file(self.pinDir + "value", "w")
		f.write("0")	
		f.close()

	def toggle(self):
		if self.state() == 1: 
			self.clear()
		else:
			self.set()			


class DigitalIO:

	def getInput(self, pinId):
		return PinIn(pinId)

	def getOutput(self, pinId):
		return PinOut(pinId)

	def release(self, pin):
		del pin

