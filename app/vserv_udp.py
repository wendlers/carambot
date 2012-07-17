#!/usr/bin/python

from util.udp import UdpServer 
from io.digital import DigitalIO
from device.dcmctl import MCtlChannel, DualChannelMCtl 
from robot.vehicle import Vehicle

SERVER_PORT = 50007

class VehicleServer(UdpServer):

	vehicle = None

	def __init__(self, bindTo = "", port = SERVER_PORT):
		UdpServer.__init__(self, bindTo, port)

		io = DigitalIO()

		mch1 = MCtlChannel(io.getOutput(7), io.getOutput(8))
		mch2 = MCtlChannel(io.getOutput(9), io.getOutput(10))
		mctl = DualChannelMCtl(mch1, mch2)
		self.vehicle  = Vehicle(mctl)

	def dispatch(self, seq, data, clientIp, clientPort):
		print "[%s %s]: %i %s" % (clientIp,clientPort, seq, data)

		try:
			c   = data["msgId"]
			res = { "msgId" : "ok" }

			if c == "fw": 
				print " -> set vehicle to: FORWARD"	
				self.vehicle.fw()
			elif c == "bw": 
				print " -> set vehicle to: BACKWARD"	
				self.vehicle.bw()
			elif c == "le": 
				print " -> set vehicle to: LEFT"	
				self.vehicle.le()
			elif c == "ri": 
				print " -> set vehicle to: RIGHT"	
				self.vehicle.ri()
			elif c == "br": 
				print " -> set vehicle to BREAK"	
				self.vehicle.br()
			else:
				res = { "msgId" : "err", "msg" : "Unknown command" }

			self.respond(clientIp,clientPort, seq, res)

		except Exception as e:
			print e
			res = { "msgId" : "err", "msg" : "Data format mismatch" }
			self.respond(clientIp,clientPort, seq, res)

try:
	srv = VehicleServer()
	srv.run()
except Exception as e:
	print e
