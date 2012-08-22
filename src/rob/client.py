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

import curses 

from util.cursesscr import CursesScreen
from util.udp 		import UdpClient, UdpCommException

CLIENT_PORT = 50008
SERVER      = "127.0.0.1"
SERVER_PORT = 50007
SEND_TIMEOUT= 5

class RobotClient(UdpClient, CursesScreen):
	'''
	Carambot client class. Connects to a CarambotServer instance through UDP 
	port defined by CLIENT_PORT or specified at instance creation.
	'''
 
	GREEN 	= None
	RED		= None
	BLUE	= None
	YELLOW	= None

	curY = 1
	serverPort = None
	server = None

	def __init__(self, clientPort = CLIENT_PORT, server = SERVER, serverPort = SERVER_PORT):

		self.serverPort = serverPort
		self.server 	= server

		CursesScreen.__init__(self)
		UdpClient.__init__(self, "", clientPort)
		self.initScreen()

	def __del__(self):

		try:
			self.end()
		except:
			pass

		try:
			self.socket.close()
		except:
			pass

	def initScreen(self):

		curses.start_color()
		curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
		curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
 
		self.GREEN 	= curses.color_pair(1)
		self.RED	= curses.color_pair(2)
		self.BLUE	= curses.color_pair(3)
		self.YELLOW	= curses.color_pair(4)

		self.screen.addstr("**\n", self.RED)
		self.screen.addstr("* Simpe RobotControl. Use the following keys:\n", self.RED)
		self.screen.addstr("* - UP \t\tforward\n", self.RED)
		self.screen.addstr("* - DOWN\tbackward\n", self.RED)
		self.screen.addstr("* - LEFT\tleft\n", self.RED)
		self.screen.addstr("* - RIGHT\tright\n", self.RED)
		self.screen.addstr("* - SPACE\tbreak\n", self.RED)
		self.screen.addstr("* - q\t\tquit\n", self.RED)
		self.screen.addstr("**\n\n", self.RED)

		self.curY = 11;

	def run(self):	
		while True:

	 		maxY, maxX = self.screen.getmaxyx()

			if self.curY >= maxY:
				self.screen.clear()
				self.screen.addstr("** screenwrap **\n", self.RED)
				self.curY = 2

			c = self.screen.getch()

			self.screen.addstr("-> ", self.BLUE)

			req = None

			if c == curses.KEY_UP: 
				self.screen.addstr("FORWARD", self.YELLOW)	
				req = { "msgId" : "mv", "dir" : "fw" }
			elif c == curses.KEY_DOWN: 
				self.screen.addstr("BACKWARD", self.YELLOW)	
				req = { "msgId" : "mv", "dir" : "bw" }
			elif c == curses.KEY_LEFT: 
				self.screen.addstr("LEFT", self.YELLOW)	
				req = { "msgId" : "mv", "dir" : "le" }
			elif c == curses.KEY_RIGHT: 
				self.screen.addstr("RIGHT", self.YELLOW)	
				req = { "msgId" : "mv", "dir" : "ri" }
			elif c == ord(' '): 
				self.screen.addstr("BREAK", self.YELLOW)	
				req = { "msgId" : "mv", "dir" : "br" }
			elif c == ord('g'): 
				self.screen.addstr("PAN-0-DEG", self.YELLOW)	
				req = { "msgId" : "pan", "pos" : 0 }
			elif c == ord('f'): 
				self.screen.addstr("PAN-45-DEG", self.YELLOW)	
				req = { "msgId" : "pan", "pos" : 45 }
			elif c == ord('d'): 
				self.screen.addstr("PAN-90-DEG", self.YELLOW)	
				req = { "msgId" : "pan", "pos" : 90 }
			elif c == ord('s'): 
				self.screen.addstr("PAN-135-DEG", self.YELLOW)	
				req = { "msgId" : "pan", "pos" : 135 }
			elif c == ord('a'): 
				self.screen.addstr("PAN-180-DEG", self.YELLOW)	
				req = { "msgId" : "pan", "pos" : 180 }
			elif c == ord('S'): 
				self.screen.addstr("SCAN-AREA", self.YELLOW)	
				req = { "msgId" : "scan" }
			elif c == ord('q'): 
				break  # Exit the while()
			else:
				self.screen.addstr("UNKNOWN KEY\n", self.RED)	
				self.curY = self.curY + 1

			if req != None:

				col = self.RED
				msg = None

				try: 
					res = self.xfer(req)

					try:
						msg = res["msgId"] + ": " + res["msg"]
					except:
						col = self.GREEN
						msg = res["msgId"];

				except UdpCommException as ce:
					msg = "ex: " + ce.__str__()

				self.screen.addstr(" = " + msg + "\n",col)	
				self.curY = self.curY + 1

	def xfer(self, data):
		self.send(self.server, self.serverPort , data)
		return self.receive(self.server, self.serverPort, SEND_TIMEOUT)

