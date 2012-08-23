Carambot
========

(c) 2012 Stefan Wendler
sw@kaltpost.de
http://gpio.kaltpost.de/


Introduction
------------

Python script for 8devices Carambola SoC to drive a 4-wheel robot remotely and autonomous. 
The script uses uSherpa to communicate with a MSP430G2553 micro-controller connected to the 
Carambola through the serial line on "/dev/ttyS0". The MSP430 is responsible to operate 
the motor controller, the pan-servo, the ultrasonic range finder and the wheel encoders. 

The Carambola in this setup provides connectivity through its build in WiFi, and also allows 
to stream a live video from a web-cam connected to the Carambola USB port. An other
reason for the Carambola is, that it is affordable, but strong enough to run Python.  

As mentioned before, the purpose of this example setup is to demonstrate how one could "backpack"
a micro-controller to a stronger CPU (here the MIPS based Carambola SoC), and easily integrate it
through uSherpa firmware on the micro-controller, and uSherpa Python API on the SoC.   

Both, this demo project, and the uSherpa project are currently work in progress, and are far 
from complete right now. 

For more information follow the links below:

* [Carambola] (http://www.8devices.com/)
* [uSherpa web-page] (http://usherpa.org/?page_id=1267)
* [uSherpa firmware at git] (https://github.com/wendlers/usherpa-firmware)
* [uSherpa Python API at git] (https://github.com/wendlers/usherpa-pysherpa) 


Project Directory Layout
------------------------

* `bin`				Some wrapper-scripts to start the robot client/server 
* `LICENSE`			The license file
* `MANIFEST.in`		Manifest for distribution
* `README.md`		This README
* `setenv.sh`		Set PYTHONPATH for testing
* `setup.py`		Setup script to install/distribute
* `src`				Sources of this library
* `test-src`		Some test/example sources


Prerequisites
-------------

* To use the library, the pyserial library has to be installed. 
* A MCU (currently the TI Launchpad with MSP430G2553) with uSherpa firmware flashed.

For details see the uSherpa [firmware documentation] (https://github.com/wendlers/usherpa-firmware/tree/master/doc).  


Schematics
----------

TODO


Install Carambot
----------------

No installation is needed. The robot client and server could be run directly from 
the project directory.


Use Carambot Server
-------------------

From the top-level project directory, start the server with the following command:

	./bin/carambot-srv 

This assumes, that the MSP430 is connected to "/dev/ttyS0". If you like to enable 
remote logging to a client (carambot-cli) running e.g. on IP 192.168.1.2, use the 
following command:

	./bin/carambot-srv -c 192.168.1.2

For a list of all available command line options issue the following:
 
	./bin/carambot-srv -h


Use Carambot Client
-------------------

To connect the carambot curses client to a server instance, the following has to
be issued (if your server runs on IP 192.168.1.3):

	./bin/carambot-cli -s 192.168.1.3

For a list of all available command line options issue the following:
 
	./bin/carambot-cli -h


