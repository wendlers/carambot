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

VERSION="Carambot Server v0.1"

import traceback
import logging
import logging.handlers

from optparse import OptionParser

from rob.carambot 		import Robot
from rob.server 		import RobotServer
from rob.simplepilot 	import RobotPilot

srv = None

class CarambotServer(RobotServer):

	pilot = None

	def __init__(self, robot, port):
		RobotServer.__init__(self, robot, port)

	def dispatchRobotCommands(self, data):

		# if autopilot is running, stop it
		if not self.pilot == None:

			logging.debug("Autopilot is running, trying to stop it ...")
			self.pilot.abort = True
			self.pilot.join()
			del self.pilot
			logging.debug("Autopilot stopped")

		res = { "msgId" : "ok" }

		c   = data["msgId"]

		if c == "mv":

			d = data["dir"]

			if d == "fw": 
				logging.debug("set vehicle to: FORWARD")	
				self.robot.vehicle.fw()
			elif d == "bw": 
				logging.debug("set vehicle to: BACKWARD")	
				self.robot.vehicle.bw()
			elif d == "le": 
				logging.debug("set vehicle to: LEFT")	
				self.robot.vehicle.le()
			elif d == "ri": 
				logging.debug("set vehicle to: RIGHT")	
				self.robot.vehicle.ri()
			elif d == "br": 
				logging.debug("set vehicle to BREAK")	
				self.robot.vehicle.br()
			else:
				res = { "msgId" : "err", "msg" : "Command mv: unknown direction " + d }

		elif c == "tr":

			if data["deg"] == 0:
				logging.debug("not turning robot")
			else:

				d = int(data["deg"] / 5)

				if d < 0:
					logging.debug("turning robot for %i ticks left" % abs(d))
					self.robot.vehicle.le(abs(d))
				else:	
					logging.debug("turning robot for %i ticks right" % d)
					self.robot.vehicle.ri(d)

		elif c == "fw":

			if data["tic"] == 0:
				logging.debug("not moving robot")
			else:
				logging.debug("moving robot forward %i tics" % data["tic"])
				f = self.robot.vehicle.fw(data["tic"])	

				res = { "msgId" : "ok", "full" : `f` }

		elif c == "pan":

			d = data["pos"]
			r = self.robot.panrf.rangeAt(d)
			logging.debug("set pan to pos %i" % d)
			logging.debug("range finder range: %i" % r)
			res = { "msgId" : "range", "msg" : `r` + "@" + `d` }

		elif c == "scan":

			a = self.robot.panrf.scanArea()
			logging.debug("scan area: %s" % a)
			res = { "msgId" : "scan", "msg" : `a` }

		elif c == "auto":
			logging.debug("Starting autupilot thread")
			self.pilot = RobotPilot(self.robot)
			self.pilot.daemon = True
			self.pilot.start()

		return res

try:
	parser = OptionParser() 

	parser.add_option("-p", "--port", dest="port", type="int",
		help="Robot server port (default 50007)", default=50007, metavar="PORT") 

	parser.add_option("-c", "--logclient", dest="logclient",
		help="Client name/ip for remote logging", metavar="HOST") 

	parser.add_option("-s", "--serialport", dest="serialport", 
		help="uSherpa serial port (default /dev/ttyS0)", default="/dev/ttyS0", metavar="PORT") 

	parser.add_option("-v", "--verbose", dest="verboselevel", type="int",
		help="Verbose level for logging (10: DEBUG, 50: CRITICAL)", default=20, metavar="LEVEL") 

 	(options, args) = parser.parse_args()

	logging.basicConfig(level=options.verboselevel)

	# add remote log client (if requested)
	if not options.logclient == None:
		socketHandler = logging.handlers.SocketHandler(options.logclient, 
			logging.handlers.DEFAULT_TCP_LOGGING_PORT)
		rootLogger = logging.getLogger()
		rootLogger.addHandler(socketHandler)

	logging.info(VERSION)
	logging.info("uSherpa and Carambot rocking the wheels!")

	rob 	= Robot(options.serialport, True)
	srv		= CarambotServer(rob, options.port)

	srv.run()

except Exception as e:

	logging.error(`e` + "::" + e.__str__())

finally:

	if not srv == None:
		srv.end()
