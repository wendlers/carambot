#!/usr/bin/python

from util.udp import UdpServer 
from device.dcmctl import MCtlChannel, DualChannelMCtl 
from robot.vehicle import Vehicle

from usherpa.api import *                    
from usherpa.serialcomm import *

SERVER_PORT = 50007

class VehicleServer(UdpServer):

	vehicle = None

	ps 	= None
	
	def __init__(self, bindTo = "", port = SERVER_PORT):
		UdpServer.__init__(self, bindTo, port)

		self.ps = SerialPacketStream("/dev/ttyS0")
		self.ps.start()
		
		us = uSherpa(self.ps)
		
		# set xfer retrys to 3
		us.retrys = 3
			
		mch1 = MCtlChannel(us, uSherpa.PIN_1_4, uSherpa.PIN_1_5)
		mch2 = MCtlChannel(us, uSherpa.PIN_1_6, uSherpa.PIN_1_7)
		mctl = DualChannelMCtl(mch1, mch2)
		self.vehicle  = Vehicle(mctl)

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

				print " -> set pan to pos", d

			elif c == "rf":

				print " -> range finder"

			self.respond(clientIp,clientPort, seq, res)

		except Exception as e:
			print e
			res = { "msgId" : "err", "msg" : "Data format mismatch" }
			self.respond(clientIp,clientPort, seq, res)

try:
	srv = VehicleServer()
	srv.run()
	srv.end()
except Exception as e:
	print e
