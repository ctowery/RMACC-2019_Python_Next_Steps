import numpy as np
import pandas as pd
import datashader as ds
from datashader import transfer_functions as tf
from datashader import utils
from datashader.colors import inferno, viridis
from numba import jit, jitclass
from math import sin, cos, sqrt, fabs
from numba import int32, float32
import time
import os
import sys
from colorcet import palette

class Attractors(object):
    """ """
    def __init__(self, *args, **kwargs):
        self.first = False
        
        self.parse_kwargs(**kwargs)
        self.parse_coords()
        self.parse_avars()
        #self._numIters = 100000#00
        self._attrType = ''
        self._aOrientation = ''
        self._cmap = 'bgy'
        self._res = 400

    def parse_kwargs(self, **kwargs):
        svd_opts = ['fxn', 'coords', 'avars']
        
        for key in svd_opts:
          if key in kwargs:
            setattr(self, key, kwargs[key])

    def parse_coords(self):
        self.x = self.coords[0]
        self.y = self.coords[1]
        self.z = self.coords[2]

    def parse_avars(self):
        self.a = self.avars[0]
        self.b = self.avars[1]
        self.c = self.avars[2]
        self.d = self.avars[3]
        self.e = self.avars[4]
        self.f = self.avars[5]

    def Bedhead(self,x,y,z):
      a = self.a
      b = self.b
      Xn = np.sin(x*y/b)*y + np.cos(a*x-y)
      Yn = x + sin(y)/b
      Zn = 0.0
      return Xn,Yn,Zn
      
    def Clifford(self,x,y,z):
      a = self.a
      b = self.b
      c = self.c
      d = self.d
      Xn = np.sin(a * y) + c * np.cos(a * x)
      Yn = np.sin(b * x) + d * np.cos(b * y)
      Zn = 0.0
      return Xn,Yn,Zn
           
    def De_Jong(self,x,y,z):
      Xn = sin(self.a * y) - cos(self.b * x)
      Yn = sin(self.c * x) - cos(self.d * y)
      Zn = 0.0
      return Xn, Yn, Zn       
           
           
           
    def Pickover(self,x,y,z): 
      Xn =  np.sin(self.a*y) - z*np.cos(self.b*x)
      Yn =  z*np.sin(self.c*x) - np.cos(self.d*y)
      Zn =  np.sin(x) 
      return Xn, Yn, Zn

    def Fractal_Dream(self, x, y, z):
      a = self.a
      b = self.b
      c = self.c
      d = self.d
      Xn = np.sin(y*b)+c*np.sin(x*b)
      Yn = np.sin(x*a)+d*np.sin(y*a)
      Zn = 0.0
      return Xn,Yn,Zn

    def GM_G(self, x, mu):
      return mu * x + 2 * (1 - mu) * x**2 / (1.0 + x**2)

    def Gumowski_Mira(self,x, y, z):
      a = self.a
      b = self.b
      mu = self.c
      
      Xn = y + a*(1 - b*y**2)*y  +  self.GM_G(x, mu)
      Yn = -x + self.GM_G(Xn, mu)
      Zn = 0.0
      return Xn, Yn, Zn

    def Hopalong(self, x, y, z):
      a = self.a
      b = self.b
      c = self.c
      Xn = y - np.sqrt(np.fabs(b * x - c)) * np.sign(x)
      Yn = a - x
      Zn = 0.0
      return Xn,Yn,Zn
   
    def Icon(self, x, y, z):#a, b, g, om, l, d,
      a = self.a
      b = self.b
      g = self.c 
      om = self.d
      l = self.e
      d = np.int(self.f)
      zzbar = x*x + y*y
      p = a*zzbar + l
      zreal, zimag = x, y
      for i in range(1, d-1):
        za, zb = zreal * x - zimag * y, zimag * x + zreal * y
        zreal, zimag = za, zb
      
      zn = x*zreal - y*zimag
      p += b*zn
      
      Xn = p*x + g*zreal - om*y
      Yn = p*y - g*zimag + om*x
      Zn = 0.0
      return Xn, Yn, Zn   
        
    def Lorenz(self,x,y,z):
      a = self.a
      b = self.b
      c = self.c
      d = self.d
      Xn = x+a*d*(y-x)
      Yn = y+d*(b*x-y-z*x)
      Zn = z+d*(x*y-c*z)
      return Xn, Yn, Zn
        
    def Lorenz84(self,x,y,z):
      a = self.a
      b = self.b
      f = self.c
      g = self.d
      d = self.e
      Xn = x+d*(-a*x-y*y-z*z+a*f)
      Yn = y+d*(-y+x*y-b*x*z+g)
      Zn = z+d*(-z+b*x*y+x*z)
      return Xn, Yn, Zn
        
    def Poly_A(self,x,y,z):
      p0 = self.a
      p1 = self.b
      p2 = self.c 
      Xn = p0+y-z*y
      Yn = p1+z-x*z
      Zn = p2+x-y*x 
      return Xn,Yn,Zn
  
    def Svensson(self,x, y,z):
      a = self.a
      b = self.b
      c = self.c
      d = self.d
      Xn = d * np.sin(a * x) - np.sin(b * y)
      Yn = c * np.cos(a * x) + np.cos(b * y)
      Zn = 0.0
      return Xn, Yn, Zn
      
   

    def trajectory(self):
        fxn_dispatch = {'Bedhead':self.Bedhead,
                        'Clifford':self.Clifford,
                        'De_Jong':self.De_Jong, 
                        'De_Jong1':self.De_Jong, 
                        'Fractal_Dream':self.Fractal_Dream,
                        'Gumowski_Mira':self.Gumowski_Mira,
                        'Hopalong':self.Hopalong,
                        'Icon':self.Icon,
                        'Lorenz':self.Lorenz, 
                        'Lorenz84':self.Lorenz84, 
                        'Pickover':self.Pickover, 
                        'Poly_A':self.Poly_A,
                        'Svensson':self.Svensson,
                        }
 
        x, y, z = np.zeros(self._numIters), np.zeros(self._numIters), np.zeros(self._numIters)
        x[0], y[0], z[0] = self.x, self.y, self.z
        for i in np.arange(self._numIters-1):
            x[i+1], y[i+1], z[i+1] = fxn_dispatch[self.fxn](x[i], y[i], z[i])
        return pd.DataFrame(dict(x=x, y=y, z=z))

    def dsplot(self): 
        """Return a Datashader image by collecting `n` trajectory points for the given attractor `fn`"""
        cmap = palette[self._cmap][::-1]
        start = time.time()
        df  = self.trajectory()
        end = time.time()
        self._timeCalc = end - start
        start = time.time()
        cvs = ds.Canvas(plot_width = self._res, plot_height = self._res)
        
        if self._aOrientation == 'XY':
          agg = cvs.points(df, 'x', 'y')
        elif self._aOrientation == 'XZ':
          agg = cvs.points(df, 'x', 'z')
        else:
          agg = cvs.points(df, 'y', 'z')

        img = tf.shade(agg, cmap=cmap)
        end = time.time()
        self._timeRender = end - start
        self.saveImg(img=img,tmp=True)
        return img
    
    '''
    def plot(self):
        """Plot the given attractor `fn` once per provided set of arguments."""
        return tf.Images(self.dsplot())
    '''
    
    def saveImg(self,img, fName='', tmp=False):
      if tmp:
        fName = 'tempAttr'
      
      utils.export_image(img=img,filename=fName, fmt=".png", background=None)

        
    @property
    def attrType(self):
      return self._attrType
    
    @property
    def aOrientation(self):
      return self._aOrientation
        
    @property
    def cmap(self):
      """Getter - return cmap"""
      return self._cmap
  
    @property
    def numIters(self):
      return self._numIters
  
    @property
    def res(self):
      return self._res
    
    @cmap.setter
    def cmap(self, val):
      """Setter - sets cmap"""
      self._cmap = val
      
    @numIters.setter
    def numIters(self, val):
      self._numIters = val
      
    @attrType.setter  
    def attrType(self, val):
      self._attrType = val
      
    @aOrientation.setter
    def aOrientation(self, val):
      self._aOrientation = val
      
    @res.setter
    def res(self, val):
      self._res = val