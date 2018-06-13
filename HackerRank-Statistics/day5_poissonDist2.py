from utils import Utils
from stats import Stats

CA = 160 + 40 * Stats.poissonSquareExpectedValue(0.88)
CB = 128 + 40 * Stats.poissonSquareExpectedValue(1.55)

print( Utils.scale (CA, 3))
print( Utils.scale (CB, 3))
