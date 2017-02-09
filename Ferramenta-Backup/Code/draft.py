#test.py

#open file

import os
import datetime 
import sys
from pathlib import Path
import hashlib
from CTreeItem import TreeItem
from CTreeModel import TreeModel

from PyQt5.QtWidgets import QWidget, QTreeView, QApplication
from PyQt5.QtCore import QModelIndex

def hashFile(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

	   # loop till the end of the file
	   chunk = 0
	   while chunk != b'':
		   # read only 1024 bytes at a time
		   chunk = file.read(1024)
		   h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()

def defaultLocation():
	return os.getcwd();

def defaultIndex():
	path = os.path.join (defaultLocation(), "MasterRPT.idx")
	if not os.path.exists(path):
		# create file if it does not exist
		file = open(path, 'w')
		file.close()
	return path;
	
def printDefaultAttributes():
	name = defaultIndex()
	stats = os.stat(name)
	print("Size: " + str(stats.st_size))
	date = datetime.datetime.fromtimestamp(stats.st_mtime)
	print("Time: " + datetime.datetime.isoformat(date))
	print("Hash: " + hashFile(name))

def printContents():
	path = defaultIndex()
	print("Path: " + path)
	file = 	open(path, mode="r")
	line = file.readline()
	print ("Line: " + line)	
	print ("All: ")
	all = file.read()
	print ("Read all: " + all)
	file.close()
	
def printTree(treeItem, tab, model):
	prefix = " " * (tab * 4)
	if treeItem.parentItem == None:
		index = QModelIndex()
		row = -1
	else:
		row = treeItem.row()
		index = model.createIndex(row, 0, treeItem.parentItem)		
	print("{0}{1} --- {2} [{3}, {4}, {5}]".format(prefix,treeItem,index, row, 0, treeItem.parentItem))
	for item in treeItem.childItems:
		printTree(item, tab+1, model)
	
class CMainWindow(QWidget):
	def __init__(self):
		super().__init__()	
		self.__createUI()

	def __createUI(self):
		# ---------------- UI ----------------------
		self.setGeometry(400, 30, 600, 400)
		self.setWindowTitle("Files Locations")

		
		# Define experiment Tree View
		self.treeView = QTreeView(self)	
		self.treeView.setMinimumWidth(700)
		self.treeView.setMinimumHeight(500)

		item0 = TreeItem(["Selected", r"Source", "Action", r"Target",r"Type"])
		dir0 = TreeItem([False, r"Path 1", False, r"PathA", "D"], item0)
		file1 = TreeItem([False, r"Path 1\File1", False, r"PathA\File1", "F"], dir0)
		file2 = TreeItem([False, r"Path 1\File2", False, r"PathA\File2", "F"], dir0)
		dir1 = TreeItem([False, r"Path 1\sub1", False, r"PathA\sub1", "D"], dir0)
		file3 = TreeItem([False, r"Path 1\sub1\File3", False, r"PathA\sub1\File3", "F"], dir1)
		file4 = TreeItem([False, r"Path 1\sub1\File4", False, r"PathA\sub1\File4", "F"], dir1)
		dir2 = TreeItem([False, r"Path 2", False, r"PathB", "D"], item0)
		file1 = TreeItem([False, r"Path 2\File1", False, r"PathB\File1", "F"], dir2)
		
		# basepath = "testHierarchy"
		# baseDir1 = "sourceDir"
		# baseDir2 = "repoDir"
		
		# dirToNode = {}
		
		# rootNode = TreeItem(["Selected", r"Source", "Action", r"Target",r"Type"])
		
		# standardModel = TreeModel(item0)
		
		# for path, subdirs, files in os.walk(basepath):
			# dir = TreeItem([False, os.path.join(baseDir1,path), False, os.path.join(baseDir2,path),"D"])
			# dirToNode[path] = dir
			# if path == basepath:
				# rootNode.appendChild(dir)
			# else:
				# parent = os.path.dirname(path)
				# parentNode = dirToNode[parent]
				# parentNode.appendChild(dir)
			# for filename in files:
				# file = TreeItem([False, os.path.join(baseDir1,path,filename), False, os.path.join(baseDir2,path,filename),"F"], dir)
				
		
		# standardModel = TreeModel(rootNode) 
		standardModel = TreeModel(item0)
		
		printTree(item0, 0, standardModel)		
		
		self.treeView.setModel(standardModel)
	#	standardModel.dump(item0, 0)
		self.treeView.expandAll()

		
		
		# print("RowCount: " + str(standardModel.rowCount()))
		# print("ColumnCount: " + str(standardModel.columnCount()))

				

if __name__ == '__main__':
	# print ("Default location: " + defaultLocation())
	# print ("Default Index: " + defaultIndex())
	# printDefaultAttributes()
	# printContents()
	# d = {}
	# d["a"] = 1
	# d["b"] = 2
	# print (d["a"])
	# print ("a" in d)

	app = QApplication(sys.argv)	
	main = CMainWindow()
	main.show()	
	app.exec_()
	