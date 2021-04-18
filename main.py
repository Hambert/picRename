# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from gui.MainForm import Ui_FileRename
from control.fileRenamePlus import getFileDate, rightExt, renameFiles
import os
import exifread
import PIL
from PIL import Image

class mainQtForm(Ui_FileRename):
	def __init__(self, dialog):
		Ui_FileRename.__init__(self)
		self.setupUi(dialog)
		self.rename_btn.clicked.connect(self.listDir)
		self.select_btn.clicked.connect(self.showDialog)
		self.refresh_btn.clicked.connect(self.refreshFiles)
		self.selectedDir = ''

	def listDir(self):
		print('list dir content')
		try :
			#self.listWidget.addItem('Moin')
			print(self.selectedDir)
			#print(self.fileList)
			renameFiles(path=self.selectedDir, newFilename=self.inputFilename, dryRun=False, resizeOption=False )
		except:
			print("Error")
	
	def selectDir(self):
		print('Select dir')
		return

	
	def refreshFiles(self):
		if self.selectedDir is not '':
			print('File selected: ' + self.selectedDir)
			self.listWidget_preview.clear()
			self.listWidget.clear()
			os.chdir(self.selectedDir)
			self.fileList = os.listdir()
			self.fileList.sort()

			if self.lineEdit_FileName.text() is not '':
				self.inputFilename = self.lineEdit_FileName.text()
			else:
				self.inputFilename = 'Dienstabend'


			i = 1
			for filename in self.fileList:
				if i < 10:
					count = "0" + str(i)
				else:
					count = str(i)

				extension = rightExt(filename)
				if not extension:
					continue

				fileDate = getFileDate(filename)
				if not fileDate:
					fileDate = ""


				self.listWidget.addItem(filename)
				newFilename = fileDate + "_" + self.inputFilename + count + extension
				i += 1
				
				self.listWidget_preview.addItem(newFilename)
		else:
			self.listWidget_preview.clear()
			self.listWidget.clear()
			print('cancel')

		return


	def showDialog(self):

		#fname = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', '/home',"Images files (*.png *.jpeg *.jpg)")
		self.selectedDir = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Output Folder", QtCore.QDir.currentPath());
		self.refreshFiles()
		return

			
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	# Hier ist in der ui Datei ein QDialog erstellt
	mainWindow = QtWidgets.QDialog()
	
	mainClass = mainQtForm(mainWindow)
	
	mainWindow.show()
	sys.exit(app.exec_())
