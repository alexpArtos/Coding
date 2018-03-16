#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Stats:
	@staticmethod
	def mean(vector):
		return sum(vector)/len(vector)
	
	@staticmethod
	def median(vector):
		N = len(vector)
		if (N%2 == 0):			
			leftOfCentre = vector[N//2-1]
			rightOfCentre = vector[N//2]
			return (leftOfCentre + rightOfCentre) / 2
		else:
			return vector[N//2]

	@staticmethod
	def mode(vector):
		"""Returns any modal value of this vector
		"""
		count = {}
		max = None
		for item in vector:
			if item in count:
				count[item] = count[item] + 1
			else:
				count[item] = 1
			if max is None:
				max = (item, 1)
			else:
				if count[item] > max[1]:
					max = (item, count[item])
		return max[0]
			