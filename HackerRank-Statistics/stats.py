#!/usr/bin/python3
# -*- coding: utf-8 -*-

from functools import reduce
import math

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

	@staticmethod
	def lowerHalf(vector):
		N = len(vector)
		if (N%2 == 0):
			return vector[0:N//2]
		else:
			return vector[0:N//2]

	@staticmethod
	def upperHalf(vector):
		N = len(vector)
		if (N%2 == 0):
			return vector[N//2:]
		else:
			return vector[N//2+1:]
		
	@staticmethod
	def Q1(vector):
		lower = Stats.lowerHalf(vector)
		return Stats.median(lower)
		
	@staticmethod	
	def Q2(vector):
		return Stats.median(vector)
		
	@staticmethod
	def Q3(vector):
		upper = Stats.upperHalf(vector)
		return Stats.median(upper)
		
	@staticmethod
	def expandPopulation(points, weights):
		return reduce(
			  lambda a,l: a + l, 
			  [[x]*f for x,f in zip(points, weights)], 
			  []
			 )
		
	@staticmethod
	def standardDeviation(points):
		m = Stats.mean(points)
		N = len(points)
		s = sum([(x - m)**2 for x in points])
		return math.sqrt(s / N)
	
	@staticmethod
	def binomDistCumulative(maxX,n,p):
		binom = 1
		pSuc = 1
		pFail = (1-p)**n
		prob = 0
		for x in range(0,maxX+1, 1):
			prob = prob + binom * pSuc * pFail
			pSuc = pSuc * p
			pFail = pFail / (1-p)
			binom = binom * (n-x) / (x+1)
		return prob	
		
	@staticmethod
	def geomDist(p,n):
		q = 1-p
		return q**(n-1) * p
		
	@staticmethod
	def geomDistCumulative(p,n):
		q = 1-p
		return reduce(lambda a,x:
				           a + Stats.geomDist(p,x),					   
					   range(1,n+1),
					   0)

	@staticmethod
	def poissonDist(l,k):
		return math.exp(-l) * l**k / math.factorial(k)

	@staticmethod
	def poissonSquareExpectedValue(l):
		return l**2 + l
		
		
	@staticmethod
	def poissonDistCumulative(l,k):
		return reduce(lambda a,x:
				           a + Stats.poissonDist(l,x),
					   range(0,n+1),
					   0)

	@staticmethod
	def normDistCumulative(mean, stdDev, x):
		return 1/2 * (1 + math.erf((x - mean) / (stdDev * math.sqrt(2))))
	
		