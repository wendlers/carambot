#! /usr/bin/python

import curses 

from util.cursesscr import CursesScreen
from util.udp import UdpClient, UdpCommException

CLIENT_PORT = 50008

SERVER_IP   = "127.0.0.1"
#SERVER_IP   = "172.16.100.25"
SERVER_PORT = 50007
SEND_TIMEOUT= 1

class CarambotClient(UdpClient, CursesScreen):

	GREEN 	= None
	RED		= None
	BLUE	= None
	YELLOW	= None

	curY = 1

	def __init__(self, bindTo = "", port = CLIENT_PORT):
		CursesScreen.__init__(self)
		UdpClient.__init__(self, bindTo, port)
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

		self.getScreen().addstr("**\n", self.RED)
		self.getScreen().addstr("* Simpe RobotControl. Use the following keys:\n", self.RED)
		self.getScreen().addstr("* - UP \t\tforward\n", self.RED)
		self.getScreen().addstr("* - DOWN\tbackward\n", self.RED)
		self.getScreen().addstr("* - LEFT\tleft\n", self.RED)
		self.getScreen().addstr("* - RIGHT\tright\n", self.RED)
		self.getScreen().addstr("* - SPACE\tbreak\n", self.RED)
		self.getScreen().addstr("* - q\t\tquit\n", self.RED)
		self.getScreen().addstr("**\n\n", self.RED)

		self.curY = 11;

	def run(self):	
		while True:

	 		maxY, maxX = self.getScreen().getmaxyx()

			if self.curY >= maxY:
				self.getScreen().clear()
				self.getScreen().addstr("** screenwrap **\n", self.RED)
				self.curY = 2

			c = self.getScreen().getch()

			self.getScreen().addstr("-> ", self.BLUE)

			req = None

			if c == curses.KEY_UP: 
				self.getScreen().addstr("FORWARD", self.YELLOW)	
				req = { "msgId" : "mv", "dir" : "fw" }
			elif c == curses.KEY_DOWN: 
				self.getScreen().addstr("BACKWARD", self.YELLOW)	
				req = { "msgId" : "mv", "dir" : "bw" }
			elif c == curses.KEY_LEFT: 
				self.getScreen().addstr("LEFT", self.YELLOW)	
				req = { "msgId" : "mv", "dir" : "le" }
			elif c == curses.KEY_RIGHT: 
				self.getScreen().addstr("RIGHT", self.YELLOW)	
				req = { "msgId" : "mv", "dir" : "ri" }
			elif c == ord(' '): 
				self.getScreen().addstr("BREAK", self.YELLOW)	
				req = { "msgId" : "mv", "dir" : "br" }
			elif c == ord('a'): 
				self.getScreen().addstr("PAN-0-DEG", self.YELLOW)	
				req = { "msgId" : "pan", "pos" : 0 }
			elif c == ord('s'): 
				self.getScreen().addstr("PAN-45-DEG", self.YELLOW)	
				req = { "msgId" : "pan", "pos" : 45 }
			elif c == ord('d'): 
				self.getScreen().addstr("PAN-90-DEG", self.YELLOW)	
				req = { "msgId" : "pan", "pos" : 90 }
			elif c == ord('f'): 
				self.getScreen().addstr("PAN-135-DEG", self.YELLOW)	
				req = { "msgId" : "pan", "pos" : 135 }
			elif c == ord('g'): 
				self.getScreen().addstr("PAN-180-DEG", self.YELLOW)	
				req = { "msgId" : "pan", "pos" : 180 }
			elif c == ord('q'): 
				break  # Exit the while()
			else:
				self.getScreen().addstr("UNKNOWN KEY\n", self.RED)	
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

				self.getScreen().addstr(" = " + msg + "\n",col)	
				self.curY = self.curY + 1

	def xfer(self, data):
		self.send(SERVER_IP, SERVER_PORT, data)
		return self.receive(SERVER_IP, SERVER_PORT, SEND_TIMEOUT)

cli = None

try:

	cli = CarambotClient()
	cli.run()

except Exception as e:
	print e
