import sys
import random
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import time
from os import walk
from toPdf import toPdf 

class ThreatClass(QThread):
	any_signal = QtCore.pyqtSignal(str)

	def __init__(self, parent=None, index='', path='',out='',height=0,width=0,potrait='Landscape'):
		super(ThreatClass, self).__init__(parent)
		self.index = index
		self.is_running = True
		self.inputFolderPath = path
		self.out = out
		self.height = height
		self.width = width
		self.potrait = potrait
	
	def run(self):
		print(self.width)
		print(self.height)
		pdf = toPdf(self.height,self.width,self.potrait)
		f = []
		for (dirpath, dirnames, filenames) in walk(self.inputFolderPath):
			self.any_signal.emit('<br>'+str(len(filenames))+" Dosyalar işlenmek için hazırlanıyor...")
			for file in filenames:
				splt = file.split('.')
				if 'xslt'==splt[len(splt)-1]:
					self.any_signal.emit('<br>'+file+' Dosya işleniyor.')
					pth = dirpath+'/'+file
					pdf.main(pth,self.out,file)
				

		
	def stop(self):
		self.is_running = False
		self.terminate()

class MyApp(QWidget):
	
	def __init__(self, parent = None):
		super(MyApp, self).__init__(parent)
		app = QtWidgets.QApplication(sys.argv)
		self.logTxt = ''
		window = uic.loadUi("main.ui")
		window.inputFolder.clicked.connect(self.getfile)
		window.outFolder.clicked.connect(self.getfile1)
		window.pushButton.clicked.connect(self.start)
		window.pushButton_2.clicked.connect(self.stoptask)
		window.spinBox.setValue(210)
		window.spinBox_2.setValue(297)

		window.comboBox_2.currentTextChanged.connect(self.on_combobox_changed)
		window.comboBox_3.currentTextChanged.connect(self.on_potrait_changed)
		
		self.inputEdit = window.lineEdit
		self.outEdit = window.lineEdit_2
		self.pushButton = window.pushButton
		self.logText = window.textEdit
		self.inputFolderPath = ''
		self.inputFolderOut = ''
		self.spinBox = window.spinBox
		self.spinBox_2 = window.spinBox_2
		self.potrait = 'Landscape'

		self.logWrite('<b>Select Folder</b>')
		window.show()		
		app.exec()

	def getfile(self):
		fname =  QFileDialog.getExistingDirectory(self, 'Open Folder')
		self.inputEdit.setText(fname)
		self.logWrite('<br><b>SELECTED FOLDER:</b> '+fname)
		self.inputFolderPath = fname

	def getfile1(self):
		fname =  QFileDialog.getExistingDirectory(self, 'Open Folder')
		self.outEdit.setText(fname)
		self.logWrite('<br><b>SELECTED FOLDER:</b> '+fname)
		self.inputFolderOut = fname

	def on_combobox_changed(self, value):
		if value=='A4':
			self.spinBox.setValue(210)
			self.spinBox_2.setValue(297)
		if value=='A5':
			self.spinBox.setValue(210)
			self.spinBox_2.setValue(148)

	def on_potrait_changed(self, value):
		self.potrait = value

	def start(self):
		if self.inputFolderPath=='' or self.inputFolderOut=='':
			self.logWrite('<br>Pls select folders...')
		else:
			self.pushButton.setEnabled(False)
			self.logWrite('<br>Progress started. Pls wait...')
			self.p = ThreatClass(parent=None,index='',path=self.inputFolderPath,out=self.inputFolderOut,height=self.spinBox_2.value(),width=self.spinBox.value(),potrait=self.potrait)
			self.p.start()
			self.p.any_signal.connect(self.logWrite)

	def stoptask(self):
		self.pushButton.setEnabled(True)
		self.logWrite('<br>Stop Progress')
		self.p.terminate()

	def logWrite(self,txt):
		self.logTxt = self.logTxt+str(txt)
		self.logText.setHtml(self.logTxt)



if __name__ == "__main__":
	app =  QtWidgets.QApplication(sys.argv)
	widget = MyApp()
	widget.resize(500, 500)
	widget.show()
	sys.exit(app.exec())