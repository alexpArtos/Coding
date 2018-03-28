#!/usr/bin/python3
# -*- coding: utf-8 -*-

from utils import Utils
from stats import Stats
	
input()
numbers = list(map(int,input().split()))

stdev = Stats.standardDeviation(numbers)

print(Utils.scale(stdev, 1))
