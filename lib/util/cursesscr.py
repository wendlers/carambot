import curses 

class CursesScreen:

	screen = None

	def __init__(self):
		self.screen = curses.initscr()
		curses.noecho()
		curses.cbreak()
		self.screen.keypad(1)

	def __del__(self):
		self.screen.keypad(0)
		curses.nocbreak()
		curses.echo()
		curses.endwin()	

	def getScreen(self):
		return self.screen
