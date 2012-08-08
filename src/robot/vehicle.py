"""
  Vehicle
"""

from device.dcmctl import DualChannelMCtl 

class Vehicle:

	mctl = None

	def __init__(self, dChMCtl):
		self.mctl = dChMCtl

	def fw(self):
		self.mctl.fw(1, 1)

	def bw(self):
		self.mctl.bw(1, 1)

	def br(self):
		self.mctl.br(1, 1)

	def ri(self):
		self.mctl.fw(1, 0)
		self.mctl.bw(0, 1)

	def le(self):
		self.mctl.bw(1, 0)
		self.mctl.fw(0, 1)	

