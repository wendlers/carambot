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

import logging
import time

from threading import Thread

class RobotPilot(Thread):

	robot = None
	abort = False

	def __init__(self, robot):
		
		Thread.__init__(self)

		logging.info("Constructed simple RobotPilot")

		self.robot = robot	

	def run(self):

		panrf   = self.robot.panrf
		vehicle = self.robot.vehicle
		rf  	= panrf.rf 

		self.abort = False

		while not self.abort:

			# (1) move foreward until obstacle was detected
			logging.info("Autopilot: moving forward until obstacle detected")
			vehicle.fw()
			
			while rf.currentRange() > minr and not self.abort:
				time.sleep(0.1)	
					
			vehicle.br()

			if self.abort:
				logging.info("Autopilot: aborted")
				break

			logging.info("Autopilot: stopped because of obstacle, scanning for new direction")

			# (2) scan area at 0, 45, 90, 135, 180 deg., see which has most space
			a = panrf.scanArea()
				
			logging.info("Autopilot: area = " + `a`)

			maxr = 0		# max. range found
			maxp = 90		# postion where found this (in deg.)
					
			# search scan result for pos. with max. space
			for v in a:
				for p in v:
					if v[p] > maxr:
						maxr = v[p]
						maxp = p

			if self.abort:
				logging.info("Autopilot: aborted")
				break
						
			print "Most promising direction is", maxr, maxp 
			
			logging.info("Autopilot: most promising range is %i at %i deg." % (maxr, maxp))

			# 90 deg. is center, above 90 deg. meens found max. space on left
			if maxp > 90:

				logging.info("Autopilot: turning left for new direction")
				vehicle.le()

				# calulating time it take approx. to reach max. pos
				time.sleep(0.01 * ( maxp - 90.0))
			
			# and < 90 means found max. space on right
			else:

				logging.info("Autopilot: turning right for new direction")
				vehicle.ri()

				# calulating time it take approx. to reach max. pos
				time.sleep(0.01 * maxp)

			# no go forward, start again at (1)

