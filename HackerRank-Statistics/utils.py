#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Utils:
	@staticmethod
	def scale(n, scale):
		"""Returns n with a number of decimal places equal to scale, after rounding.
		"""
		formatMask = "{:0." + str(scale) + "f}"
		return formatMask.format(n)
				
