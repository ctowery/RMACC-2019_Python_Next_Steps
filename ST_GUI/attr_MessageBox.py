import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class attr_MessageBox(QMessageBox):
  def __init__(self):
    QMessageBox.__init__(self)
    self._min = 0
    self._max = 16777215

  def event(self, e):
    result = QMessageBox.event(self, e)

    self.setMinimumHeight(self._min)
    self.setMaximumHeight(self._max)
    self.setMinimumWidth(self._min)
    self.setMaximumWidth(self._max)
    self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    textEdit = self.findChild(QTextEdit)
    if textEdit is not None:
      textEdit.setMinimumHeight(self._min)
      textEdit.setMaximumHeight(self._max)
      textEdit.setMinimumWidth(self._min)
      textEdit.setMaximumWidth(self._max)
      textEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    return result
  
  def enableSizeGrib(self, grip=False):
    self.setSizeGripEnabled(grip)
  
  ####################
  # Getters
  ####################
  @property
  def min(self):
    return self._min
  
  @property
  def max(self):
    return self._max  
    
  ####################
  # Setters
  ####################
  @min.setter
  def min(self, val):
    self._min = val
    
  @max.setter
  def max(self, val):
    self._max = val