from PyQt5.QtGui import QStandardItemModel, QColor, QBrush
from PyQt5.QtCore import Qt, QVariant, pyqtSignal, QModelIndex
from PyQt5 import QtCore
# import pdb

from CTreeItem import TreeItem

# general notes:
# the model is constantly playing a dance between indices and TreeItems
# everything in the model is based on indices, but the relations between the data
# can only be understood via the TreeItems.
# Therefore, it is necessary to convert from ones to the others.
# The root of the tree is self.rootItem, which is a TreeItem.
# The corresponding index is an invalid index, obtained via QModelIndex().
# Whenever we test is an index is valid, with isValid(), we are in effect 
# testing if we are pointing at the root of the tree.
# To convert from indices to items is easy: just call internalPointer().
# To convert in the other direction, we have to call self.createIndex(row, column, parent).


class TreeModel(QtCore.QAbstractItemModel):
	def __init__(self, rootNode, parent=None):
		''' TreeModel constructor
		'''
		super(TreeModel, self).__init__(parent)
		self.rootItem = rootNode
#		self.dataChanged = pyqtSignal(QModelIndex,QModelIndex)
		self.debug = False
		
	def columnCount(self, parent):
		''' Returns the number of columns held by a parent node
			[parent] is an index for a TreeItem.
		'''
		if parent.isValid():
			return parent.internalPointer().columnCount()
		else:
			return self.rootItem.columnCount()
			
	def data(self, index, role):
		''' Returns the content of the item pointed by [index] and for [role]
		'''
		if not index.isValid():
			return None
		if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
			if index.column() == 2:
				result = ""
				name = str(index)
				parent = str(self.parent(index))
				return "Name: {0}\nParent: {1}".format(name, parent)
			elif index.column() > 0 and index.column() < 4:
				item = index.internalPointer()
				return item.data(index.column())
			else:
				return ""
		elif role == QtCore.Qt.ToolTipRole:
			return self.indexToStr(index)
		elif role == QtCore.Qt.CheckStateRole:
			if index.column() == 0:
				item = index.internalPointer()
				return item.data(index.column())
		elif role == QtCore.Qt.ForegroundRole:
			item = index.internalPointer()
			type = item.data(4)
			if type == "D":
				#red = QBrush(QColor(100,0,0))
				red = QBrush(Qt.red)
				return red
			elif type == "F":
				blue = QBrush(Qt.blue)
				return blue
			else:
				return QVariant()

	def setData(self, index, value, role):
		''' Gives another [value] to the item specified by [index] and for [role]
		'''
		if role & ( QtCore.Qt.EditRole | QtCore.Qt.CheckStateRole) > 0:
			item = index.internalPointer()
			item.setData(index.column(), value)
			if (index.column() == 0):
				self.refreshNode(index)
		return True
		
	def refreshNode(self, index):
		''' Sends a signal to refresh the node pointed by [index],
			its children and all nodes on the path to root
		'''
		self.refreshChildren(index)
		self.refreshFromNodeToRoot(index)

	def refreshFromNodeToRoot(self, index):
		''' Refreshes the nodes from [index] to root.
		'''
		self.dataChanged.emit(index, index)
		parent = self.parent(index)		
		if parent.isValid():		
			self.refreshFromNodeToRoot(parent)
		
	def refreshChildren(self, index):
		'''Refreshes all nodes children of the node pointed by [index]
		'''
		# print("refrehs children for: " + str(index.internalPointer().name()))
		if self.hasChildren(index):
			leftChild = self.index(0,0,index)
			topLeft = self.createIndex(0,0,leftChild)
			# print("topLeft: " + str(topLeft.internalPointer().name()))
			nChildren = self.rowCount(index)
			# print("rowCount: " + str(nChildren))
			rightChild = self.index(nChildren - 1,0,index)
			topRight = self.createIndex(nChildren-1,0, rightChild)	
			# print("topRight: " + str(topRight.internalPointer().name()))
			self.dataChanged.emit(topLeft, topRight)		

	def hasChildren(self, index):
		''' returns whether this node has any children
		'''
		if not index.isValid():
			item = self.rootItem
		else:
			item = index.internalPointer()
		if item.childItems == []:
			return False
		else:
			return True
		
			
	def flags(self, index):
		''' Returns the flags for the node pointed by [index]
		'''
		if not index.isValid():
			return QtCore.Qt.NoItemFlags
		baseFlags = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
		if index.column() == 0:
			 baseFlags = baseFlags | QtCore.Qt.ItemIsUserCheckable 
		return baseFlags

	def headerData(self, section, orientation, role):
		''' Returns the header value for the [section]
		'''
		headerList = ["Selected", r"Source", "Action", r"Target",r"Type"]
		if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
			if section < 4: # show only first 4 columns. Other data is for background purposes
				return headerList[section]
		return None

	def index(self, row, column, parent):
		''' Returns an index for the child of parent at coordinates [row] and [index]
		'''
		if not self.hasIndex(row, column, parent):
			return QtCore.QModelIndex()
		if not parent.isValid():
			parentItem = self.rootItem
		else:
			parentItem = parent.internalPointer()
		childItem = parentItem.child(row)
		if childItem:
			return self.createIndex(row, column, childItem) # should this not be self.createIndex(row, column, parentItem) instead?
		else:
			return QtCore.QModelIndex()

	def parent(self, index):
		''' Returns an index for the parent of the node pointed by [index]
		'''
		if not index.isValid():
			return QtCore.QModelIndex()
		childItem = index.internalPointer()
		parentItem = childItem.parent()
		if parentItem == self.rootItem:
			return QtCore.QModelIndex()
		return self.createIndex(parentItem.row(), 0, parentItem)

	def rowCount(self, parent):
		''' Returns the number of rows held by a parent node
			[parent] is an index for a TreeItem.
		'''		
		if parent.column() > 0:
			return 0
		if not parent.isValid():
			parentItem = self.rootItem
		else:
			parentItem = parent.internalPointer()
		if parentItem == QModelIndex():
			return -1
		else:
			return parentItem.childCount()
			
	def dump(self, item, level):
		print()
		print("Starting dumping index")
		# obtain an index for [item]
		if item == self.rootItem:
			index = QModelIndex()
		else:
			index = createIndex(0,0,item.parentItem())
		print("Starting index: {0}".format(index))

		self.dumpIndex(index, level)
		
		for i in range(0, self.rowCount(index)):
			childIndex = self.createIndex(i, 0, index)
			self.dumpIndex(childIndex, level+1)

	def indexToStr(self, index):
		name = str(index)
		row = str(index.row())
		col = str(index.column())
		pointer = str(index.internalPointer())
		parent = str(index.parent())
		#rCount = str(index.rowCount())
		#cCount = str(index.columnCount())
		#sons = str(index.childCount())
		
		result = "Name: {0}\nRow: {1}\nColumn: {2}\nPointer: {3}\nParent: {4}".format(name, row, col, pointer, parent)
		return result

	def dumpIndex(self, index, level):
		if level > 2:
			return
		prefix = " "*(level * 4)
		print("{0}New index\n>>>>>>>>>>>>>".format(prefix))
		item = index.internalPointer()
		if not index.isValid():
			print("{0}invalid index".format(prefix))
		else:
			print("{0}index details:".format(prefix))
			print("{0}Dump Item. Row:{1}, Column:{2}, Parent:{3}".format(prefix, index.row(), index.column(), index.parent()))
			print("{0}Item: {1} - Index: {2}".format(prefix, item, index))
			print([self.data(self.createIndex(0,i,index), QtCore.Qt.DisplayRole) for i in range(0,5)])
			print([item.data(i) for i in range(0,5)])
			print("{0} Rows: {1}".format(prefix, str(self.rowCount(index))))
			print("{0} Columns: {1}".format(prefix, str(self.columnCount(index))))

		if item is not None:
			print("{0} Name: {1}".format(prefix,  item.name()))
			print("{0} Children: {1}".format(prefix,  str(item.childCount())))
			print("----------------------")
			
		
