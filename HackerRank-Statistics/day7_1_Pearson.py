import math

from stats import Stats
from utils import Utils

_ = input("Size of variables: ") 
X = Utils.readFloatsLine("Enter X: ")
Y = Utils.readFloatsLine("Enter Y: ")

pcc = Stats.PearsonCC(X,Y)
print (Utils.scale(pcc,3))