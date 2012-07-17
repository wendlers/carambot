#!/usr/bin/python

from time import sleep 

from io.digital import DigitalIO
from device.dcmctl import MCtlChannel, DualChannelMCtl 


try:
	io = DigitalIO()

	mch1 = MCtlChannel(io.getOutput(7), io.getOutput(8))
	mch2 = MCtlChannel(io.getOutput(9), io.getOutput(10))
	mctl = DualChannelMCtl(mch1, mch2)

	print "FORWARD - both"
	mctl.fw(1, 1)	# forward both motors
	sleep(2)
	mctl.br(1, 1)	# break both motors

	print "BACKWARD - both"
	mctl.bw(1, 1)	# backward both motors
	sleep(2)
	mctl.br(1, 1)	# break both motors

	print "FORWARD - ch1"
	mctl.fw(1, 0)	# forward channel 1
	sleep(2)
	mctl.br(1, 1)	# break both motors

	print "FORWARD - ch2"
	mctl.fw(0, 1)	# forward channel 2
	sleep(2)
	mctl.br(1, 1)	# break both motors

	print "BACKWARD - ch1"
	mctl.bw(1, 0)	# backward channel 1
	sleep(2)
	mctl.br(1, 1)	# break both motors

	print "BACKWARD - ch2"
	mctl.bw(0, 1)	# backward channel 2
	sleep(2)
	mctl.br(1, 1)	# break both motors

except Exception as e:
	print e
