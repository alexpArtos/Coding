import math
from utils import Utils
from stats import Stats		   

mean = 2.4 * 100
stdDev = 2.0 * math.sqrt(100)

pSuccess = Stats.normDistCumulative(mean, stdDev, 250)

print( Utils.scale (pSuccess, 4))


