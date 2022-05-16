#!/bin/python3

import os
import sys
import numpy
import time
import shutil

from g import g
from ds import ds

class transforms:

  @staticmethod
  def eos(sigma):
    d = numpy.zeros((3,3,), dtype=numpy.float64)
    d[0,0] = 1.0 + sigma
    d[1,1] = 1.0 + sigma
    d[2,2] = 1.0 + sigma
    return d


  @staticmethod
  def ec_mskp(sigma, stype):
    d = numpy.zeros((3,3,), dtype=numpy.float64)
    if(stype == 'c11_c12'):
      d[0,0] = 1.0 + sigma
      d[1,1] = 1.0 - sigma
      d[2,2] = 1.0 + sigma**2 / (1.0 - sigma**2)     
    elif(stype == 'c44'):
      d[0,0] = 1.0
      d[1,1] = 1.0
      d[2,2] = 1.0 + sigma**2 / (4.0 - sigma**2)    
      d[0,1] = sigma / 2.0 
      d[1,0] = sigma / 2.0
    return d

  @staticmethod
  def ec_rfkj(sigma, stype):
    d = numpy.zeros((3,3,), dtype=numpy.float64)
    if(stype == 'd1'):
      d[0,0] = 1.0 + sigma
      d[1,1] = 1.0
      d[2,2] = 1.0     
    elif(stype == 'd2'):
      d[0,0] = 1.0
      d[1,1] = 1.0 + sigma
      d[2,2] = 1.0   
    elif(stype == 'd3'):
      d[0,0] = 1.0 
      d[1,1] = 1.0
      d[2,2] = 1.0  + sigma
    elif(stype == 'd4'):
      u = (1.0 - sigma**2)**(1.0/3.0)
      d[0,0] = 1.0 / u
      d[1,1] = 1.0 / u
      d[2,2] = 1.0 / u
      d[1,2] = sigma / u
      d[2,1] = sigma / u
    elif(stype == 'd5'):
      u = (1.0 - sigma**2)**(1.0/3.0)
      d[0,0] = 1.0 / u
      d[1,1] = 1.0 / u
      d[2,2] = 1.0 / u
      d[0,2] = sigma / u
      d[2,0] = sigma / u
    elif(stype == 'd6'):
      u = (1.0 - sigma**2)**(1.0/3.0)
      d[0,0] = 1.0 / u
      d[1,1] = 1.0 / u
      d[2,2] = 1.0 / u
      d[0,1] = sigma / u
      d[1,0] = sigma / u
    elif(stype == 'd7'):
      u = (1.0 - sigma**2)**(1.0/3.0)
      d[0,0] = (1.0 + sigma) / u
      d[1,1] = (1.0 - sigma) / u
      d[2,2] = 1.0 / u      
    elif(stype == 'd8'):
      u = (1.0 - sigma**2)**(1.0/3.0)
      d[0,0] = (1.0 + sigma) / u
      d[1,1] = 1.0 / u
      d[2,2] = (1.0 - sigma) / u    
    elif(stype == 'd9'):
      u = (1.0 - sigma**2)**(1.0/3.0)
      d[0,0] = 1.0 / u
      d[1,1] = (1.0 + sigma) / u 
      d[2,2] = (1.0 - sigma) / u    
    return d












