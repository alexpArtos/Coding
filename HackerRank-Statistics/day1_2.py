#!/usr/bin/python3
# -*- coding: utf-8 -*-

from utils import Utils
from stats import Stats
	
input()
points = map(int,input().split())
freqs = map(int, input().split())
S = Stats.expandPopulation(points, freqs)

S.sort()

Q1 = Stats.Q1(S)
Q3 = Stats.Q3(S)
print(Utils.scale(Q3-Q1, 1))

