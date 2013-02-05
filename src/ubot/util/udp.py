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

import pickle

from select import select
from socket import *

class UdpCommException(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)


class UdpServer:

	bufSize	= 1024
	socket 	= None

	def __init__(self, bindTo = "", port = 50007):
		self.socket = socket(AF_INET, SOCK_DGRAM)
		self.socket.bind((bindTo, port))

	def __del__(self):
		self.socket.close()

	def run(self):
		try:
			while 1:
				msgStr, (clientIp,clientPort) = self.socket.recvfrom(self.bufSize)
				msg = pickle.loads(msgStr)
				self.dispatch(msg["seq"], msg["data"], clientIp, clientPort)
		except KeyboardInterrupt:
			pass

	def respond(self, clientIp, clientPort, seq, data):
		msg = { "seq" : seq, "data": data }
		self.socket.sendto(pickle.dumps(msg), (clientIp, clientPort))

	def dispatch(seq, self, data, clientIp, clientPort):
		print "[%s %s]: %i %s" % (clientIp,clientPort,seq, data)


class UdpClient:

	bufSize		= 1024
	socket 		= None
	seq			= 0

	def __init__(self, bindTo = "", port = 50008):
		self.socket = socket(AF_INET, SOCK_DGRAM)
		self.socket.bind((bindTo, port))

	def __del__(self):
		self.socket.close()

	def send(self, serverIp, serverPort, data):
		self.seq = self.seq + 1
		msg = { "seq" : self.seq, "data": data }
		self.socket.sendto(pickle.dumps(msg), (serverIp, serverPort))
		return self.seq

	def receive(self, serverIp, serverPort, timeout, lastSeq = None):

		ready  = select([self.socket], [], [], timeout)
		msgStr = None
		ip     = None
		port   = None

		if ready[0]:
			msgStr, (ip, port) = self.socket.recvfrom(self.bufSize)

		if msgStr == None: 
			raise UdpCommException("Timeout while waiting for response")

		msg = pickle.loads(msgStr)

		if lastSeq != None and msg["seq"] != lastSeq:
			raise UdpCommException("Unexpected sequence # in response")
			
		return msg["data"] 


	def xfer(self, serverIp, serverPort, timeout, data):
		lastSeq = self.send(serverIp, serverPort, data)
		return self.receive(serverIp, serverPort, timeout, lastSeq)

