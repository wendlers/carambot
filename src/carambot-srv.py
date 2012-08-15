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

from util.udp import UdpServer 

from device.dcmctl import MCtlChannel, DualChannelMCtl
from device.servo  import Servo 
from device.rangefinder import RangeFinder 

from robot.vehicle import Vehicle
from robot.panrf import PanRf 

from usherpa.api import *                    
from usherpa.serialcomm import *

SERVER_PORT = 50007

class CarambotServer(UdpServer):
	'''
	Carambot server class running on the Carambola. It listens on UPD port
	defined by SERVER_PORT. 
	'''
 
	vehicle = None
	panrf	= None
	ps 		= None
	
	def __init__(self, bindTo = "", port = SERVER_PORT):
		UdpServer.__init__(self, bindTo, port)

		self.ps = SerialPacketStream("/dev/ttyUSB0")
		# self.ps = SerialPacketStream("/dev/ttyS0")
		self.ps.start()
		
		us = uSherpa(self.ps)
		
		# set xfer retrys to 3
		us.retrys = 3
			
		mch1 = MCtlChannel(us, uSherpa.PIN_1_4, uSherpa.PIN_1_5)
		mch2 = MCtlChannel(us, uSherpa.PIN_1_6, uSherpa.PIN_1_7)
		mctl = DualChannelMCtl(mch1, mch2)
		self.vehicle  = Vehicle(mctl)

		pan = Servo(us, uSherpa.PIN_2_2)
		rf  = RangeFinder(us, uSherpa.PIN_2_0)
		self.panrf = PanRf(pan, rf)
		

	def end(self):
		self.ps.stop()
		
	def dispatch(self, seq, data, clientIp, clientPort):
		print "[%s %s]: %i %s" % (clientIp,clientPort, seq, data)

		try:
			res = { "msgId" : "ok" }

			c   = data["msgId"]

			if c == "mv":

				d = data["dir"]

				if d == "fw": 
					print " -> set vehicle to: FORWARD"	
					self.vehicle.fw()
				elif d == "bw": 
					print " -> set vehicle to: BACKWARD"	
					self.vehicle.bw()
				elif d == "le": 
					print " -> set vehicle to: LEFT"	
					self.vehicle.le()
				elif d == "ri": 
					print " -> set vehicle to: RIGHT"	
					self.vehicle.ri()
				elif d == "br": 
					print " -> set vehicle to BREAK"	
					self.vehicle.br()
				else:
					res = { "msgId" : "err", "msg" : "Command mv: unknown direction " + d }

			elif c == "pan":

				d = data["pos"]
				r = self.panrf.rangeAt(d)
				print " -> set pan to pos", d
				print " -> range finder range:", r
				res = { "msgId" : "range", "msg" : `r` + "@" + `d` }

			elif c == "scan":

				a = self.panrf.scanArea()
				print " -> scan area:", a
				res = { "msgId" : "scan", "msg" : `a` }

			self.respond(clientIp,clientPort, seq, res)

		except Exception as e:
			print e
			res = { "msgId" : "err", "msg" : "Data format mismatch" }
			self.respond(clientIp,clientPort, seq, res)

try:
	srv = CarambotServer()
	srv.run()
	srv.end()
except Exception as e:
	print e
