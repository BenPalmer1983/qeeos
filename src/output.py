#!/bin/python3
"""
Output
"""

import os
import time
import numpy
import shutil

from datetime import datetime

from g import g


class output:


  """
  Log
  ######################################################"""

  @staticmethod
  def log(inp, fh = None, verbose=0):
    t = time.time() - g.start
    t = "{0:.4e}".format(t)
    while(len(t) < 10):
      t = " " + t
    if(verbose <= g.verbose['print']):
      if(isinstance(inp, list)):
        for inpn in inp:
          print(inpn)
      else:
        print(inp)
    if(isinstance(inp, list)):
      tofile = ''
      for inpn in inp:
        tofile = tofile + t + "   " + str(inpn) + '\n'
    else:
      tofile = t + "   " + str(inp) + '\n'

    
    if(verbose <= g.verbose['file']):
      g.fh.write(tofile)
      g.fh.flush()

    # Always save if a specific file provided
    if(fh != None):
      fh.write(tofile)

    