from PyQt5.QtGui import QStandardItem

class TreeItem(object):
	def __init__(self, data, parent=None):
		self.parentItem = parent
		self.itemData = data
		self.childItems = []
		if (parent is not None):
			parent.appendChild(self)

	def appendChild(self, item):
		self.childItems.append(item)
		item.parent = self

	def child(self, row):
		return self.childItems[row]

	def childCount(self):
		return len(self.childItems)

	def columnCount(self):
		return len(self.itemData)

	def data(self, column):
		try:
			# print("Item data: " + str(self.itemData))
			# print("Column: " + str(column))
			return self.itemData[column]
		except IndexError:
			return None

	def parent(self):
		return self.parentItem

	def row(self):
		if self.parentItem:
			return self.parentItem.childItems.index(self)
		return 0

	def __repr__(self):
		if self.itemData is None:
			data = "None"
		else:
			data = str(self.itemData)
		return "TreeItem: " + data