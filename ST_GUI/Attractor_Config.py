import numpy as np
import pandas as pd
import os
import sys

class Attractor_Config():
    """Utility class to open the Attractors configuration file
       and extract the parameters for a chosen attractor type"""
    
    def __init__(self, fName=""):
        self._indexSet=False
        self._df = None
        self._fName = fName
        self._coords = []
        self._params = []
        
        if self.fName is not None:
            self.get_AttractorConfigFile()
    
    def get_AttractorConfigFile(self):
        """Open the Attractors configuration file"""
        if os.path.isfile(self._fName) and os.access(self._fName, os.R_OK):
            self._df = pd.read_csv(self._fName)
        else:
            print("ERROR: The file is either missing or it's not readable")
            sys.exit(1)
    
    def getAttractor(self, fxn):
        """Get the configuration for the desired attractor"""
        if not self._indexSet:
          self._df.set_index('Attractor', inplace=True) 
          self._indexSet = True
        a = self._df.loc[fxn]

        self._coords = [a.iloc[1], a.iloc[2], a.iloc[3]]

        self._params = np.array([])
        for v in range(4, np.size(a)):
            self._params = np.append(self._params, a.iloc[v])
    
    def getAttractorList(self):
      attrList = self._df['Attractor'].unique()
      return sorted(attrList)
    
    @property
    def coords(self):
        """Getter - return coords"""
        return self._coords
    
    @property
    def df(self):
        """Getter - return df"""
        return self._df

    @property
    def fName(self):
        """Getter - return fName """
        return self._fName
    
    @property
    def params(self):
        """Getter - return params"""
        return self._params

    
    @df.setter
    def df(self, val):
        """Setter - sets df"""
        self._df = val
        
    @coords.setter
    def coords(self, val):
        """Setter - sets coords"""
        self._coords = val
        
    @fName.setter
    def fName(self, val):
        """Setter - sets fName"""
        self._fName = val
        
    @params.setter
    def fName(self, val):
        """Setter - sets params"""
        self._params = val
    