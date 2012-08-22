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
import pickle
import logging
import logging.handlers
import SocketServer
import struct
import select

from threading import Thread

from util.cursesscr import CursesScreen
from util.udp 		import UdpClient, UdpCommException

CLIENT_PORT = 50008
SERVER      = "127.0.0.1"
SERVER_PORT = 50007
SEND_TIMEOUT= 5

class LogRecordStreamHandler(SocketServer.StreamRequestHandler):
    """Handler for a streaming logging request.

    This basically logs the record using whatever logging policy is
    configured locally.
    """

    def handle(self):
        """
        Handle multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format. Logs the record
        according to whatever policy is configured locally.
        """
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)
            record = logging.makeLogRecord(obj)
            self.handleLogRecord(record)

    def unPickle(self, data):
        return pickle.loads(data)

    def handleLogRecord(self, record):
        # if a name is specified, we use the named logger rather than the one
        # implied by the record.
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name
        logger = logging.getLogger(name)
        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        logger.handle(record)

class LogRecordSocketReceiver(SocketServer.ThreadingTCPServer, Thread):
    """
    Simple TCP socket-based logging receiver suitable for testing.
    """

    allow_reuse_address = 1

    def __init__(self, handler, host='localhost',
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT):
        SocketServer.ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = False 
        self.timeout = 1
        self.logname = None

        Thread.__init__(self)

	def end(self):
		self.abort = True

    def run(self):

        while not self.abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)
            if rd:
                self.handle_request()

class RobotClient(UdpClient, CursesScreen, SocketServer.StreamRequestHandler):
	'''
	Robot client class. Connects to a robot server instance through UDP 
	port defined by CLIENT_PORT or specified at instance creation.
	'''
 
	serverPort 	= None
	server 		= None

	maxX = None
	maxY = None

	menuWin  = None
	cmdWin   = None
	logWin   = None
	helpWin  = None

	cmdPad = None 	
	cmdSeq = 0

	logPad = None
	logPos = 0

	viewMode = 0

	VIEW_MODE_CMDLOG	=	0
	VIEW_MODE_CMDONLY	=	1
	VIEW_MODE_LOGONLY	=	2
	VIEW_MODE_HELP		=	3

	tcpserver = None

	def __init__(self, clientPort = CLIENT_PORT, server = SERVER, serverPort = SERVER_PORT):

		self.serverPort = serverPort
		self.server 	= server

		UdpClient.__init__(self, "", clientPort)
		CursesScreen.__init__(self)
		self.initScreen()

		self.tcpserver = LogRecordSocketReceiver(self)
		self.tcpserver.start()

	def __del__(self):

		try:
			self.end()
		except:
			pass

		try:
			self.tcpserver.stop()
			self.tcpserver.join()
		except:
			pass

		try:
			self.socket.close()
		except:
			pass

	def initScreen(self, refresh = False):

		self.maxY, self.maxX = self.screen.getmaxyx()

			
		curses.start_color()
		curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
		curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

		self.screen.refresh()

		if self.maxY < 20 or self.maxX < 40:
			self.screen.clear()
			self.screen.addstr(0,0, "Screen too small!", curses.color_pair(1))
		else:
			self.showMenu(refresh)
			self.showCommands(refresh)
			self.showLog(refresh)
			self.showHelp(refresh)

	def showMenu(self, resize = False):

		if self.menuWin == None or resize:
			self.menuWin = curses.newwin(3, self.maxX, 0, 0)

		self.menuWin.clear()
		self.menuWin.bkgd(curses.color_pair(1))
		self.menuWin.box()
	
		if self.viewMode == self.VIEW_MODE_HELP:
			self.menuWin.addstr(1, 2, "F10 Exit help")
		else:
			self.menuWin.addstr(1, 2, "F1 Show help | F2 Toggle view | F10 Exit")

		self.menuWin.refresh()

	def showHelp(self, resize = False):

		if not self.viewMode == self.VIEW_MODE_HELP:
			return

		h = self.maxY - 3

		if self.helpWin == None or resize:
			self.helpWin = curses.newwin(h, self.maxX, 3, 0)

		self.helpWin.clear()
		self.helpWin.bkgd(curses.color_pair(1))
		self.helpWin.box()
		self.displayHelp()
		self.helpWin.refresh()

		self.screen.addstr(3, 2, "[Help]")


	def showCommands(self, resize = False):

		if self.viewMode == self.VIEW_MODE_LOGONLY or self.viewMode == self.VIEW_MODE_HELP:
			return

		if self.viewMode == self.VIEW_MODE_CMDONLY:
			h = self.maxY - 3
		else:
			h = int((self.maxY - 3) / 2 + 3) - 3

		if self.cmdWin == None or resize:
			self.cmdWin = curses.newwin(h, self.maxX, 3, 0)

		if self.cmdPad == None:
			self.cmdPad = curses.newpad(self.maxY - 5, self.maxX - 2)

		self.cmdWin.clear()
		self.cmdWin.bkgd(curses.color_pair(1))
		self.cmdWin.box()
		self.cmdWin.addstr(1, 2, "Seq.")
		self.cmdWin.addstr(1, 8, "Command")
		self.cmdWin.addstr(1, 18, "Response")
		self.cmdWin.refresh()

  		self.cmdPad.refresh(0, 0, 5, 1, 1 + h, self.maxX - 2)

		self.screen.addstr(3, 2, "[Command history]")

	def showLog(self, resize = False):

		if self.viewMode == self.VIEW_MODE_CMDONLY or self.viewMode == self.VIEW_MODE_HELP:
			return

		if self.viewMode == self.VIEW_MODE_LOGONLY:
			y = 3
			h = self.maxY - 3
		else:
			y = int((self.maxY - 3) / 2 + 3)
			h = int((self.maxY - 3) / 2 + 3) - 3

		if self.logWin == None or resize:
			self.logWin = curses.newwin(h, self.maxX, y, 0)

		if self.logPad == None:
			self.logPad = curses.newpad(10000, 100)

		self.logWin.clear()
		self.logWin.bkgd(curses.color_pair(1))
		self.logWin.box()
		self.logWin.addstr(1, 2, "viewMode: %i" % self.viewMode)
		self.logWin.refresh()

  		self.logPad.refresh(self.logPos, 0, y + 1, 1, self.maxY - 2, self.maxX - 2)

		self.screen.addstr(y, 2, "[Server log]")

	def addCommand(self, command, response, pair = 1):

		self.cmdSeq = self.cmdSeq + 1

		if self.viewMode == self.VIEW_MODE_CMDONLY:
			h = self.maxY - 3
		else:
			h = int((self.maxY - 3) / 2 + 3) - 3

		self.cmdPad.move(0,1)
		self.cmdPad.insertln()
		self.cmdPad.addstr(0, 1, "%04i" % self.cmdSeq)
		self.cmdPad.addstr(0, 7, command)
		self.cmdPad.addstr(0, 17, response, curses.color_pair(pair))

		if self.viewMode == self.VIEW_MODE_LOGONLY or self.viewMode == self.VIEW_MODE_HELP:
			return 

		self.cmdPad.refresh(0, 0, 5, 1, h + 1, self.maxX - 2)

	def addLog(self, log, pair = 1):

		if self.viewMode == self.VIEW_MODE_LOGONLY:
			y = 3
			h = self.maxY - 3
		else:
			y = int((self.maxY - 3) / 2 + 3)
			h = int((self.maxY - 3) / 2 + 3) - 3

		self.logPad.move(0,1)
		self.logPad.insertln()
		self.logPad.addstr(0, 1, log)

		if self.viewMode == self.VIEW_MODE_CMDONLY or self.viewMode == self.VIEW_MODE_HELP:
			return 

  		self.logPad.refresh(self.logPos, 0, y + 1, 1, self.maxY - 2, self.maxX - 2)

	def displayHelp(self):

		self.helpWin.addstr(2, 2, "Not available!")

	def processRobotCommands(self, c):

		return False 

	def run(self):

		prevViewMode = self.viewMode

		while True:

			self.screen.move(0, 0)

			c = self.screen.getch()

			if c == curses.KEY_F10: 
				if self.viewMode == self.VIEW_MODE_HELP:
					self.viewMode = prevViewMode
					self.initScreen(True)
				else:
					break 

			elif c == curses.KEY_F1:
				if not self.viewMode == self.VIEW_MODE_HELP:
					prevViewMode = self.viewMode
					self.viewMode = self.VIEW_MODE_HELP
					self.initScreen(True)

			elif c == curses.KEY_F2:
				self.viewMode = (self.viewMode + 1) % 3
				self.initScreen(True)
		
			elif c == curses.KEY_NPAGE:
				self.logPos = self.logPos + 5 

				if self.logPos >= 10000:
					self.logPos = 9995

				self.showLog()

			elif c == curses.KEY_PPAGE:
				self.logPos = self.logPos - 5

				if self.logPos < 0:
					self.logPos = 0 

				self.showLog()

			elif c == curses.KEY_RESIZE:
				self.initScreen(True)

			else:

				if not self.processRobotCommands(c):
					self.addCommand("UNKNOWN", "NONE", 4)

		try:
			self.tcpserver.end()
			self.tcpserver.join()
		except:
			pass


	def xfer(self, data):
		self.send(self.server, self.serverPort , data)
		return self.receive(self.server, self.serverPort, SEND_TIMEOUT)

	def handle(self):
		while True:
			chunk = self.connection.recv(4)
			if len(chunk) < 4:
				break
			slen = struct.unpack('>L', chunk)[0]
			chunk = self.connection.recv(slen)
			while len(chunk) < slen:
				chunk = chunk + self.connection.recv(slen - len(chunk))
			obj = pickle.loads(chunk)
			record = logging.makeLogRecord(obj)
			self.handleLogRecord(record)

	def handleLogRecord(self, record):

		name = record.name
		sefl.addLog(name)
		'''
        # logger = logging.getLogger(name)
        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        # logger.handle(record)

		'''
