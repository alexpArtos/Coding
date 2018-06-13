#!/usr/bin/python3
# -*- coding: utf-8 -*-

from utils import Utils
from stats import Stats

pReject = 0.12
n = 10

pNoMoreThan2 = Stats.binomDistCumulative(2,n,pReject)
pAtLeast2 = 1 - Stats.binomDistCumulative(1,n,pReject)

print( Utils.scale (pNoMoreThan2, 3))
print( Utils.scale (pAtLeast2, 3))