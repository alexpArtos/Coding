#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Photography Manager

Application to create a consolidated backup of photographs from different sources.

author: Alexandre Pinto
"""

import pdb
import sys, os

from PyQt5.QtGui import QStandardItemModel

from controls import *
from CRepoManager import CRepositoryManager
from CTreeItem import TreeItem
from CTreeModel import TreeModel
from PyQt5.QtWidgets import QGroupBox, QListView, QWidget, QApplication, QAbstractItemView, QTreeView

class CMainWindow(QWidget):
	def __init__(self):
		super().__init__()
			
		self.__createUI()
		self.__initializeStructures()
		self.__setUIBehaviour()
		self.repoManager.loadRepositories()
		self.__selectedRepo = None

	def __createUI(self):
		# ---------------- UI ----------------------
		self.setGeometry(600, 30, 800, 800)
		self.setWindowTitle("Files Locations")

		# ---------------- Variables ------------------------
		defaultSource = os.path.dirname(os.getcwd())
		
		# Define left-side controls
		self.box1 = QGroupBox('Files source', self)
		self.box1.setGeometry(10, 10, 340, 100)
		self.txtSource = CDirText("Origin Directory", defaultSource, self.box1)
		self.txtSource.setGeometry(10,20,300,20)
		
		self.btnAnalyse = QPushButton("Analyse", self)
		self.btnAnalyse.setGeometry(50, 120,250, 20)
		
		# Define right-side controls
		self.box2 = QGroupBox('Repositories', self)
		self.box2.setGeometry(380,10,400,500)

		self.lstRepos = QListView(self.box2)
		self.lstRepos.ViewMode = QListView.ListMode
		self.lstRepos.setGeometry(10,50,385,200)
		self.lstRepos.setSelectionMode(QAbstractItemView.MultiSelection)
		
		self.btnCreateRepo = QPushButton("New Repository", self.box2)
		self.btnCreateRepo.setGeometry(10, 20, 125,20)
			
		self.btnRepairRepo = QPushButton("Repair Repository", self.box2)
		self.btnRepairRepo.setGeometry(140, 20, 125,20)

		self.btnRemoveRepo = QPushButton("Remove Repository", self.box2)
		self.btnRemoveRepo.setGeometry(270, 20, 125,20)
		
		self.txtRepo = CTextWithLabel("Selected Repository", "", self.box2)
		self.txtRepo.setGeometry(10,250,385,20)	
		
		# Define experiment Tree View
		self.treeView = QTreeView(self)	
		
		item0 = TreeItem([r"Source", "Action", r"Target"])
		
		standardModel = TreeModel(item0)
		self.treeView.setModel(standardModel)
		
		item1 = TreeItem([r"Path 1\File1", False, r"PathA\File1"])
		item2 = TreeItem([r"Path 1\File2", False, r"PathA\File2"])
		item0.appendChild(item1)
		item0.appendChild(item2)
		
		print standardModel.rowCount()
		print standardModel.columnCount()

		
		
	def __initializeStructures(self):
		# create repository manager
		self.repoManager = CRepositoryManager(self)

		# set view model
		repoModel = QStandardItemModel()
		self.lstRepos.setModel(repoModel)
		self.repoManager.setModel(repoModel)		
	
	def __setUIBehaviour(self):
		# Handle list selection
		self.lstRepos.selectionModel().selectionChanged.connect(self.__selectRepo)
		
		# Handle New Repository: create repository for a given location
		self.btnCreateRepo.clicked.connect(self.repoManager.createRepo)
		
		# Handle Repair Repository: recreate the repository at a given location
		self.btnRepairRepo.clicked.connect(self.__handleRepairRepo)
		
		# Handle Remove Repository
		self.btnRemoveRepo.clicked.connect(self.__handleRemoveRepo)
		
		# Handle Analyse button
		self.btnAnalyse.clicked.connect(self.__handleAnalyse)
		
	# redefine handling of close event
	def closeEvent(self, event):
		self.repoManager.saveRepositories()
		event.accept()				

	# find what repos are currently selected
	def __getSelectedRepos(self):
		# obtain selection		
		indexes = self.lstRepos.selectionModel().selectedIndexes()		
		if len(indexes) == 0:
			# if none are selected, do nothing
			return []

		model = self.lstRepos.model()
		repos = [model.itemFromIndex(indexes[i]).data()	for i in range(0, len(indexes))]
		return repos
		
	# remove any selected repos
	def __handleRepairRepo(self):		
		repos = self.__getSelectedRepos()
		for repo in repos:	
			self.repoManager.repairRepo(repo)

	# remove any selected repos
	def __handleRemoveRepo(self):		
		repos = self.__getSelectedRepos()
		for repo in repos:	
			self.repoManager.removeRepo(repo)
	
	def __selectRepo(self, selected, deselected):
		indexes = selected.indexes()
		model = self.lstRepos.model()
		if len(indexes) > 0:
			repo = model.itemFromIndex(indexes[0]).data()	
			self.__selectedRepo = repo
			self.txtRepo.setText(repo.description())
			self.txtRepo.setToolTip(repo.description())			
		else: 
			self.txtRepo.setText("")
			self.txtRepo.setToolTip("")
			
	def __handleAnalyse(self):
		''' This function makes the analysis between the selected repository and the source directory
			It should then open a window to present the results
			These should be placed in a model, similarly to what we do with repositories, albeit a much more complex one
						
			Before we create the comparison model, we load the repository into memory and organize the structures for searches.
		'''		
		if self.__selectedRepo == None:
			print("No repository selected")
			return
		# this does not feel right. The structures for organizing CRepoItem should be inside the corresponging CRepository,
		# and not in the RepoManager: it has nothing to do with this, and we should not have to worry with erasing these structures when we change repository
		repo = self.repoManager.loadRepoInMemory(self.__selectedRepo.location())		
		
		# after we have the repository loaded and indexed,
		# we need to walk through the folder 
		# and compute its status within the repository
		matches = repo.analyse(self.txtSource.tetx())
		
		displayMatchResults(matches)
	
if __name__ == '__main__':
    
	app = QApplication(sys.argv)
	main = CMainWindow()
	main.show()	
	sys.exit(app.exec_())