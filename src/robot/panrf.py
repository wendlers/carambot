'''
Range finder with pan unit
'''

import time

from device.servo  import Servo 
from device.rangefinder import RangeFinder 

class PanRf:

	pan = None
	rf  = None
	pos = 90
	
	def __init__(self, pan, rf):
		self.pan = pan
		self.rf  = rf

	def __debouncedRangeRead(self, maxDelta = 5, maxTries = 6, compReadings = 3):

		r  = 0 	# reading
		pr = 0	# pre reading
		ra = 0	# reding average
		
		for i in range(maxTries):	

			pr = self.rf.currentRange()

			stable = True	# assume result is stable
			ra = pr

			for j in range(1, compReadings):

				r = self.rf.currentRange()
				ra = ra + r

				if abs(pr - r) > maxDelta:
					stable = False 	# delta was to big - not stable yet
					break

			if stable:
				return int(ra / compReadings)

		print " -> debouncedRangeRead: unable to get stable range after", maxTries, "tries"

		return -1

	def scanArea(self, positions = [ 0, 45, 90, 135, 180] , endPos = 90):

		ranges = []

		for p in positions:
			ranges.append( { p : self.rangeAt(p) } )
			
		self.pan.goTo(endPos)

		return ranges


	def rangeAt(self, position):
		self.pan.goTo(position)

		d = float(abs(self.pos - position)) / 180.0
		time.sleep(d)
		self.pos = position

		return self.__debouncedRangeRead()
