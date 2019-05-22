import os
import sys
import traceback 
import pandas as pd
from enum import Enum
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
 
from main_window import Ui_MainWindow

from Attractor_Config import Attractor_Config
from Attractors import Attractors

from colorcet import palette
from attr_MessageBox import attr_MessageBox

_cmaps = ['bgy','bgyw','bjy', 'bkr', 'bky', 'blues','coolwarm','dimgray','fire',
          'gray','gwv','isolum','kb','kbc','kg','kgy','kr','rainbow']
CMAPS = Enum('CMAPS', _cmaps)


class Main_Window(QMainWindow, Ui_MainWindow):
  def __init__(self):
    QMainWindow.__init__(self)
    Ui_MainWindow.__init__(self)

    #                1000000000
    self._numIters = 1000000 
    self._aOrientation = 'XY'
    self._cmap = ''
    self._attrType = None   #No attractor selected
    
    #Call the QT generated UI_MainWindow classes setupUi() fxn
    #to actually create the GUI
    self.setupUi(self)

    #Add values to controls not set in Ui_MainWindow 
    self.spinBox_NumberOfIterations.setValue(self._numIters)
    self.populate_comboBox_AxialOrientation() #THEY ADD THIS CODE!
    self.populateColorMap_combobox(self.comboBox_cmaps,0)

   
    #########################
    # Signals
    #########################
    #File menu - Load
    self.actionLoad_File.triggered.connect(self.slot_load_file)
    
    #File menu - Quit
    self.actionQuit.triggered.connect(self.close_application)
    
    #Save Attractor IMAGE They ADD THIS CODE
    #self.action_Save_Attractor

    self.comboBox_AttractorType.currentIndexChanged.connect(self.slot_AttractorType)
    
    self.spinBox_NumberOfIterations.valueChanged.connect(self.slot_NumIterations)
    
    self.comboBox_AxialOrientation.currentIndexChanged.connect(self.slot_AxialOrientation)
   
    self.comboBox_cmaps.currentIndexChanged.connect(self.slot_cmaps)
    
    self.pushButton_Plot.clicked.connect(self.slot_pBtn_Render)
    
  def slot_AttractorType(self, idx):
    """ Update to the newly selected attractor type """
    self._attrType = self.comboBox_AttractorType.currentText()
    
  def slot_NumIterations(self, val):
    self._numIters = val
        
  def slot_AxialOrientation(self, idx):
    self._aOrientation = self.comboBox_AxialOrientation.currentText()
  
  def slot_cmaps(self, idx):
    self._cmap = self.comboBox_cmaps.currentText()
    
  
  ######
  def slot_pBtn_Render(self):
    if not self._attrType:
      szMsg = 'Error: No attractor configurations selected!\nLoad configuration file and select attractor first!'   
      szTitle = 'No Configuration File Loaded'
      self.showMSGDialog(szMsg, szTitle)
      return

    self._attrData.getAttractor(self._attrType)
    coords = self._attrData.coords
    avars = self._attrData.params
    
    #Find the QFrame height and make that the img resolution.
    self._res = self.frame.frameGeometry().height()
    
    #attr = Attractors(fxn='Pickover', coords=coords, avars=avars)
    start  = time.time()
    attr = Attractors(fxn=self._attrType, coords=coords, avars=avars) 
    attr.numIters = self._numIters
    attr.aOrientation = self._aOrientation
    attr.res = self._res
     
    attr.cmap = self._cmap
    self._img = attr.dsplot()
        
    pixmap = QPixmap('tempAttr.png')
    self.lPixmap.setPixmap(pixmap)
    #self.resize(self.lPixmap.width(),self.lPixmap.height())
    
    end = time.time()
    timeTotal=end-start
    szMsg = ('Done!\nCalc time(seconds):       {}\nRender time(seconds):  {}\nTotal runtime:                {}'.format(attr._timeCalc, attr._timeRender, timeTotal))
    szTitle = 'Rendering Complete'
    self.showMSGDialog(szMsg)
    
    
  ######
  
  def populate_comboBox_AttractorType(self,idx=8):
    """"""
    for item in self._attrList:
      self.comboBox_AttractorType.addItem(item)
    self.comboBox_AttractorType.setCurrentIndex(idx)
    self._attrType = str(self.comboBox_AttractorType.currentText())
      
  
  def populate_comboBox_AxialOrientation(self, idx=0):
    #THEY ADD THIS CODE
    aOrientation = ('XY', 'XZ', 'YZ')
    for item in aOrientation:
      self.comboBox_AxialOrientation.addItem(item)
    self.comboBox_AxialOrientation.setCurrentIndex(idx)
    self._aOrientation = self.comboBox_AxialOrientation.currentText()
        
  def populateColorMap_combobox(self, cb_widget, cb_idx=0):
    """"""
    cb_widget.setIconSize(QSize(50, 8))
    for map in CMAPS:
      iconname = (':/cmaps/{}.png'.format(map.name))
      icon = QIcon()
      icon.addPixmap(QPixmap(iconname), QIcon.Normal, QIcon.Off)
      cb_widget.addItem(icon, map.name)

    cb_widget.setCurrentIndex(cb_idx)
    self._cmap = self.comboBox_cmaps.currentText()

    
  def showMSGDialog(self, szMsg='', szTitle=''):
    """ Create and show a warning message box stating to many data dimensions
        are selected when drop down an analysis dimension (3D->2D).
    """
    msg = attr_MessageBox()
    msg.setIcon(QMessageBox.Warning)

    msg.setText(szMsg)
    msg.setWindowTitle(szTitle)
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()
    
    
  #########################
  # Slots
  #########################
  def slot_load_file(self):
    title = 'Open Attractor Configuration File'
    filter = "Attractor files (*.atr)"
    fName = QFileDialog.getOpenFileName(None, title, '', filter)
    #print('Loading: {}'.format(fName))

    self._attrData = Attractor_Config(fName[0])
    
    #Get the unique list of attractors
    self._attrList = self._attrData.getAttractorList()
    self.populate_comboBox_AttractorType()
    
    self._haveConfig = True
    

  def close_application(self):
    """ Slot - File menu->Quit - close the application"""
    sys.exit(0)
    
      
    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    #MainWindow = QMainWindow()
    #ui = Ui_MainWindow()
    #ui.setupUi(MainWindow)
    
    #Create an instance of our new, parent, Main_Window class 
    #which inherits from the QT generate main_window.py 
    instance = Main_Window()
    
    #Set the parent Main_Window as the active window
    app.setActiveWindow(instance)
    
    #Show the GUI
    instance.show()
    
    #Use exceptions for cleaner exit handeling
    try:
      sys.exit(app.exec_())
    except Exception as e:
      print(e)
