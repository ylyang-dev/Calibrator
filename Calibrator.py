import os
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QInputDialog, QFileDialog, QMessageBox
from struct import *

qtCreatorFile = "AppGui.ui"
if os.path.isfile(qtCreatorFile):
	# Use AppGui.ui file for debug
	Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
else:
	# Use converted AppGui.py file for release
	from AppGui import Ui_MainWindow


class Calibrator(QtWidgets.QMainWindow, Ui_MainWindow):
	'''
	DragonFly RF calibration file generator application.
	'''
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.setWindowFlags( QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint |     \
		                     QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint )

		self.listLoopMode = [ self.cmbLoopMode_1, self.cmbLoopMode_2 ]
		self.listOpenLoopAtt = [ self.txtOpenLoopAtt_1, self.txtOpenLoopAtt_2 ]
		self.listClosedLoopPower = [ self.txtClosedLoopPower_1, self.txtClosedLoopPower_2 ]

		self.listVoltage = [ self.txtVoltage_1,  self.txtVoltage_2,  self.txtVoltage_3,  self.txtVoltage_4,
							 self.txtVoltage_5,  self.txtVoltage_6,  self.txtVoltage_7,  self.txtVoltage_8,
							 self.txtVoltage_9,  self.txtVoltage_10, self.txtVoltage_11, self.txtVoltage_12,
							 self.txtVoltage_13, self.txtVoltage_14, self.txtVoltage_15, self.txtVoltage_16,
							 self.txtVoltage_17, self.txtVoltage_18, self.txtVoltage_19, self.txtVoltage_20,
							 self.txtVoltage_21, self.txtVoltage_22, self.txtVoltage_23, self.txtVoltage_24,
							 self.txtVoltage_25, self.txtVoltage_26, self.txtVoltage_27, self.txtVoltage_28,
							 self.txtVoltage_29, self.txtVoltage_30, self.txtVoltage_31, self.txtVoltage_32 ]

		self.listPower   = [ self.txtPower_1,  self.txtPower_2,  self.txtPower_3,  self.txtPower_4,
							 self.txtPower_5,  self.txtPower_6,  self.txtPower_7,  self.txtPower_8,
							 self.txtPower_9,  self.txtPower_10, self.txtPower_11, self.txtPower_12,
							 self.txtPower_13, self.txtPower_14, self.txtPower_15, self.txtPower_16,
							 self.txtPower_17, self.txtPower_18, self.txtPower_19, self.txtPower_20,
							 self.txtPower_21, self.txtPower_22, self.txtPower_23, self.txtPower_24,
							 self.txtPower_25, self.txtPower_26, self.txtPower_27, self.txtPower_28,
							 self.txtPower_29, self.txtPower_30, self.txtPower_31, self.txtPower_32 ]
		
		self.txtRevision.setAlignment ( QtCore.Qt.AlignCenter )
		self.txtPowerLevelCount.setAlignment ( QtCore.Qt.AlignCenter )
		self.txtDetectPointCount.setAlignment ( QtCore.Qt.AlignCenter )
		
		self.cmbLoopMode_1.clear ()
		self.cmbLoopMode_1.addItems ( [ "Open Loop", "Closed Loop" ] )

		self.cmbLoopMode_2.clear ()
		self.cmbLoopMode_2.addItems ( [ "Open Loop", "Closed Loop" ] )

		for openLoopAtt in self.listOpenLoopAtt:
			openLoopAtt.setAlignment ( QtCore.Qt.AlignCenter )

		for closedLoopPower in self.listClosedLoopPower:
			closedLoopPower.setAlignment ( QtCore.Qt.AlignCenter )

		for voltage in self.listVoltage:
			voltage.setAlignment ( QtCore.Qt.AlignCenter )

		for power in self.listPower:
			power.setAlignment ( QtCore.Qt.AlignCenter )
		

		# Browse button and Generate button
		self.btnGenerate.setEnabled ( False )
		self.btnBrowse.pressed.connect   ( self.btnBrowse_pressed_callback )
		self.btnGenerate.pressed.connect ( self.btnGenerate_pressed_callback )


	def btnBrowse_pressed_callback ( self ):
		options  = QFileDialog.Options ()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName ( self, "Open Calibration File", "", "Calibration Files (*.cfg);;All Files (*)", options = options )
		if fileName:
			self.txtFileName.setText ( fileName )
			fin = open ( fileName, "rb" )
			cal_data = fin.read ()
			fin.close ()
			self.populate_calibraton_data ( cal_data )


	def populate_calibraton_data ( self, cal_data ):
		revision, powerLevelCount = unpack ( "<HB", cal_data [ 0 : 3 ] )

		self.txtRevision.setText ( str ( revision ) )
		self.txtRevision.setAlignment ( QtCore.Qt.AlignCenter )
		self.txtPowerLevelCount.setText ( str ( powerLevelCount ) )
		self.txtPowerLevelCount.setAlignment ( QtCore.Qt.AlignCenter )

		for i in range ( powerLevelCount ):
			loopMode, openLoopAtten, closedLoopPower = unpack ( "<BHH", cal_data [ 3 + i * 5 : 8 + i * 5 ] )
			self.listLoopMode [ i ].setCurrentIndex ( loopMode )
			self.listOpenLoopAtt [ i ].setText ( str ( openLoopAtten ) )
			self.listOpenLoopAtt [ i ].setAlignment ( QtCore.Qt.AlignCenter )
			self.listClosedLoopPower [ i ].setText ( str ( closedLoopPower ) )
			self.listClosedLoopPower [ i ].setAlignment ( QtCore.Qt.AlignCenter )

		detectPointCount = cal_data [ 13 ]
		self.txtDetectPointCount.setText ( str ( detectPointCount ) )
		self.txtDetectPointCount.setAlignment ( QtCore.Qt.AlignCenter )

		for i in range ( 32 ):
			voltage, power = unpack ( "<HH", cal_data [ 14 + i * 4 : 18 + i * 4 ] )
			self.listVoltage [ i ].setText ( str ( voltage ) )
			self.listVoltage [ i ].setAlignment ( QtCore.Qt.AlignCenter )
			self.listPower [ i ].setText ( str ( power ) )
			self.listPower [ i ].setAlignment ( QtCore.Qt.AlignCenter )

		self.btnGenerate.setEnabled ( True )


	def btnGenerate_pressed_callback ( self ):
		# Revision
		try:
			revision = int ( self.txtRevision.toPlainText () )
			if ( revision < 0 ):
				raise ValueError
		except ValueError:
			QMessageBox.critical ( self, "Error", "Invalid Version.\n\nMust be >= 0.", QMessageBox.Ok )
			self.txtRevision.setFocus ()
			return
		#print ( "revision: %d" % revision )


		# RF power level count
		try:
			powerLevelCount = int ( self.txtPowerLevelCount.toPlainText () )
			if ( powerLevelCount < 2 ):
				raise ValueError
		except ValueError:
			QMessageBox.critical ( self, "Error", "Invalid Power Level Count.\n\nMust be >= 2.", QMessageBox.Ok )
			self.txtPowerLevelCount.setFocus ()
			return
		
		cal_data = pack ( "<HB", revision, powerLevelCount )
		#print ( "powerLevelCount: %d" % powerLevelCount )


		# RF power level settings
		for i in range ( powerLevelCount ):
			# RF loop control mode
			loopMode = self.listLoopMode [ i ].currentIndex ()

			# RF power level open loop attenuation
			try:
				openLoopAtten = int ( self.listOpenLoopAtt [ i ].toPlainText () )
			except ValueError:
				QMessageBox.critical ( self, "Error", "Invalid Open Loop Attenuation #%d." % ( i + 1 ), QMessageBox.Ok )
				self.listOpenLoopAtt [ i ].setFocus ()
				return

			# RF power level closed loop power
			try:
				closedLoopPower = int ( self.listClosedLoopPower [ i ].toPlainText () )
			except ValueError:
				QMessageBox.critical ( self, "Error", "Invalid Closed Loop Power #%d." % ( i + 1 ), QMessageBox.Ok )
				self.listClosedLoopPower [ i ].setFocus ()
				return

			cal_data += pack ( "<BHH", loopMode, openLoopAtten, closedLoopPower )
			#print ( "loopMode: %2d, openLoopAtten: %5d, closedLoopPower: %5d" % ( loopMode, openLoopAtten, closedLoopPower ) )


		# Detector curve count
		try:
			detectPointCount = int ( self.txtDetectPointCount.toPlainText () )
			if ( detectPointCount > 32 ) or ( detectPointCount <= 0 ):
				raise ValueError
		except ValueError:
			QMessageBox.critical ( self, "Error", "Invalid Detector Point Count.\n\nValid range: (0, 32].", QMessageBox.Ok )
			self.txtDetectPointCount.setFocus ()
			return

		cal_data += pack ( "<B", detectPointCount )
		#print ( "detectPointCount: %d" % detectPointCount )


		# Detector point settings
		for i in range ( 32 ):
			# Voltage
			try:
				voltage = int ( self.listVoltage [ i ].toPlainText () )
			except ValueError:
				QMessageBox.critical ( self, "Error", "Invalid Voltage #%d." % ( i + 1 ), QMessageBox.Ok )
				self.listVoltage [ i ].setFocus ()
				return

			# Power
			try:
				power = int ( self.listPower [ i ].toPlainText () )
			except ValueError:
				QMessageBox.critical ( self, "Error", "Invalid Power #%d." % ( i + 1 ), QMessageBox.Ok )
				self.listPower [ i ].setFocus ()
				return

			cal_data += pack ( "<HH", voltage, power )
			#print ( "voltage: %5d, power: %5d" % ( voltage, power ) )

		#print ( cal_data )
		#print ( self.txtFileName.toPlainText () )
		# ready to write back to file
		try:
			with open ( self.txtFileName.toPlainText (), "wb" ) as f:
				f.write ( cal_data )
		except FileNotFoundError:
			QMessageBox.critical ( self, "Error", "File not found:\n\n" + self.txtFileName.toPlainText (), QMessageBox.Ok )
			self.txtFileName.setFocus ()
			return

		QMessageBox.information ( self, "File Generation", "Calibration file is stored at:\n\n" + self.txtFileName.toPlainText (), QMessageBox.Ok )


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = Calibrator()
	window.show()
	sys.exit(app.exec_())
