import math

from utils import Utils

baseMean = 500
baseStdDev = 80
n = 100
mean = baseMean 
stdDev = baseStdDev / math.sqrt(n)
z = 1.96

A = mean - z * stdDev
B = mean + z * stdDev

print( Utils.scale (A, 2))
print( Utils.scale (B, 2))


