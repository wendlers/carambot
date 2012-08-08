"""
 Drive Servo 
"""

from usherpa.api import * 

class Servo:

	us  = None
	pin = None 

	def __init__(self, us, pin): 
		self.us  = us
		self.pin = pin
	
		self.us.pinMode(self.pin, uSherpa.PWM)	
		self.us.pwmPeriod(self.pin, 22000)

		self.goTo(90)

	def __deg2duty(self, deg):
		d = deg

		if d < 0:
			d = 0
		elif d > 180:
			d = 180 

		t = 180 / 10.5

		dc = float(d / t) + 3.5 

		usDc = 0xFF / 100 * dc

		return int(usDc)

	def goTo(self, deg):
		self.us.pwmDuty(self.pin, self.__deg2duty(deg))

