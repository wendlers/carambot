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

import sys
import curses
import traceback

from optparse import OptionParser
from rob.client import RobotClient

cli = None

class CarambotClient(RobotClient):

	def __init__(self, clientPort, server, serverPort):
		RobotClient.__init__(self, clientPort, server, serverPort)

	def displayHelp(self):

		self.helpWin.addstr(2, 2, "Carambot specific commands:")
		self.helpWin.addstr(4, 2, "LEFT   Move left")
		self.helpWin.addstr(5, 2, "RIGHT  Move right")
		self.helpWin.addstr(6, 2, "UP     Move forward")
		self.helpWin.addstr(7, 2, "DOWN   Move backward")
		self.helpWin.addstr(8, 2, "SPACE  Break")

	def processRobotCommands(self, c):

			if c == curses.KEY_UP: 
				cmd = "FORWARD"
				req = { "msgId" : "mv", "dir" : "fw" }

			elif c == curses.KEY_DOWN: 
				cmd = "BACKWARD"	
				req = { "msgId" : "mv", "dir" : "bw" }

			elif c == curses.KEY_LEFT: 
				cmd = "LEFT"	
				req = { "msgId" : "mv", "dir" : "le" }

			elif c == curses.KEY_RIGHT: 
				cmd = "RIGHT"	
				req = { "msgId" : "mv", "dir" : "ri" }

			elif c == ord(' '): 
				cmd = "BREAK"	
				req = { "msgId" : "mv", "dir" : "br" }

			elif c == ord('g'): 
				cmd = "PAN-0"	
				req = { "msgId" : "pan", "pos" : 0 }

			elif c == ord('f'): 
				cmd = "PAN-45"	
				req = { "msgId" : "pan", "pos" : 45 }

			elif c == ord('d'): 
				cmd = "PAN-90"	
				req = { "msgId" : "pan", "pos" : 90 }

			elif c == ord('s'): 
				cmd = "PAN-135"	
				req = { "msgId" : "pan", "pos" : 135 }

			elif c == ord('a'): 
				cmd = "PAN-180"	
				req = { "msgId" : "pan", "pos" : 180 }

			elif c == ord('S'): 
				cmd = "SCAN-AREA"	
				req = { "msgId" : "scan" }
	
			else:

				return False

			if not req == None:

				try: 
					res = self.xfer(req)
					self.addCommand(cmd, `res`)

				except Exception as e:

					self.addCommand(cmd, e.__str__(), 2)

			return True

try:

	parser = OptionParser() 

	parser.add_option("-s", "--server", dest="server", 
		help="Robot server IP or hostname", metavar="HOST") 

	parser.add_option("-c", "--clientport", dest="clientport", type="int", 
		help="Robot client port (default 50008)", default=50008, metavar="PORT") 

	parser.add_option("-p", "--port", dest="port", type="int",
		help="Robot server port (default 50007)", default=50007, metavar="PORT") 

 	(options, args) = parser.parse_args()

	if options.server == None:
		print "Missing argument: -s/--server"
		sys.exit(1)

	cli	= CarambotClient(options.clientport, options.server, options.port)
	cli.run()
	cli.end()

except Exception as e:
	if not cli == None:
		cli.end()	

	print traceback.format_exc()
