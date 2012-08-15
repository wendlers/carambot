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

from usherpa.api import * 

class Servo:
'''
Class representing a servo connected to one of the uSherpas HW PWM ports. 
The class allows you to position the servo in degrees (from 0 to 180).
'''

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

