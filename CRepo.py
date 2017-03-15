#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Photography Manager

Application to create a consolidated backup of photographs from different sources.

author: Alexandre Pinto
"""

import os
import re

import utils
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

	class RepoPath(Enum):
		FREE = 1 # represents a situation where a given path does not exist in the repo
		EQUAL = 2 # represents a situation where a given path represents the same file in the repo
		DIFFERENT = 3 # represents a situation where a given path represents a different file in the repo
		
		
	def __init__(self, name="", location=""):
		self.__name = name
		self.__location = location
		self.repoHashDict = {} # hash --> list of RepoItems
		self.localRepoDict = {} # location --> list of RepoItems
		
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
		file = open(filename, 'r')
		for line in file:					
			m = re.search(CRepository.readLinePattern(), line)
			if (not m is None):
				filename = m.group(1)
				hash = m.group(2)
				size = int(m.group(3))
				date = float(m.group(4))
				item = CRepositoryItem(filename, size, date, hash)			
				self.registerItem(item)
		file.close()

	def itemPath(self, repoItem):
		return repoItem.locationRelative(self.location())
	
		
	def registerItem(self, repoItem):
		'''Register the item in the repo's dictionaries. 		
			If this item's hash already exists, 
			it adds the item to the list under that hash.
			Otherwise, it creates a new list with this item for that hash 
			Remember a repository items's location is already relative
		'''
		hash = repoItem.hash()
		if hash in self.repoHashDict.keys():
			itemList = self.repoHashDict[hash]
			itemList.append(repoItem)			
		else:
			self.repoHashDict[hash] = [repoItem]				
		
		path = repoItem.location()
		if path not in self.localRepoDict.keys():
			self.localRepoDict[path] = repoItem
		else:
			raise KeyError("Duplicate key: " + path)
		
	def analyseSubFolder(self, repoSubPath, basepath):
		# for each file,
		# compute its hash and size
		# obtain all entries with the same hash and size
		# check if there is a file in that location

		print("Analysing path {0} for repository sub-folder {1}".format(basepath, repoSubPath))
		matches = []
		for path, subdirs, files in os.walk(basepath):			
			for name in files:
				filename = os.path.normpath(os.path.join(path, name))
				# obtains relative of filename inside basepath.
				relpath = utils.relativePath(filename, basepath)
				(fileSize, fileModified, fileHash) = utils.getDataFile(filename)
						
				(exists, hashList) = self.getHashesIfFileExists(fileHash, fileSize)
				# checks if this file exists in the repository.
				# it does this by looking at the relative path of the file from the repository's root
				repoPath = os.path.join(repoSubPath, relpath)
				locationType = self.matchFilepathInRepo(repoPath, hashList)
				
				
				if not exists:
					if locationType == CRepository.RepoPath.FREE:
						category = CRepository.Matches.NEW
					else:
						category = CRepository.Matches.CONFLICT_NEW
				else:
					if locationType == CRepository.RepoPath.FREE:
						category = CRepository.Matches.COPY
					elif locationType == CRepository.RepoPath.EQUAL:
						category = CRepository.Matches.EXISTING
					elif locationType == CRepository.RepoPath.DIFFERENT:
						category = CRepository.Matches.CONFLICT_EXIST
				matches.append((filename, category, hashList))
			# end for
		# end for
		return matches
		
		
	def analyse(self, basepath):
		''' This function walks through all files in path,
			and for each of them detects its state in respect to the repository.
			It stores this state in a dictionary keyed by the file name
		'''
	
		print("Analysing path {0}".format(basepath))
		return self.analyseSubFolder("", basepath)
		
					
	def matchFilepathInRepo(self, path, hashList):
		''' returns a member of RepoPath comparing path in the repo and in the file system
			hashList must contain a list of the files in the repo that match 
			the file represented by path in the file system (same hash and size).
		'''
		if path in self.localRepoDict:
			# there is a file at this location in the repository
			repoItem = self.localRepoDict[path]
			# if this file is a copy of the filesystem version, then it must be in hashList
			if repoItem in hashList:
				return self.RepoPath.EQUAL
			else:
				return self.RepoPath.DIFFERENT
		else:
			return self.RepoPath.FREE
					
	def getHashesIfFileExists(self, hash, size):
		''' checks if there is any file in the repository with the same hash and size
		'''
		if (hash in self.repoHashDict):
			hashList = self.repoHashDict[hash]
			filteredHashList = [item for item in hashList if item.size() == size]
			result = (len(filteredHashList) > 0, filteredHashList)
		else:
			result = (False, [])		
		
		return result
		
	@staticmethod
	def readLinePattern():
		''' regExp describing an entry in the repository file
		'''
		return '"([^"]*)" ([0-9a-f]*), (\d*), ([.0-9]*)(, [(.*)])?'
		
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


		
		
		
		
