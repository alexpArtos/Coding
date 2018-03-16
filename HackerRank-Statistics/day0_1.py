#!/usr/bin/python3
# -*- coding: utf-8 -*-

from utils import Utils
from stats import Stats
	
input()
line = input()
values = line.split()
numbers = [int(i) for i in values]
numbers.sort()

average = Stats.mean(numbers)
median = Stats.median(numbers)
mode = Stats.mode(numbers)

print(Utils.scale(average,1))
print(Utils.scale(median, 1))
print(mode)
