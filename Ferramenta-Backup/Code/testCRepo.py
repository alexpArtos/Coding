import unittest

import pdb
import sys, os, shutil

from PyQt5.QtWidgets import QGroupBox, QListView, QWidget, QApplication, QAbstractItemView
from main import CMainWindow
from CRepo import CRepository
from CRepoItem import CRepositoryItem
from CRepoManager import CRepositoryManager
import utils


class TestCRepo(unittest.TestCase):

	hashDict = {}
	dirFileCount = 0
	
	def setUp(self):	
		# create the test directory, and its contents
		self.createDirectoryTree()
		self.createRepoMirror()
		
		
	def tearDown(self):
		# remove the test directory
		shutil.rmtree(self.getTestDirectory(), True)
		
	
	def repoFileName(self):
		return "testRepo.rpt"
		
	def getTestDirectory(self):
		return os.path.join(utils.defaultLocation(), "TestDir")

	def testFileExists(self):
		item11 = CRepositoryItem("dir1\subdir11\fileA", 100, "12-12-2012 00:00", "hash1")
		item12 = CRepositoryItem("dir2\fileB", 105, "12-12-2012 00:00", "hash1")
		item13 = CRepositoryItem("dir2\fileC", 100, "12-12-2016 00:30", "hash1")
		item21 = CRepositoryItem("dir3\fileC", 200, "12-12-2016 00:30", "hash2")
		item22 = CRepositoryItem("dir3\fileD", 200, "12-12-2016 00:30", "hash2")
		
		repo = 	CRepository()
		
		self.assertEqual((False, []), repo.getHashesIfFileExists("hash0", 100))
		self.assertEqual((False, []), repo.getHashesIfFileExists("hash1", 100))
		self.assertEqual((False, []), repo.getHashesIfFileExists("hash1", 200))
		self.assertEqual((False, []), repo.getHashesIfFileExists("hash2", 200))

		repo.registerItem(item11)
		repo.registerItem(item12)
		repo.registerItem(item13)
		repo.registerItem(item21)
		repo.registerItem(item22)
		
		self.assertEqual((False, []), repo.getHashesIfFileExists("hash0", 100))
		self.assertEqual((True, [item11, item13]), repo.getHashesIfFileExists("hash1", 100))
		self.assertEqual((False, []), repo.getHashesIfFileExists("hash1", 200))
		self.assertEqual((True, [item21, item22]), repo.getHashesIfFileExists("hash2", 200))

	def testanalyse(self):	
		# create a master repository file for tests
		self.createMasterFile()
		
		# create a repository file for tests
		self.createRepoFile()

		# start an application to load the repositories
		self.app = QApplication(sys.argv)
		self.main = CMainWindow()		
		
		
		self.assertIsNotNone(self.main.repoManager)
		repo = self.main.repoManager.loadRepoInMemory(self.repoFileName())
		self.assertIsNotNone(repo, "repository is None")
		matchList = repo.analyse(os.getcwd())
		self.assertIsNotNone(matchList, "matches is None")
				
		self.assertEqual(self.dirFileCount, len(matchList))
		
		# create association of filenames to type of match
		
		fm = {}
		fm["file1"] = CRepository.Matches.EXISTING
		fm["file2"] = CRepository.Matches.CONFLICT-NEW
		fm["file3"] = CRepository.Matches.CONFLICT-EXIST
		fm["file4"] = CRepository.Matches.NEW
		fm["dirA\fileA1"] = CRepository.Matches.CONFLICT-NEW
		fm["dirA\fileA2"] = CRepository.Matches.EXISTING
		fm["dirB\fileA1"] = CRepository.Matches.COPY
		fm["dirB\fileA2"] = CRepository.Matches.COPY
		fm["dirC\file4"] = CRepository.Matches.NEW
		fm["dirC\file5"] = CRepository.Matches.NEW
		
		# when using fm[repoItem], here and below, I actually have to replace this by a method that returns the relative path of the item		
		
		for (repoItem, matchClass) in matchlist:		
			path = repoItem.locationRelative(self.getTestDirectory())
			expectedMatch = fm[path]
			# checks that the match class returned for this item is the expected one
			unittest.assertEqual(expectedMatch, matchClass)
				

		# leave the application
		self.app.quit()
		
	# Auxiliary functions
	def createRepoFile(self):
		path = os.path.join (utils.defaultLocation(), self.repoFileName())
		repofile = open(path, 'w')
		repofile.write('"file1" {0}, 1500, 1480634023.2752092\n'.format(self.hashDict["hash1"]))
		repofile.write('"file2" {0}, 1500, 1480634023.2752092\n'.format(self.hashDict["hash2"]))
		repofile.write('"file3" {0}, 1500, 1480634023.2752092\n'.format(self.hashDict["hash3"]))
		repofile.write('"dirA\fileA1" {0}, 1500, 1480634023.2752092\n'.format(self.hashDict["hashA1"]))
		repofile.write('"dirA\fileA2" {0}, 1500, 1480634023.2752092\n'.format(self.hashDict["hashA2"]))
		repofile.write('"dirA\fileA3" {0}, 1500, 1480634023.2752092\n'.format(self.hashDict["hashA3"]))
		repofile.close()
		
	
	def createMasterFile(self):
		masterIndex = CRepositoryManager.defaultIndex()
		file = open(masterIndex, 'w')
		repo = CRepository("testRepo", self.repoFileName())
		file.write(repo.description() + "\n")
		file.close()

	
	
	def createDirectoryTree(self):
		dir = self.getTestDirectory()
		os.makedirs(dir, 0o777, True)
		self.createFile(dir, r"file1", "hash1")
		self.createFile(dir, r"file2", "hash2_")
		self.createFile(dir, r"file3", "hashA1")
		self.createFile(dir, r"file4", "hash4")
		self.createFile(dir, r"dirA\fileA1", "hashA1_")
		self.createFile(dir, r"dirA\fileA2", "hashA2")
		self.createFile(dir, r"dirB\fileA1", "hashA1")
		self.createFile(dir, r"dirB\fileA2", "hashA2")
		self.createFile(dir, r"dirC\file4", "hash4")
		self.createFile(dir, r"dirC\file5", "hash5")

	def createRepoMirror(self):
		''' the purpose of this function is to create a directory that mirrors the contents of the repo file
			so that we can have all the hashes in our dictionary
		'''
		dir = os.path.join(self.getTestDirectory(), r"../origHashes")
		os.makedirs(dir, 0o777, True)
		self.createFile(dir, r"file1", "hash1")
		self.createFile(dir, r"file2", "hash2")
		self.createFile(dir, r"file3", "hash3")
		self.createFile(dir, r"dirA\fileA1", "hashA1")
		self.createFile(dir, r"dirA\fileA2", "hashA2")
		self.createFile(dir, r"dirA\fileA3", "hashA3")
		
		

	def createFile(self, path, name, contents):
		filename = os.path.join(path, os.path.normpath(name))
		fileDir = os.path.dirname(filename)
		if not utils.fileExists(fileDir):
			os.mkdir(fileDir)
		file  = open(filename, 'w')		
		file.write(contents)
		file.close()
		hash = utils.hashFile(filename)
		self.hashDict[contents] = hash
		self.dirFileCount = self.dirFileCount + 1
		
		
if __name__ == '__main__':
    unittest.main()
	
