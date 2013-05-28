#!/usr/bin/env python

##
# This file is part of the uSherpa Python Library project
#
# Copyright (C) 2012 Stefan Wendler <sw@kaltpost.de>
#
# The uSherpa Python  Library is free software; you can redistribute 
# it and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  uSherpa Python Library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
# 
#  You should have received a copy of the GNU Lesser General Public
#  License along with the JSherpa firmware; if not, write to the Free
#  Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
#  02111-1307 USA.  
##

'''
uSherpa Python Library setup-script. To install this library use: 

  sudo python setup.py install  

'''

import os
import shutil

from distutils.core import setup

setup(name='carambot',
	version='0.2',
	description='carambot',
	long_description='Smiple robot using uSherpa as a basis',
	author='Stefan Wendler',
	author_email='sw@usherpa.org',
	url='http://www.usherpa.org/',
	license='LGPL 2.1',
	platforms=['Linux'],
	package_dir = {'': 'src'},
	packages = ['ubot', 'ubot.device', 'ubot.rob', 'ubot.util'],
	requires = ['serial(>=2.4)', 'usherpa(>=0.1)']
)

# install wrapper scripts 
base   = "/usr/local/bin"
server = "%s/carambot-srv" % base
client = "%s/carambot-cli" % base

try:
	shutil.copyfile("./bin/carambot-srv", server)
	os.chmod(server, 0755)
except:
	pass

try:
	shutil.copyfile("./bin/carambot-cli", client)
	os.chmod(client, 0755)
except:
	pass

