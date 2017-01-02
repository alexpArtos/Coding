import unittest

import pdb
import sys, os

from PyQt5.QtWidgets import QGroupBox, QListView, QWidget, QApplication, QAbstractItemView
from main import *
from CRepo import *


class TestMain(unittest.TestCase):

	def setUp(self):
		self.createMasterFile()
		
		self.app = QApplication(sys.argv)
		self.main = CMainWindow()		

		
	def tearDown(self):
		self.app.quit()

	def createMasterFile(self):
		masterIndex = CRepositoryManager.defaultIndex()
		file = open(masterIndex, 'w')
		repo = CRepository("testRepo", "testRel.rpt")
		file.write(repo.description() + "\n")
		file.close()
		

	# def testStartUp(self):
		# app = QApplication(sys.argv)
		# main = CMainWindow()		
		# main.txtSource = "teste"
		# main.btnAnalyse.click()

		
	def testanalyse(self):	
		self.assertIsNotNone(self.main.repoManager)
		repo = self.main.repoManager.loadRepoInMemory("testRel.rpt")
		self.assertIsNotNone(repo, "repository is None")
		matches = repo.analyse(os.getcwd())
		self.assertIsNotNone(matches, "matches is None")
		

if __name__ == '__main__':
    unittest.main()
