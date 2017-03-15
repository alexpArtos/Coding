from CTreeItem import TreeItem
from CTreeModel import TreeModel

from PyQt5.QtWidgets import QWidget, QTreeView, QApplication
from PyQt5.QtCore import QModelIndex
import os, utils

class CResultsWindow(QWidget):
	def __init__(self):
		super().__init__()    
		self.__createUI()

	def __createUI(self):
		# ---------------- UI ----------------------
		self.setGeometry(10, 30, 1370, 800)
		self.setWindowTitle("Repository Matches")

		
		# Define experiment Tree View
		self.treeView = QTreeView(self)    

		self.treeRoot = TreeItem(["Selected", r"Source", "Action", r"Target",r"Type",r"Copies"])
		standardModel = TreeModel(self.treeRoot)        	
		self.treeView.setModel(standardModel)
		
		self.treeView.setMinimumWidth(1370)
		self.treeView.setMinimumHeight(800)
		self.treeView.setColumnWidth(0, 130)
		self.treeView.setColumnWidth(2, 140)
		self.treeView.setColumnWidth(1, 550)
		self.treeView.setColumnWidth(3, 550)		
		self.treeView.expandAll()

	def loadResults(self, matches, repoPath, sourcePath):
		# matches must contain:
		# the source path, the match type, the corresponding repository locations
		# type is computed from the path: either a file or a directory
		# matches never include pure directories: these have to be recognized as we traverse the matches, 
		# and the hierarchy has to be deduced

		 
		currentDir = []
		dirNodes = {}
		for (path, matchClass, repoList) in matches:
			print("Adding match for {0}".format(path))
			# obtain this file's path            
			dirname= utils.getPath(path)
			# if this is the first element, create a directory entry in the tree
			if currentDir == []:
				treeItem = self.addDir(dirname, self.treeRoot, repoPath, sourcePath)
				currentDir.append(dirname)
				dirNodes[dirname] = treeItem
			else:
				missingDirs = []
				while dirname not in currentDir:  
					missingDirs.append(dirname)
					dirname = os.path.dirname(dirname)
				
				parentNode = dirNodes[dirname]
				
				while len(missingDirs) > 0:
					dirname = missingDirs.pop()
					parentNode = self.addDir(dirname, parentNode, repoPath, sourcePath)
					currentDir.append(dirname)
					dirNodes[dirname] = parentNode

			parentNode = dirNodes[dirname]
			self.addFile(path, matchClass, repoList, parentNode, repoPath, sourcePath)
					
					
	def addDir(self, sourceFile, parent, repoPath, sourcePath):
		path1 = sourceFile
		relPath = utils.relativePath(sourceFile, sourcePath)
		path2 = os.path.join(repoPath, relPath)
		return TreeItem([False, path1, False, path2, "D",[]], parent)
					
	def addFile(self, sourceFile, match, repoList, parent, repoPath, sourcePath):
		path1 = sourceFile
		relPath = utils.relativePath(sourceFile, sourcePath)
		path2 = os.path.join(repoPath, relPath)         
		return TreeItem([False, path1, match, path2, "F",repoList], parent)

			
		