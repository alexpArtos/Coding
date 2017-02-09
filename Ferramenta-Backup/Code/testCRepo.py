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

	hashDict = {}
	dirFileCount = 0
	
	def setUp(self):	
		# create the test directory, and its contents
		self.createDirectoryTree()
		self.createRepository()
		
		# create a master repository file for tests		
		self.createMasterFile()
				
		# start an application to load the repositories
		self.app = QApplication(sys.argv)
		self.main = CMainWindow()		
		
	def tearDown(self):
		# leave the application
		self.app.quit()

		# remove the test directory
		#shutil.rmtree(self.getTestDirectory(), True)
		
			
	
	def repoFileName(self):
		return os.path.join(self.getRepoDirectory(), "testRepo.rpt")
		
	def getTestDirectory(self):
		return os.path.join(utils.defaultLocation(), "TestDir")

	def getRepoDirectory(self):
		return os.path.join(utils.defaultLocation(), "testRepository")
		
	# def testFileExists(self):
	
		# print("testFileExists")
	
		# item11 = CRepositoryItem("dir1\subdir11\fileA", 100, "12-12-2012 00:00", "hash1")
		# item12 = CRepositoryItem("dir2\fileB", 105, "12-12-2012 00:00", "hash1")
		# item13 = CRepositoryItem("dir2\fileC", 100, "12-12-2016 00:30", "hash1")
		# item21 = CRepositoryItem("dir3\fileC", 200, "12-12-2016 00:30", "hash2")
		# item22 = CRepositoryItem("dir3\fileD", 200, "12-12-2016 00:30", "hash2")
		
		# print("test: new repo")
		# repo = 	CRepository()
		# print("test: new repo end")
		
		# self.assertEqual((False, []), repo.getHashesIfFileExists("hash0", 100))
		# self.assertEqual((False, []), repo.getHashesIfFileExists("hash1", 100))
		# self.assertEqual((False, []), repo.getHashesIfFileExists("hash1", 200))
		# self.assertEqual((False, []), repo.getHashesIfFileExists("hash2", 200))

		# print("test: registers")
		
		# repo.registerItem(item11)
		# repo.registerItem(item12)
		# repo.registerItem(item13)
		# repo.registerItem(item21)
		# repo.registerItem(item22)
		
		# print("test: registers end")
		
		# self.assertEqual((False, []), repo.getHashesIfFileExists("hash0", 100))
		# self.assertEqual((True, [item11, item13]), repo.getHashesIfFileExists("hash1", 100))
		# self.assertEqual((False, []), repo.getHashesIfFileExists("hash1", 200))
		# self.assertEqual((True, [item21, item22]), repo.getHashesIfFileExists("hash2", 200))

		# print("end test")

	def testLineParser(self):
		print("--- Starting testLineParser ---")
		line = '"file1" c22dd47bb77cb2f411ede211f28f50b9c8c134b6, 1500, 1480634023.2752092'
		m = re.search(CRepository.readLinePattern(), line)
		
		self.assertIsNotNone(m, "No matches were found")
		self.assertEqual('file1', m.group(1), "Group 1 failed")
		self.assertEqual('c22dd47bb77cb2f411ede211f28f50b9c8c134b6', m.group(2), "Group 2 failed")
		self.assertEqual('1500', m.group(3), "Group 3 failed")
		self.assertEqual('1480634023.2752092', m.group(4), "Group 4 failed")
		self.assertEqual(None, m.group(5), "Group 5 failed")

		
	def testLoadRepository(self):
		print("--- Starting testLoadRepository ---")
		repo = self.main.repoManager.repoDict[self.repoFileName()]
		repo.loadFromFile()
		self.assertEqual(6, len(repo.repoHashDict.keys()))		
				
		repoItem = repo.localRepoDict['file1']
		self.assertEqual('file1', repoItem.location())
		self.assertEqual('c22dd47bb77cb2f411ede211f28f50b9c8c134b6', repoItem.hash())
		self.assertEqual(5, repoItem.size())
		self.assertEqual(1234567890.1115553, repoItem.time())

		
		
	def testanalyse(self):						
		print("--- Starting testanalyse ---")
		self.assertIsNotNone(self.main.repoManager)
		repo = self.main.repoManager.loadRepoInMemory(self.repoFileName())
		self.assertIsNotNone(repo, "repository is None")
		
		matchList = repo.analyse(self.getTestDirectory())
		
		self.assertIsNotNone(matchList, "matches is None")
		
		self.assertEqual(self.dirFileCount, len(matchList))
		
		# create association of filenames to type of match
		
		fm = {}
		fm[r"file1"] = CRepository.Matches.EXISTING
		fm[r"file2"] = CRepository.Matches.CONFLICT_NEW
		fm[r"file3"] = CRepository.Matches.CONFLICT_EXIST
		fm[r"file4"] = CRepository.Matches.NEW
		fm[r"dirA\fileA1"] = CRepository.Matches.CONFLICT_NEW
		fm[r"dirA\fileA2"] = CRepository.Matches.EXISTING
		fm[r"dirB\fileA1"] = CRepository.Matches.COPY
		fm[r"dirB\fileA2"] = CRepository.Matches.COPY
		fm[r"dirC\file4"] = CRepository.Matches.NEW
		fm[r"dirC\file5"] = CRepository.Matches.NEW

		
		for (path, matchClass) in matchList:		
			relPath = utils.relativePath(path, self.getTestDirectory())
			self.assertTrue(relPath in fm, "{0} not in fm ({1})".format(relPath, path))
			expectedMatch = fm[relPath]
			# checks that the match class returned for this item is the expected one
			self.assertEqual(expectedMatch, matchClass, "Failed match for {0}".format(relPath))
				

	def testAnalyseSubFolder(self):
		print("--- Starting testAnalyseSubFolder ---")
		repo = self.main.repoManager.loadRepoInMemory(self.repoFileName())
	
		matchList = repo.analyseSubFolder("dirA", os.path.join(self.getTestDirectory(), "dirA"))
		
		self.assertIsNotNone(matchList, "matches is None")
			
		# create association of filenames to type of match
		
		fm = {}
		fm[r"dirA\fileA1"] = CRepository.Matches.CONFLICT_NEW
		fm[r"dirA\fileA2"] = CRepository.Matches.EXISTING

		
		for (path, matchClass) in matchList:		
			relPath = utils.relativePath(path, self.getTestDirectory())
			self.assertTrue(relPath in fm, "{0} not in fm ({1})".format(relPath, path))
			expectedMatch = fm[relPath]
			# checks that the match class returned for this item is the expected one
			self.assertEqual(expectedMatch, matchClass, "Failed match for {0}".format(relPath))
		
	
	def createMasterFile(self):
		masterIndex = CRepositoryManager.defaultIndex()
		repo = CRepository("testRepo", self.repoFileName())
		with open(masterIndex, 'w') as file:
			file.write(repo.description() + "\n")

	
	def createDirectoryTree(self):
		dir = self.getTestDirectory()
		os.makedirs(dir, 0o777, True)
		self.createFile(dir, r"file1", "hash1", True)
		self.createFile(dir, r"file2", "hash2_", True)
		self.createFile(dir, r"file3", "hashA1", True)
		self.createFile(dir, r"file4", "hash4", True)
		self.createFile(dir, r"dirA\fileA1", "hashA1_", True)
		self.createFile(dir, r"dirA\fileA2", "hashA2", True)
		self.createFile(dir, r"dirB\fileA1", "hashA1", True)
		self.createFile(dir, r"dirB\fileA2", "hashA2", True)
		self.createFile(dir, r"dirC\file4", "hash4", True)
		self.createFile(dir, r"dirC\file5", "hash5", True)

	def createRepository(self):
		''' this creates the repository represented by the repo file
		'''
			
		dir = self.getRepoDirectory()
		os.makedirs(dir, 0o777, True)
		self.createFile(dir, r"file1", "hash1")
		self.createFile(dir, r"file2", "hash2")
		self.createFile(dir, r"file3", "hash3")
		self.createFile(dir, r"dirA\fileA1", "hashA1")
		self.createFile(dir, r"dirA\fileA2", "hashA2")
		self.createFile(dir, r"dirA\fileA3", "hashA3")
		self.createRepoFile()

		
	# Auxiliary functions
	def createRepoFile(self):
		dir = self.getRepoDirectory()
		os.makedirs(dir, 0o777, True)
		path = os.path.join (dir, self.repoFileName())
		with open(path, 'w') as repofile:
			repofile.write(r'"file1" {0}, 5, 1234567890.1115553'.format(self.hashDict["hash1"]) + "\n")
			repofile.write(r'"file2" {0}, 5, 1234567890.1115553'.format(self.hashDict["hash2"]) + "\n")
			repofile.write(r'"file3" {0}, 5, 1234567890.1115553'.format(self.hashDict["hash3"]) + "\n")
			repofile.write(r'"dirA\fileA1" {0}, 6, 1234567890.1115553'.format(self.hashDict["hashA1"]) + "\n")
			repofile.write(r'"dirA\fileA2" {0}, 6, 1234567890.1115553'.format(self.hashDict["hashA2"]) + "\n")
			repofile.write(r'"dirA\fileA3" {0}, 6, 1234567890.1115553'.format(self.hashDict["hashA3"]) + "\n")
		
		

	def createFile(self, path, name, contents, countFile=False):
		filename = os.path.join(path, os.path.normpath(name))
		fileDir = os.path.dirname(filename)
		if not utils.fileExists(fileDir):
			os.mkdir(fileDir)
		with open(filename, 'w') as file:
			file.write(contents)
		hash = utils.hashFile(filename)
		self.hashDict[contents] = hash
		if countFile:
			self.dirFileCount = self.dirFileCount + 1
		
		
if __name__ == '__main__':
    unittest.main()
	
