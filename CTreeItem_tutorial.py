from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import Qt, QVariant
import pdb

class TreeItem(object):
	def __init__(self, data, parent=None):
		self.parentItem = parent
		self.checked = None
		self.action = None

		# data i an array of information for the tree item
		# 0: whether this item is selected
		# 1: the source path
		# 2: the type of match
		# 3: the repo path
		# 4: whether it is a file or a directory
		# 5: the list of associated copies in the repository 
		
		if data[0]:
			self.checked = Qt.Checked
		else:
			self.checked = Qt.Unchecked

		if data[2]:
			self.action = Qt.Checked
		else:
			self.action = Qt.Unchecked
			
		self.source = data[1]
		self.target = data[3]
		self.type = data[4]
		self.copyList = data[5]
	
		if parent is not None:
			parent.appendChild(self)
		self.childItems = []

	def name(self):
		return self.source
		
	def appendChild(self, item):
		self.childItems.append(item)
		item.parentItem = self

	def child(self, row):
		return self.childItems[row]

	def childCount(self):
		if self.childItems == []:
			return 0
		else:
			return len(self.childItems)

	def columnCount(self):
		return 5

	def data(self, column):
		try:
			if column == 0:
				return self.checked
			elif column == 1:
				return self.source
			elif column == 2:
				return self.action
			elif column == 3:
				return self.target
			elif column == 4:
				return self.type
			else:
				return QVariant()
		except IndexError:
			return None

	def setData(self, column, value):
		try:
			if column == 0:
				self.checked = value
				if self.type == "D":
					if value != Qt.PartiallyChecked:			
						for child in self.childItems:
							child.setData(column, value)
				if self.parentItem is not None:
					self.parentItem.computeChecked()									
			if column == 1:
				self.source = value
			elif column == 2:
				self.action = value
			elif column == 3:
				self.target = value
			elif column == 4:
				self.type = value
		except IndexError:
			return None		
			
	def computeChecked(self):
		state = None
		for child in self.childItems:
			if state == None:
				# we let state be the checked value of the first child
				state = child.checked
				if state == Qt.PartiallyChecked:
					# if we are partially checked, we can never be anything else
					break
			else:
				# if we receive a different state from current, then we have at least two different checked states in the children
				# therefore we are partially checked for ever
				# otherwise, we keep the same state as current. this will remain only if all children have the same state.
				if child.checked != state:
					state = Qt.PartiallyChecked
					break
		self.checked = state
		if self.parentItem is not None:
			self.parentItem.computeChecked()
			
	def parent(self):
		return self.parentItem

	def row(self):
		if self.parentItem:
			return self.parentItem.childItems.index(self)
		return 0