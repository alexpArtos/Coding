#!/usr/bin/python3
# -*- coding: utf-8 -*-

from utils import Utils
from stats import Stats
	
input()
tokens = input().split()
N = len(tokens)
numbers = list(map(int, tokens))
numbers.sort()

Q1 = Stats.Q1(numbers)
Q2 = Stats.Q2(numbers)
Q3 = Stats.Q3(numbers)

print(Utils.scale(Q1,0))
print(Utils.scale(Q2,0))
print(Utils.scale(Q3,0))