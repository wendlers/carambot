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

VERSION="Carambot Server v0.1"

import traceback
import logging
import logging.handlers

from optparse import OptionParser

from rob.carambot 	import Robot
from rob.server 	import RobotServer

srv = None

try:
	parser = OptionParser() 

	parser.add_option("-p", "--port", dest="port", type="int",
		help="Robot server port (default 50007)", default=50007, metavar="PORT") 

	parser.add_option("-c", "--logclient", dest="logclient",
		help="Client name/ip for remote logging", metavar="HOST") 

	parser.add_option("-s", "--serialport", dest="serialport", 
		help="uSherpa serial port (default /dev/ttyS0)", default="/dev/ttyS0", metavar="PORT") 

	parser.add_option("-v", "--verbose", dest="verboselevel", type="int",
		help="Verbose level for logging (10: DEBUG, 50: CRITICAL)", default=20, metavar="LEVEL") 

 	(options, args) = parser.parse_args()

	logging.basicConfig(level=options.verboselevel)

	# add remote log client (if requested)
	if not options.logclient == None:
		socketHandler = logging.handlers.SocketHandler(options.logclient, logging.handlers.DEFAULT_TCP_LOGGING_PORT)
		rootLogger = logging.getLogger()
		rootLogger.addHandler(socketHandler)

	logging.info(VERSION)
	logging.info("uSherpa and Carambot rocking the wheels!")

	rob 	= Robot(options.serialport)
	srv		= RobotServer(rob, options.port)

	srv.run()

except Exception as e:
	logging.error(`e` + "::" + e.__str__())
finally:
	if not srv == None:
		srv.end()
