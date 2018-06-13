from stats import Stats					   
from utils import Utils
	
mean = 20 
stdDev = 2 

pLess19_5 = Stats.normDistCumulative(mean, stdDev, 19.5)
pBetween22_20 = Stats.normDistCumulative(mean, stdDev, 22) - Stats.normDistCumulative(mean, stdDev, 20)

print( Utils.scale (pLess19_5, 3))
print( Utils.scale (pBetween22_20, 3))
