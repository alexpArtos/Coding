import unittest

import re, sys, os

from PyQt5.QtWidgets import QApplication
from main import CMainWindow
from CRepo import CRepository
from CRepoManager import CRepositoryManager
import utils
import shutil

class TestCRepo(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super(TestCRepo, self).__init__(*args, **kwargs)
		self.hashDict = {}
		self.dirFileCount = 0
		self.defaultLocation = ""

	
	def setUp(self):	
		# store the default location at the start
		if self.defaultLocation == "":
			self.defaultLocation = os.getcwd()
					
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
		return os.path.join(self.defaultLocation, "TestDir")

	def getRepoDirectory(self):
		return os.path.join(self.defaultLocation, "testRepository")
		
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
		# load from repo file 
		repo = self.main.repoManager.repoDict[self.repoFileName()]
		repo.loadFromFile()
		self.assertEqual(12, len(repo.repoHashDict.keys()))		

		keys = ['file1', 'file2', 'file3', 
				r'dirA\fileA1', r'dirA\fileA2', r'dirA\fileA3', 
				r'dirC\file5', r'dirC\fileC1', r'dirC\fileC2',
				r'dirD\file5', r'dirD\file6',
				r'dirZ\dirX\dirW\fileW1', r'dirZ\dirX\dirW\fileY2']
		hashes = [
			'c22dd47bb77cb2f411ede211f28f50b9c8c134b6',
			'07231459bd9aa24caa9870ce32fb02135d95bacc',
			'3e4c81c2cbd2289b627122a4a9059cd485e11f62',
			'fdaa25932715af8a6b95f08d5fd6310ac407a23e',
		    '71542a7339dae015f75f23ba2e65fcb3d3f51675',
		    '6f2b92bec11549e4d87fbccd78586822eca52c4c',
		    'b0b0a88d3b0c4c9b56e20a9b4175002255f1bf57',
			'febf6d6d7a45ba2f87bc738e70fdecfc36d3c631',
			'7c39c710abf61ca9960cbbc7b3aa0967b3f2ca8a',
			'b0b0a88d3b0c4c9b56e20a9b4175002255f1bf57',
			'04b07757062c5bc5ce3c78738c0540960977e64c',
			'1e390eb3b38a1c43ee3498999f5d6678bae4ab9d',
			'c01aba7f6cb5182e1eb128e51a5983b3722e6319']
		sizes = [5,5,5,
				 6,6,6,
				 5,6,6,
				 5,5,
				 6,6]

		for i in range((len(keys))):			
			key = keys[i]
			thishash = hashes[i]
			size = sizes[i]
			repoItem = repo.localRepoDict[key]
			self.assertEqual(key, repoItem.location())
			self.assertEqual(thishash , repoItem.hash())
			self.assertEqual(size, repoItem.size())
			self.assertEqual(1234567890.1115553, repoItem.time())
		
	def verifyMatches(self, matchList, fm, sourceFolder):
		for (path, matchClass, repoList) in matchList:		
			relPath = utils.relativePath(path, sourceFolder)
			self.assertTrue(relPath in fm, "{0} not in fm ({1})".format(relPath, path))
			(expectedMatch, expectedPathlist) = fm[relPath]
			self.assertEqual(expectedMatch, matchClass, "Failed match for {0} - class".format(relPath))
			self.assertEqual(expectedPathlist, [repo.location() for repo in repoList], "Failed match for {0} - path list".format(relPath))
		
		
	def testanalyse(self):						
		''' This analyses a repository and a folder from controlled locations.
			The repository is located at: <dev folder>\testRepository
			and the source directory at: <dev folder>\TestDir.
			the hierarchy in TestDir is plain: it has only 3 sub-directories and these have no children
			testRepoository has only a subset of these, having only one sub-directory
		'''
		print("--- Starting testanalyse ---")
		self.assertIsNotNone(self.main.repoManager)
		repo = self.main.repoManager.loadRepoInMemory(self.repoFileName())
		self.assertIsNotNone(repo, "repository is None")
		
		matchList = repo.analyse(self.getTestDirectory())
		
		self.assertIsNotNone(matchList, "matches is None")
		
		self.assertEqual(self.dirFileCount, len(matchList))
		
		# create association of filenames to type of match	
		# tuple: 
		# 1: match class, 
		# 2: whether there is a file at the corresponding location in the repository, 
		# 3: all the occurrences of this file in the repo
		# The last information is useful to display in a tooltip
		fm = {}
		fm[r"file1"] = (CRepository.Matches.EXISTING, [r"file1"]) 
		fm[r"file2"] = (CRepository.Matches.CONFLICT_NEW, [])
		fm[r"file3"] = (CRepository.Matches.CONFLICT_EXIST, [r"dirA\fileA1"])
		fm[r"file4"] = (CRepository.Matches.NEW, [])
		fm[r"dirA\fileA1"] = (CRepository.Matches.CONFLICT_NEW, [])
		fm[r"dirA\fileA2"] = (CRepository.Matches.EXISTING, [r"dirA\fileA2"]) 
		fm[r"dirB\fileA1"] = (CRepository.Matches.COPY, [r"dirA\fileA1"])
		fm[r"dirB\fileA2"] = (CRepository.Matches.COPY, [r"dirA\fileA2"])
		fm[r"dirC\file4"] = (CRepository.Matches.NEW, [])
		fm[r"dirC\file5"] = (CRepository.Matches.EXISTING, [r"dirC\file5", r"dirD\file5"])
		fm[r"dirC\dirX\dirD\file5"] = (CRepository.Matches.COPY, [r"dirC\file5", r"dirD\file5"])
		fm[r"dirC\dirX\dirD\file6"] = (CRepository.Matches.NEW, [])
		fm[r"dirC\dirX\dirD\dirE\file7"] = (CRepository.Matches.NEW, [])
		fm[r"dirC\dirX\dirD\dirE\file8"] = (CRepository.Matches.NEW, [])
		fm[r"dirY\fileY1"] = (CRepository.Matches.COPY, [r"dirZ\dirX\dirW\fileW1"])
		fm[r"dirY\fileY2"] = (CRepository.Matches.COPY, [r"dirZ\dirX\dirW\fileY2"])
		fm[r"dirY\fileY3"] = (CRepository.Matches.NEW, [])

		self.verifyMatches(matchList, fm, self.getTestDirectory())
				
	def testAnalyseSubFolder1(self):
		''' This demonstrates how we can make analyses based on a sub-folder of a repository
			As arguments, we pass the relative path to the folder inside the repository,
			and the full path of the source folder.
		'''
		print("--- Starting testAnalyseSubFolder: simple dir ---")
		repo = self.main.repoManager.loadRepoInMemory(self.repoFileName())
	
		repoFolder = "dirA"
		sourceSubFolder = os.path.join(self.getTestDirectory(), r"dirA")
		
		matchList = repo.analyseSubFolder(repoFolder, sourceSubFolder)
		
		self.assertIsNotNone(matchList, "matches is None")
			
		# create association of filenames to type of match
		
		fm = {}
		fm[r"fileA1"] = (CRepository.Matches.CONFLICT_NEW, [])
		fm[r"fileA2"] = (CRepository.Matches.EXISTING, [r"dirA\fileA2"])
	
		self.verifyMatches(matchList, fm, sourceSubFolder)

	def testAnalyseSubFolder2(self):
		''' This demonstrates how we can make analyses based on a sub-folder of a repository
			As arguments, we pass the relative path to the folder inside the repository,
			and the full path of the source folder.
		'''
		print("--- Starting testAnalyseSubFolder: deep hierarchy ---")
		repo = self.main.repoManager.loadRepoInMemory(self.repoFileName())
	
		sourceSubFolder = os.path.join(self.getTestDirectory(), r"dirC\dirX\dirD")
		repoFolder = "dirD"
		matchList = repo.analyseSubFolder(repoFolder, sourceSubFolder)
		
		self.assertIsNotNone(matchList, "matches is None")
			
		# create association of filenames to type of match
		
		fm = {}
		fm[r"file5"] = (CRepository.Matches.EXISTING, [r"dirC\file5", r"dirD\file5"]) 
		fm[r"file6"] = (CRepository.Matches.CONFLICT_NEW, [])
		fm[r"dirE\file7"] = (CRepository.Matches.NEW, [])
		fm[r"dirE\file8"] = (CRepository.Matches.NEW, [])

		self.verifyMatches(matchList, fm, sourceSubFolder)
		
	def testAnalyseSubFolder3(self):
		''' This demonstrates how we can make analyses based on a sub-folder of a repository
			As arguments, we pass the relative path to the folder inside the repository,
			and the full path of the source folder.	
		'''
		print("--- Starting testAnalyseSubFolder: deep hierarchy ---")
		repo = self.main.repoManager.loadRepoInMemory(self.repoFileName())
	
		sourceSubFolder = os.path.join(self.getTestDirectory(), "dirY")
		repoFolder = "dirZ\dirX\dirW"
		matchList = repo.analyseSubFolder(repoFolder, sourceSubFolder)
		
		self.assertIsNotNone(matchList, "matches is None")
			
		# create association of filenames to type of match
		
		fm = {}
		fm[r"fileY1"] = (CRepository.Matches.COPY, [r"dirZ\dirX\dirW\fileW1"])
		fm[r"fileY2"] = (CRepository.Matches.EXISTING, [r"dirZ\dirX\dirW\fileY2"])
		fm[r"fileY3"] = (CRepository.Matches.NEW, [])
		
		self.verifyMatches(matchList, fm, sourceSubFolder)		
		
		
	
	def createMasterFile(self):
		os.chdir(self.defaultLocation)
		masterIndex = CRepositoryManager.defaultIndex()
		repo = CRepository("testRepo", self.repoFileName())
		with open(masterIndex, 'w') as file:
			file.write(repo.description() + "\n")

	
	def createDirectoryTree(self):
		directory = self.getTestDirectory()
		# delete directory tree if it exists
		shutil.rmtree(directory, True)
		os.makedirs(directory, 0o777, True)
		self.createFile(directory, r"file1", "hash1", True)
		self.createFile(directory, r"file2", "hash2_", True)
		self.createFile(directory, r"file3", "hashA1", True)
		self.createFile(directory, r"file4", "hash4", True)
		self.createFile(directory, r"dirA\fileA1", "hashA1_", True)
		self.createFile(directory, r"dirA\fileA2", "hashA2", True)
		self.createFile(directory, r"dirB\fileA1", "hashA1", True)
		self.createFile(directory, r"dirB\fileA2", "hashA2", True)
		self.createFile(directory, r"dirC\file4", "hash4", True)
		self.createFile(directory, r"dirC\file5", "hash5", True)
		self.createFile(directory, r"dirC\dirX\dirD\file5", "hash5", True)
		self.createFile(directory, r"dirC\dirX\dirD\file6", "file6", True)
		self.createFile(directory, r"dirC\dirX\dirD\dirE\file7", "hash7", True)
		self.createFile(directory, r"dirC\dirX\dirD\dirE\file8", "hash8", True)
		self.createFile(directory, r"dirY\fileY1", "hashY1", True)
		self.createFile(directory, r"dirY\fileY2", "hashY2", True)
		self.createFile(directory, r"dirY\fileY3", "hashY3", True)
		

	def createRepository(self):
		''' this creates the repository represented by the repo file
		'''
			
		directory = self.getRepoDirectory()
		# remove directory tree if it exists
		shutil.rmtree(directory, True)
		os.makedirs(directory, 0o777, True)
		self.createFile(directory, r"file1", "hash1")
		self.createFile(directory, r"file2", "hash2")
		self.createFile(directory, r"file3", "hash3")
		self.createFile(directory, r"dirA\fileA1", "hashA1")
		self.createFile(directory, r"dirA\fileA2", "hashA2")
		self.createFile(directory, r"dirA\fileA3", "hashA3")
		self.createFile(directory, r"dirC\fileC1", "hashC1")
		self.createFile(directory, r"dirC\fileC2", "hashC2")
		self.createFile(directory, r"dirC\file5", "hash5")
		self.createFile(directory, r"dirD\file5", "hash5")
		self.createFile(directory, r"dirD\file6", "hash6")
		# I don't create dirE so that I can have a missing directory as well, for tests
		self.createFile(directory, r"dirZ\dirX\dirW\fileW1", "hashY1")
		self.createFile(directory, r"dirZ\dirX\dirW\fileY2", "hashY2")
		
		
		self.createRepoFile()

		
	# Auxiliary functions
	def createRepoFile(self):
		directory = self.getRepoDirectory()
		os.makedirs(directory, 0o777, True)
		path = os.path.join (directory, self.repoFileName())
		with open(path, 'w') as repofile:
			repofile.write(r'"file1" {0}, 5, 1234567890.1115553'.format(self.hashDict["hash1"]) + "\n")
			repofile.write(r'"file2" {0}, 5, 1234567890.1115553'.format(self.hashDict["hash2"]) + "\n")
			repofile.write(r'"file3" {0}, 5, 1234567890.1115553'.format(self.hashDict["hash3"]) + "\n")
			repofile.write(r'"dirA\fileA1" {0}, 6, 1234567890.1115553'.format(self.hashDict["hashA1"]) + "\n")
			repofile.write(r'"dirA\fileA2" {0}, 6, 1234567890.1115553'.format(self.hashDict["hashA2"]) + "\n")
			repofile.write(r'"dirA\fileA3" {0}, 6, 1234567890.1115553'.format(self.hashDict["hashA3"]) + "\n")
			repofile.write(r'"dirC\file5" {0}, 5, 1234567890.1115553'.format(self.hashDict["hash5"]) + "\n")
			repofile.write(r'"dirC\fileC1" {0}, 6, 1234567890.1115553'.format(self.hashDict["hashC1"]) + "\n")
			repofile.write(r'"dirC\fileC2" {0}, 6, 1234567890.1115553'.format(self.hashDict["hashC2"]) + "\n")
			repofile.write(r'"dirD\file5" {0}, 5, 1234567890.1115553'.format(self.hashDict["hash5"]) + "\n")
			repofile.write(r'"dirD\file6" {0}, 5, 1234567890.1115553'.format(self.hashDict["hash6"]) + "\n")
			repofile.write(r'"dirZ\dirX\dirW\fileW1" {0}, 6, 1234567890.1115553'.format(self.hashDict["hashY1"]) + "\n")
			repofile.write(r'"dirZ\dirX\dirW\fileY2" {0}, 6, 1234567890.1115553'.format(self.hashDict["hashY2"]) + "\n")
			
		
	def recCreateDir(self, path):
		# print("Recursive create: {0}".format(path))
		if utils.fileExists(path):
			return
		else:
			subDir = os.path.basename(path)
			directory = os.path.dirname(path)
			self.recCreateDir(directory)
			os.chdir(directory)
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
		filehash = utils.hashFile(filename)
		self.hashDict[contents] = filehash 
		if countFile:
			self.dirFileCount = self.dirFileCount + 1
		
		
if __name__ == '__main__':
	unittest.main()
	
