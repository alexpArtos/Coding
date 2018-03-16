#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Stats:
	@staticmethod
	def mean(points):
		"""Returns the arithmetic mean of points
		"""
		return sum(points)/len(points)
	
	@staticmethod	
	def median(points):
		"""Returns the median of points
		"""
		N = len(points)
		if (N%2 == 0):			
			leftOfCentre = points[N//2-1]
			rightOfCentre = points[N//2]
			return (leftOfCentre + rightOfCentre) / 2
		else:
			return points[N//2]

	@staticmethod
	def mode(points):
		"""Returns any modal value of this points
		"""
		count = {}
		max = None
		for item in points:
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
			
	@staticmethod
	def weightedMean(points, weights):
		"""Returns the weighted mean of points using weights
		"""
		weightedSum = sum([a*b for a,b in zip(points, weights)])
		totalWeight = sum(weights)
		return weightedSum / totalWeight
		