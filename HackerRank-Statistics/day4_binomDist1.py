#!/usr/bin/python3
# -*- coding: utf-8 -*-

from stats import Stats
from utils import Utils

boysWeight = 1.09
girlsWeight = 1.0
probBoy =  boysWeight / (boysWeight + girlsWeight)

print (Utils.scale( 1 - Stats.binomDistCumulative(2,6,probBoy), 3))
