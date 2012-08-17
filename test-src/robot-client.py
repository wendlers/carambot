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
import traceback

from optparse import OptionParser
from rob.client import RobotClient

cli = None

try:

	parser = OptionParser() 

	parser.add_option("-s", "--server", dest="server", 
		help="Robot server IP or hostname", metavar="HOST") 

	parser.add_option("-c", "--clientport", dest="clientport", type="int", 
		help="Robot client port (default 50008)", default=50008, metavar="PORT") 

	parser.add_option("-p", "--port", dest="port", type="int",
		help="Robot server port (default 50007)", default=50007, metavar="PORT") 

 	(options, args) = parser.parse_args()

	if options.server == None:
		print "Missing argument: -s/--server"

	cli		= RobotClient(options.clientport, options.server, options.port)
	cli.run()

except Exception as e:
	if not cli == None:
		del cli

	print traceback.format_exc()

print "DONE"
