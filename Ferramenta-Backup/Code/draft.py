#test.py

#open file

import os
import datetime 
from pathlib import Path
import hashlib

def hashFile(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

	   # loop till the end of the file
	   chunk = 0
	   while chunk != b'':
		   # read only 1024 bytes at a time
		   chunk = file.read(1024)
		   h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()

def defaultLocation():
	return os.getcwd();

def defaultIndex():
	path = os.path.join (defaultLocation(), "MasterRPT.idx")
	if not os.path.exists(path):
		# create file if it does not exist
		file = open(path, 'w')
		file.close()
	return path;
	
def printDefaultAttributes():
	name = defaultIndex()
	stats = os.stat(name)
	print("Size: " + str(stats.st_size))
	date = datetime.datetime.fromtimestamp(stats.st_mtime)
	print("Time: " + datetime.datetime.isoformat(date))
	print("Hash: " + hashFile(name))

def printContents():
	path = defaultIndex()
	print("Path: " + path)
	file = 	open(path, mode="r")
	line = file.readline()
	print ("Line: " + line)	
	print ("All: ")
	all = file.read()
	print ("Read all: " + all)
	file.close()
	
	

if __name__ == '__main__':
	# print ("Default location: " + defaultLocation())
	# print ("Default Index: " + defaultIndex())
	# printDefaultAttributes()
	# printContents()
	d = {}
	d{"a"} = 1
	d{"b"} = 2
	print (d{"a"})
	print (d.has_key(a))