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

from util.udp import UdpServer 

SERVER_PORT = 50007

class RobotServer(UdpServer):
	'''
	Carambot server class running on the Carambola. It listens on UPD port
	defined by SERVER_PORT. 
	'''
 
	robot = None
	
	def __init__(self, robot, port = SERVER_PORT):
		UdpServer.__init__(self, "", port)

		logging.info("Started RobotServer at port %s" % port)

		self.robot = robot

	def __del__(self):
		self.end()

	def end(self):
		self.robot.shutdown()

	def dispatch(self, seq, data, clientIp, clientPort):
		logging.debug("[%s %s]: %i %s" % (clientIp,clientPort, seq, data))

		try:
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

			self.respond(clientIp,clientPort, seq, res)

		except Exception as e:
			print e
			res = { "msgId" : "err", "msg" : "Data format mismatch" }
			self.respond(clientIp,clientPort, seq, res)

