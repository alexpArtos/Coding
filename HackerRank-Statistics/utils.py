#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Utils:
	@staticmethod
	def scale(n, scale):
		"""Returns n with a number of decimal places equal to scale, after rounding.
		"""
		formatMask = "{:0." + str(scale) + "f}"
		return formatMask.format(n)
				
	@staticmethod
	def readFloatsLine(message):
		tokens = input(message).split(" ")
		floatTuples = [Utils.tryParseFloat(s) for s in tokens]
		return [value for (value, valid) in floatTuples if valid]	
		
	@staticmethod
	def tryParseFloat(s):
		try:
			return(float(s), True)
		except:
			return(None, False)
	