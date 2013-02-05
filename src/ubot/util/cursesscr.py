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

import curses 

class CursesScreen:

	screen = None

	def __init__(self):
		self.start()

	def __del__(self):
		self.end()

	def start(self):
		self.screen = curses.initscr()
		curses.noecho()
		curses.cbreak()
		self.screen.keypad(1)

	def end(self):
		self.screen.keypad(0)
		curses.nocbreak()
		curses.echo()
		curses.endwin()	
