import unittest

import pdb
import re, sys, os, shutil

from PyQt5.QtWidgets import QGroupBox, QListView, QWidget, QApplication, QAbstractItemView
from main import CMainWindow
from CRepo import CRepository
from CRepoItem import CRepositoryItem
from CRepoManager import CRepositoryManager
import utils


class TestCRepo(unittest.TestCase):

	def recCreateDir(self, path):
		# print("Recursive create: {0}".format(path))
		if utils.fileExists(path):
			return
		else:
			subDir = os.path.basename(path)
			dir = os.path.dirname(path)
			self.recCreateDir(dir)
			os.chdir(dir)
			os.mkdir(subDir)	

	def createFile(self, path, name, contents, countFile=False):
		filename = os.path.join(path, os.path.normpath(name))
		fileDir = os.path.dirname(filename)
		# print("=========== CREATE FILE ================")
		# print(filename)
		# print("Base: {0}\nFile: {1}".format(os.path.dirname(filename), os.path.basename(filename)))
		self.recCreateDir(fileDir)
		with open(filename, 'w') as file:
			file.write(contents)
		hash = utils.hashFile(filename)
		self.hashDict[contents] = hash
		if countFile:
			self.dirFileCount = self.dirFileCount + 1

	def getTestDirectory(self):
		return os.path.join(utils.defaultLocation(), "TestDir")
			
	def testCreateFile(self):
		dir = self.getTestDirectory()
		pdb.set_trace()
		self.createFile(dir, r"dirC\dirX\dirD\file5", "hash5", True)
		

if __name__ == '__main__':
    unittest.main()
	
