#!/usr/bin/python3
# -*- coding: utf-8 -*-

from utils import Utils
from stats import Stats
    
N = input()
values1 = input().split()
values2 = input().split()
points = [int(i) for i in values1]
weights = [int(i) for i in values2]

wMean = Stats.weightedMean(points, weights)   

print(Utils.scale(wMean,1))
