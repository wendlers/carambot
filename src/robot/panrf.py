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

import time

from device.servo import Servo 
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

		# The servo needs some time to move to the targeted position.
		# The bigger the delta between the current position and
		# the desired position, the longer we need to wait until
		# we start measuring the reange. If range is requested to
		# early, it will not stabilize since servo is still moving. 
		d = float(abs(self.pos - position)) / 180.0
		time.sleep(d)
		self.pos = position

		return self.__debouncedRangeRead()
