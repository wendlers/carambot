Carambot
========

(c) 2012 Stefan Wendler
sw@kaltpost.de
http://gpio.kaltpost.de/

Introduction
------------

Python script for 8devices Carambola SoC to drive a 4-wheel robot remotely and autonomous. 
The script uses uSherpa to communicate with a MSP430G2553 microcontroller connected to the 
Carambola through the serial line on "/dev/ttyS0". The MSP430 is respinsible to operate 
the motor controller, the pan-servo, the ultrasonic range finder and the wheel encoders. 

The Carambola in this setup provides connectivity through its build in WiFi, and also allows 
to stream a live video from a webcam connected to the Carambolas USB port. An other
reason for the Carambola is, that it is afordable, but strong enough to run Python.  

As mentioned before, the purpose of this example setup is to demonstrate how one could "backpack"
a microcontroller to a stronger CPU (here the MIPS based Carambola SoC), and easily integrate it
through uSherpa firmware on the microcontrolle, and uShpera Python API on the SoC.   

Both, this demo project, and the uSherpa project are currently work in progress, and are far 
from complete right now. 

For more information follow the links below:

* [Carambola] (http://www.8devices.com/)
* [uSherpa webpage] (http://usherpa.org/?page_id=1267)
* [uSherpa firmware at git] (https://github.com/wendlers/usherpa-firmware)
* [uSherpa Python API at git] (https://github.com/wendlers/usherpa-pysherpa) 


Project Directory Layout
------------------------

TODO


Prerequisites
-------------

* To use the library, the pyserial library has to be installed. 
* A MCU (currently the TI Launchpad with MSP430G2553) with uSherpa firmware flashed.

For details see the uSherpa [firmware documentation] 
(https://github.com/wendlers/usherpa-firmware/tree/master/doc).  


Schematics
----------

TODO


Install Carambot
----------------
TODO


Use Carambot Server
-------------------

TODO


Use Carambot Client
-------------------

TODO

