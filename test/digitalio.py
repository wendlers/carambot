#!/usr/bin/python

from io.digital import Pin, PinIn, PinOut, DigitalIO

try:
	io = DigitalIO()
	pi = io.getInput(7)
	po = io.getOutput(8)

	pi.state()
	po.state()

	po.toggle()
	po.state()

except Exception as e:
	print e
