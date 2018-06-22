import math
from utils import Utils
from stats import Stats		   
	
mean = 205 * 49
stdDev = 15 * math.sqrt(49)

pLessThan9800 = Stats.normDistCumulative(mean, stdDev, 9800)

print( Utils.scale (pLessThan9800, 4))


