#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Photography Manager

Application to create a consolidated backup of photographs from different sources.

author: Alexandre Pinto
"""

import pdb
import os
import hashlib
import re

from PyQt5.QtWidgets import QMessageBox, QFileDialog, QInputDialog, QLineEdit


def getSaveFilename(caption, widget, defaultPath, extension):
	(filename, filter) = QFileDialog.getSaveFileName(widget, caption, defaultPath, extension, None, QFileDialog.DontConfirmOverwrite) # this always returns a tuple.
	ok = (not filename is None) and (len(filename) > 0)
	return (filename, ok)

def alert(message):
	msg = QMessageBox()
	msg.setIcon(QMessageBox.Information)
	msg.setText(message)
	msg.setWindowTitle("Alert to user")
	msg.setStandardButtons(QMessageBox.Ok)
	msg.exec_()

def yesNoQuestion(message):
	msg = QMessageBox()
	msg.setIcon(QMessageBox.Warning)
	msg.setText(message)
	msg.setWindowTitle("Alert to user")
	msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
	msg.setDefaultButton(QMessageBox.Cancel)
	result = msg.exec_()
	return result == QMessageBox.Ok
	
def inputText(widget, title, caption, default):
	return QInputDialog.getText(widget, title, caption, QLineEdit.Normal, default)

def hashFile(filename):
   """This function returns the SHA-1 hash
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

def fileExists(filename):
	return os.path.exists(filename)
	
def defaultLocation():
	return os.getcwd();
	
def relativePath(path, baseLocation):
	return os.path.relpath(path, baseLocation)