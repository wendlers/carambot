"""
 Drive Range Finder 
"""

from usherpa.api import * 

class RangeFinder:

	us  = None
	pin = None 

	def __init__(self, us, pin): 
		self.us  = us
		self.pin = pin
	
		self.us.pinMode(self.pin, uSherpa.PULLDOWN)	

	def range(self):
		return self.us.pulselengthRead(self.pin, True); 		

