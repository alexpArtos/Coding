from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

class TreeModel(QStandardItemModel):
	def __init__(self, root, parent=None):
		super(TreeModel, self).__init__(parent)
		self.rootItem = root
		

	def columnCount(self, parent = QtCore.QModelIndex()):
		if parent.isValid():
			return parent.internalPointer().columnCount()
		else:
			return self.rootItem.columnCount()

	def data(self, index, role):
		if not index.isValid():
			return None
		
		print("model data. Row: " + str(index.row()) + " - Role: " + str(role))
		
		if role == Qt.DisplayRole:          
			item = index.internalPointer()
			if item is not None:
				print(item)
			else:
				print("Null item")
			return item.data(index.column())
		elif role == Qt.CheckStateRole:
			if (index.row() == 1 and index.column() == 0):
				return Qt.Unchecked

	def flags(self, index):
		if not index.isValid():
			return QtCore.Qt.NoItemFlags
		return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable

	def headerData(self, section, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return self.rootItem.data(section)
		return None

	def index(self, row, column, parent):
		if not self.hasIndex(row, column, parent):
			return QtCore.QModelIndex()
		if not parent.isValid():
			parentItem = self.rootItem
		else:
			parentItem = parent.internalPointer()
		childItem = parentItem.child(row)
		if childItem:
			return self.createIndex(row, column, childItem)
		else:
			return QtCore.QModelIndex()

	def parent(self, index):
		if not index.isValid():
			return QtCore.QModelIndex()
		childItem = index.internalPointer()
		parentItem = childItem.parent()
		if parentItem == self.rootItem:
			return QtCore.QModelIndex()
		return self.createIndex(parentItem.row(), 0, parentItem)

	def rowCount(self, parent = QtCore.QModelIndex()):
		if parent.column() > 0:
			return 0
		if not parent.isValid():
			parentItem = self.rootItem
		else:
			parentItem = parent.internalPointer()
		return parentItem.childCount()

