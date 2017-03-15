#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Photography Manager

Application to create a consolidated backup of photographs from different sources.

author: Alexandre Pinto
"""


from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel, QStyle, QFileDialog

class CTextWithLabel(QLineEdit):
	def __init__(self, label, defaultText, parent):
		super().__init__(parent)
		self.__label = QLabel(label, parent)
		self.__label.resize(self.__label.width(), 30)
		
	def move(self, x,y):
		self.__label.move(x,y)
		super().move(x, y + self.__label.height())

	def setGeometry(self,x,y,w,h):
		self.resize(w,h)
		self.move(x,y)
	
		
class CDirText(CTextWithLabel):
	def __init__(self, label, defaultSource, parent):
		super().__init__(label, defaultSource, parent)
		self.__button = CDirButton(parent)
		self.__button.clicked.connect(self.__openDialog)
	
	def __openDialog(self):
		fileName = QFileDialog.getExistingDirectory(self.sender().parent(), "Select Directory", self.text(), QFileDialog.ShowDirsOnly)
		if (not fileName is None):
			self.setText(fileName)
	
	def move(self,x,y):
		super().move(x,y)
		self.__button.move(x + self.width(), self.y())
		
	def setGeometry(self,x,y,w,h):
		super().setGeometry(x,y,w,h)
		self.resize(w,h)
		self.move(x,y)

class CDirButton(QPushButton):
	def __init__(self, parent):
		super().__init__(parent)

		style = self.style()
		icon = style.standardIcon(QStyle.SP_DirIcon)
		self.setIcon(icon)
		self.resize(20,20)
