import os
from pathlib import Path
import utils

class CRepositoryItem:
	def __init__(self, location="", size="", modified=None, hash="", tags=[]):
		self.__location = location
		self.__size = size
		self.__modified = modified
		self.__hash = hash
		self.__tags = tags
		
	
	@classmethod	
	def fromFile(self, filename):
		self.__location = filename
		(self.__size, self.__modified, self.__hash) = utils.getDataFile(filename)
		
	def location(self):
		return self.__location
		
	def locationRelative(self, repoLocation):
		return utils.relativePath(self.location(), os.path.dirname(repoLocation))	
	
	def hash(self):
		return self.__hash
		
	def size(self):
		return self.__size
		
	def time(self):
		return self.__modified
		
	def tags(self):
		return self.__tags
		