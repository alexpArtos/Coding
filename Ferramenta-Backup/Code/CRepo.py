#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Photography Manager

Application to create a consolidated backup of photographs from different sources.

author: Alexandre Pinto
"""

import os
import re

from utils import yesNoQuestion, alert, inputText, getSaveFilename, fileExists
from CRepoItem import CRepositoryItem
from enum import Enum, unique

class CRepository:
	@unique
	class Matches(Enum):
		NEW = 1
		EXISTING = 2
		COPY = 3
		CONFLICT_NEW = 4
		CONFLICT_EXIST = 5

	def __init__(self, name="", location=""):
		self.__name = name
		self.__location = location
		self.repoHashDict = {} # hash --> list of RepoItems
		self.localHashDict = {} # location --> list of RepoItems
		
	def name(self):
		return self.__name
		
	def location(self):
		return self.__location	

	def description(self):
		return "[%s]: %s" % (self.__name, self.__location)
		
	def setName(self, name):
		self.__name = name
		
	def addFile(self, filename):
		repoItem = CRepositoryItem(filename)
		self.__files.append(repoItem)
		
	def writeToFile(self, file):
		repoLocation = self.location()
		for item in self.__files:
			entry = writeLinePattern().format(item.locationRelative(repoLocation), item.hash(), item.size(), item.time(), item.tags())
			file.write(entry)

	def loadFromFile(self):
		filename = self.location()
		print("Loading file {0}".format(filename))	
		file = open(filename, 'r')
		for line in file:					
			m = re.search(CRepository.readLinePattern(), line)
			if (not m is None):
				filename = m.group(1)
				hash = m.group(2)
				size = m.group(3)
				date = m.group(4)
				item = CRepositoryItem(hash, filename, size, date)
				registerItem(item)
		file.close()

	def registerItem(self, repoItem):
		'''Register the item in the repo's dictionaries. 		
			If this item's hash already exists, 
			it adds the item to the list under that hash.
			Otherwise, it creates a new list with this item for that hash 
			There is no need to register the item's location, because we can always test it "on the ground",
			that is, check if there is a file on that path via os calls
		'''
		hash = repoItem.hash()
		if hash in self.repoHashDict.keys():
			itemList = self.repoHashDict[hash]
			itemList.append(repoItem)
		else:
			self.repoHashDict[hash] = [repoItem]				
		
	def analyse(self, path):
		''' This function walks through all files in path,
			and for each of them detects its state in respect to the repository.
			It stores this state in a dictionary keyed by the file name
		'''
		
		# for each file,
		# compute its hash and size
		# obtain all entries with the same hash and size
		# check if there is a file in that location

		print("Analysing path {0}".format(path))
		
		for path, subdirs, files in os.walk(path):
			matches = {}
			for name in files:
				filename = os.path.normpath(os.path.join(path, name))
				(fileSize, fileModified, fileHash) = CRepositoryItem.getDataFile(filename)
						
				(exists, hashList) = self.getHashesIfFileExists(fileHash, fileSize)
				locationIsFree = not fileExists(filename)

			# end for
		# end for
		return matches
					
	def getHashesIfFileExists(self, hash, size):
		''' checks if there is any file in the repository with the same hash and size
		'''
		if (hash in self.repoHashDict):
			hashList = self.repoHashDict[hash]
			filteredHashList = [item for item in hashList if item.size() == size]
			return (len(filteredHashList) > 0, filteredHashList)
		else:
			return (False, [])		
		
	@staticmethod
	def readLinePattern():
		''' regExp describing an entry in the repository file
		'''
		return '"([^"]*)" ([0-9a-f]*), (\d*), ([.0-9]*), [(.*)]'
		
	@staticmethod
	def writeLinePattern():
		''' format string for writing an entry in the repository file
		'''
		return '"{0}" {1}, {2}, {3}, {4}\n'
		
				
	# this returns a regExp pattern that matches a name and location 
	# in a string returned by description()
	@staticmethod
	def descriptionPattern():
		return "\[(.*)\]: (.*)"


		
		
		
		
