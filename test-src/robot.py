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

Very basic test for autonoumos robot driving using the 
ultrasonic range-finder on the pan servo.
'''

import traceback
import time
import threading

from rob.carambot import Robot 

# Instance of robot
rob = None

# minimum distanced until robot searches new direction ...
minr = 150

try:

	print "uSherpa and Carambot rocking the wheels!"

	rob 	= Robot("/dev/ttyS0")
	panrf   = rob.panrf				# the range finder on the pan server
	rf  	= panrf.rf 				# only the range finder
	vehicle = rob.vehicle 			# the vehicle

	# stupid navigation loop
	try:
		while True:

			# (1) move foreward until obstacle was detected
			vehicle.fw()
			
			while rf.currentRange() > minr:
				time.sleep(0.1)	
					
			vehicle.br()

			# (2) scan area at 0, 45, 90, 135, 180 deg., see which has most space
			a = panrf.scanArea()
						
			maxr = 0		# max. range found
			maxp = 90		# postion where found this (in deg.)
					
			# search scan result for pos. with max. space
			for v in a:
				for p in v:
					if v[p] > maxr:
						maxr = v[p]
						maxp = p
						
			print "Most promising direction is", maxr, maxp 
			
			# 90 deg. is center, above 90 deg. meens found max. space on left
			if maxp > 90:
				print "-> left is better"
				vehicle.le()

				# calulating time it take approx. to reach max. pos
				time.sleep(0.01 * ( maxp - 90.0))
			
			# and < 90 means found max. space on right
			else:
				print "-> right is better"
				vehicle.ri()

				# calulating time it take approx. to reach max. pos
				time.sleep(0.01 * maxp)

			# no go forward, start again at (1)

	except KeyboardInterrupt:
		vehicle.br()

except Exception as e:
	print traceback.format_exc()
finally:
	if not rob == None:
		rob.shutdown()
