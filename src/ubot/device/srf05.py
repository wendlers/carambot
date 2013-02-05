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

class RangeFinder:

	us  = None
	pin = None 

	minRange = 150

	def __init__(self, us, pin): 
		self.us  = us
		self.pin = pin
	
		self.us.pinMode(self.pin, uSherpa.INPUT)	

	def currentRange(self):
		return self.us.pulselengthRead(self.pin, True); 		

