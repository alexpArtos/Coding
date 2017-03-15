#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Photography Manager

Application to create a consolidated backup of photographs from different sources.

author: Alexandre Pinto
"""

import os
import re

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from CRepo import CRepository
import utils

class CRepositoryManager:
	def __init__(self, widget = None):
		self.widget = widget
		self.repoDict = {} # location --> repo
		self.repoToItemDict = {} # repo --> QStandardItem

	def loadRepositories(self):
		# read a file in the main module's directory,
		# creates a repository instance for each line		
		# and adds it to the model
		# this does not immediately add the repository items
		masterIndex = self.defaultIndex()
		file = open(masterIndex, 'r')
		for line in file:
			m = re.search(CRepository.descriptionPattern(), line)
			if (not m is None):
				repo = CRepository(m.group(1), m.group(2))
				self.addRepoToModel(repo)					
			else:
				print ("Unrecognized line in index file: " + line)
		file.close()
		
		# flag that tracks whether the model has changed 
		# between loading and saving the repositories		
		self.modelChanged = False
		return 

	def saveRepositories(self):
		if (not self.modelChanged):
			return
		answer = yesNoQuestion("Save repo-list changes?")
		if not answer:
			return
			
		# proceed with saving the repository
		masterIndex = self.defaultIndex()		
		file = open(masterIndex, 'w')
		nRepos = self.__viewModel.rowCount()
		print ("Saving " + str(nRepos) + " repos ")
		for n in range (0, nRepos):
			item = self.__viewModel.item(n, 0)
			repo = item.data()
			file.write(repo.description() + "\n")
		file.close()
		self.modelChanged = False	
		
	def loadRepoInMemory(self, filepath):
		repo = self.repoDict[filepath]
		repo.loadFromFile()
		return repo
		
	@staticmethod
	def descriptionPattern():
		return "\[(.*)\]: (.*)"

	
	# ----------- operations on the view model ---------------
	def setModel(self, model):
		self.__viewModel = model

	def addRepoToModel(self, repo):
		item = QStandardItem()
		item.setText(repo.description())
		item.setData(repo)
		self.__viewModel.appendRow(item)
		self.modelChanged = True
		self.repoDict[repo.location()] = repo
		self.repoToItemDict[repo] = item
		print("Added new repo {0}".format(repo.name()))
		
	def removeRepoFromModel(self, delRepo):
		nRepos = self.__viewModel.rowCount()
		for index in range (nRepos, 0, -1):
			adjIndex = index - 1

			# I may remove an item from the list
			# if that happens, there will be less than nRepos elements
			# so when index = nRepos-1, it will cause errors when trying
			# to access an item.
			# for this reason, we iterate the vector in opposite order
			item = self.__viewModel.item(adjIndex, 0)
			repo = item.data()
			if repo == delRepo:
				print ("Deleting repo " + repo.name())
				self.removeRepoFromModelByIndex(adjIndex)
				self.modelChanged = True
		del self.repoDict[repo.location()]
		del self.repoToItemDict[repo]

	def removeRepoFromModelByIndex(self, index):
		self.__viewModel.removeRow(index)
		
	def renameRepoInModel(self, filename, newName):
		repo = self.repoDict[filename]
		print ("Renaming repo " + repo.name())
		repo.setName(newName)
		item = self.repoToItemDict[repo]
		item.setText(repo.description())
		self.modelChanged = True
				
	# ---------------------------------------------------------

	# ------------------ Handlers for main operations -----------
	def removeRepo(self, repo):
		self.removeRepoFromModel(repo)
		os.remove(repo.location())
		
	def createRepo(self):
		# this function creates a repo file and adds a corresponding entry in the repo master file
		# the repo file includes details of all the files inside or below its location
		# Interaction: 
		# 1. ask for a filename
		# 2a. if this file does not exist, ask for a repository name
		# 2b. else warn the file exists and ask if we want to overwrite it. If so, this will be the same as a repair. 
		#     The repair gives a chance of changing the repository name
		# 3. create repo file and index entry.
		# 4. iterate over all files in the directory and add their details to the repo file
		
		# Test cases:
		# - cancel selection: ok
		# - create a new filename: ok
		# - select existing file, cancel
		# - select existing file, choose to repair
	
		# open dialog to choose a location
		(filename, locationOk) = getSaveFilename("Repository Location", self.widget, utils.defaultLocation(), self.repoExtension())
		if (locationOk):
			overwrite = False
			if (not os.path.exists(filename)):
				# filename is new. Ask for a repository name
				(repoName, nameOk) = inputText(self.widget, "Enter a description for the repository", "Repository Name", "")
				# create a new repo
				self.createRepoAt(filename, repoName, True)  
			else:
				# filename exists. Ask if user wants to repair
							
				answer = yesNoQuestion("Repository file exists. Do you want to repair?")
				repo = self.getRepoByLocation(filename)

				if (repo is None):
					print("Could not find repository definition for " + filename)
				else:
					if (answer):
						self.repairRepo(repo)
					else:
						# user has cancelled 
						locationOk = False

		
	def repairRepo(self, repo):
		(repoName, nameOk) = inputText(self.widget, "Enter a description for the repository", "Repository Name", repo.name())
		filename = repo.location()
		if (nameOk):
			ok = self.createRepoAt(filename, repoName, False) 
		else:
			print("User cancelled repairing a repository")
			ok = false
					
		if ok:
			print ("Renaming repo")
			self.renameRepoInModel(filename, repoName)			
		

		
	# create a new repository at a certain location, read all the files under it and write a repo entry for each of them
	# we do not need to create the entry in the master repo list, as that will be created when we save the model on exit.
	# But we could eventually offer an option to save the model before exitting the application, just in case we lose power or something
	def createRepoAt(self, filename, repoName, isNew):
		# create a repository
		repo = CRepository(repoName, filename)

		# add to model
		self.addRepoToModel(repo)					
		
		# iterate over all files in this directory
		print ("Filename: " + filename)
		for path, subdirs, files in os.walk(os.path.dirname(filename)):
			for name in files:
				fullPath = os.path.normpath(os.path.join(path, name))
				repo.addFile(fullPath)
		
		# create repo file at location
		repoFile = open(filename, 'w')
		# and write repository to it
		repo.writeTo(repoFile)	
		#close file
		repoFile.close()
		
	
		return True
		
					
	def getRepoByLocation(self, filename):
		if filename in self.repoDict:
			repo = self.repoDict[filename]
			return repo
		return None
	
		
	# return the location of the executing program 

	@staticmethod	
	def defaultIndex():
		path = os.path.join (utils.defaultLocation(), "MasterRPT.idx")
		if not os.path.exists(path):
			# create file if it does not exist
			file = open(path, 'w')
			file.close()
		return path;

		
	def repoExtension(self):
		return "*.rpt"
		
		