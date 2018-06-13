from stats import Stats		   
from utils import Utils
	
mean = 70
stdDev = 10 

pMoreThan80 = 1 - Stats.normDistCumulative(mean, stdDev, 80)
pPassed = 1 - Stats.normDistCumulative(mean, stdDev, 60)
pFailed = Stats.normDistCumulative(mean, stdDev, 60)

print( Utils.scale (pMoreThan80*100, 2))
print( Utils.scale (pPassed*100, 2))
print( Utils.scale (pFailed*100, 2))
