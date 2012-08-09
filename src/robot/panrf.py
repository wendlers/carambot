'''
Range finder with pan unit
'''

from device.servo  import Servo 
from device.rangefinder import RangeFinder 

class PanRf:

	pan = None
	rf  = None

	def __init__(self, pan, rf):
		self.pan = pan
		self.rf  = rf

	def __debouncedRangeRead(self, maxDelta = 5, maxTries = 3, compReadings = 3):

		r  = 0 

		for i in range(maxTries):	

			pr = self.rf.currentRange()

			for j in range(compReadings):
				r = self.rf.currentRange()
				if abs(pr - r) > maxDelta:
					break

			if j == compReadings:
				return r

		return -1

	def scanArea(self, positions = [ 0, 45, 90, 135, 180] , endPos = 90):

		ranges = []

		for p in positions:
			self.pan.goTo(p)
			ranges.add( { p : self.__debouncedRangeRead() } )
			
		self.pan.goTo(endPos)

		return ranges


	def rangeAt(self, position):
		self.pan.goTo(position)
		return self.__debouncedRangeRead()
