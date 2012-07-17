#!/usr/bin/python

import curses 

from util.cursesscr import CursesScreen
from io.digital import DigitalIO
from device.dcmctl import MCtlChannel, DualChannelMCtl 
from robot.vehicle import Vehicle

cs = None

try:
	cs = CursesScreen()

	curses.start_color()
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
 
	GREEN 	= curses.color_pair(1)
	RED		= curses.color_pair(2)
	BLUE	= curses.color_pair(3)

	cs.getScreen().addstr("**\n", RED)
	cs.getScreen().addstr("* Simpe RobotControl. Use the following keys:\n", RED)
	cs.getScreen().addstr("* - UP \t\tforward\n", RED)
	cs.getScreen().addstr("* - DOWN\tbackward\n", RED)
	cs.getScreen().addstr("* - LEFT\tleft\n", RED)
	cs.getScreen().addstr("* - RIGHT\tright\n", RED)
	cs.getScreen().addstr("* - SPACE\tbreak\n", RED)
	cs.getScreen().addstr("* - q\t\tquit\n", RED)
	cs.getScreen().addstr("**\n\n", RED)

	cur_y = 11;

	io = DigitalIO()

	mch1 = MCtlChannel(io.getOutput(7), io.getOutput(8))
	mch2 = MCtlChannel(io.getOutput(9), io.getOutput(10))
	mctl = DualChannelMCtl(mch1, mch2)
	veh  = Vehicle(mctl)

	while True:

 		max_y, max_x = cs.getScreen().getmaxyx()

		if cur_y >= max_y:
			cs.getScreen().clear()
			cs.getScreen().addstr("** screenwrap **\n", RED)
			cur_y = 2

		c = cs.getScreen().getch()

		cs.getScreen().addstr("-> ", BLUE)

		if c == curses.KEY_UP: 
			cs.getScreen().addstr("FORWARD\n", GREEN)	
			cur_y = cur_y + 1
			veh.fw()
		elif c == curses.KEY_DOWN: 
			cs.getScreen().addstr("BACKWARD\n", GREEN)	
			cur_y = cur_y + 1
			veh.bw()
		elif c == curses.KEY_LEFT: 
			cs.getScreen().addstr("LEFT\n", GREEN)	
			cur_y = cur_y + 1
			veh.le()
		elif c == curses.KEY_RIGHT: 
			cs.getScreen().addstr("RIGHT\n", GREEN)	
			cur_y = cur_y + 1
			veh.ri()
		elif c == ord(' '): 
			cs.getScreen().addstr("BREAK\n", GREEN)	
			cur_y = cur_y + 1
			veh.br()
		elif c == ord('q'): 
			break  # Exit the while()

except Exception as e:
	del cs
	print e

