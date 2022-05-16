#!/bin/python3
"""
Input File
"""

import os
import sys
import numpy

from g import g
from ds import ds
from output import output
from std import std
from units import units

class ifile:

  @staticmethod
  def run():

    # Check file specified and that it exists
    if(len(sys.argv)<2):
      g.end("ERROR.  Please specifiy input file.")
    if(not os.path.isfile(sys.argv[1])):
      g.end("ERROR.  Input file does not exist.")

    # Load file 
    g.ifile['path'] = os.path.join(os.getcwd(), sys.argv[1])   
    ifile.load(g.ifile['path'])


  @staticmethod
  def load(file_path):
    output.log("Read input file", verbose=0)

    #   Default units
    ###############################################################
    input_units = {'energy': 'ev', 'length': 'ang', 'pressure': 'gpa',}

    #   Read file
    ###############################################################

    d = std.read(file_path)

    #   Loop over lines in file
    ###############################################################
    for line in d:
      f = line.split(" ")
      f[0] = f[0].upper()



      if(f[0] == "#TEMPLATE"):
        template_file = os.path.abspath(f[1])
        if(os.path.isfile(template_file)):
          g.ifile['template'] = template_file
        else:
          g.end("ERROR.  Template file does not exist.")



      elif(f[0] == "#CONFIG"):
        a0_units = None
        a0 = None
        for fn in f:
          fn = fn.split("=")
          if(fn[0].upper() == "STRUCTURE"):
            g.ifile['structure'] = fn[1].lower()
          elif(fn[0].upper() == "A0"):
            a0 = float(fn[1])
          elif(fn[0].upper() == "UNITS"):
            a0_units = fn[1]
          elif(fn[0].upper() == "CXYZ"):
            g.ifile['cxyz'] = ds.config_cxyz(fn[1].split(","))
          elif(fn[0].upper() == "LABELS"):
            g.ifile['labels'] = fn[1].split(",")
        if(a0 is not None):
          if(a0_units is not None):
            g.ifile['a0'] = units.convert(a0_units, 'angs', a0)
          else:
            g.ifile['a0'] = a0



      elif(f[0] == "#DFTSETTINGS"):
        for fn in f:
          fn = fn.split("=")
          if(fn[0].upper() == "ECUTWFC"):
            g.ifile['ecutwfc'] = float(fn[1])
          elif(fn[0].upper() == "ECUTRHO"):
            g.ifile['ecutrho'] = float(fn[1])
          elif(fn[0].upper() == "KPOINTS"):
            g.ifile['kpoints'] = ds.kpoints(fn[1])
          elif(fn[0].upper() == "DEGAUSS"):
            g.ifile['degauss'] = float(fn[1])



      elif(f[0] == "#RELAX"):
        for fn in f:
          fn = fn.split("=")
          if(fn[0].upper() == "RUN"):
            g.ifile['relax'] = True
            if(fn[1][0].upper() == "F"):
              g.ifile['relax'] = False



      elif(f[0] == "#EOS_BM"):
        for fn in f:
          fn = fn.split("=")
          if(fn[0].upper() == "RUN"):
            g.ifile['eos_bm'] = True
            if(fn[1][0].upper() == "F"):
              g.ifile['eos_bm'] = False              
          elif(fn[0].upper() == "STRAIN"):
            g.ifile['eos_bm_strain'] = float(fn[1])
          elif(fn[0].upper() == "STEPS"):
            g.ifile['eos_bm_steps'] = int(fn[1])
          elif(fn[0].upper() == "CALC"):
            g.ifile['eos_bm_calc'] = fn[1].lower()



      elif(f[0] == "#EC_MSKP"):
        for fn in f:
          fn = fn.split("=")
          if(fn[0].upper() == "RUN"):
            g.ifile['ec_mskp'] = True
            if(fn[1][0].upper() == "F"):
              g.ifile['ec_mskp'] = False              
          elif(fn[0].upper() == "STRAIN"):
            g.ifile['ec_mskp_strain'] = float(fn[1])
          elif(fn[0].upper() == "STEPS"):
            g.ifile['ec_mskp_steps'] = int(fn[1])
          elif(fn[0].upper() == "CALC"):
            g.ifile['ec_mskp_calc'] = fn[1].lower()




      elif(f[0] == "#EC_RFKJ"):
        for fn in f:
          fn = fn.split("=")
          if(fn[0].upper() == "RUN"):
            g.ifile['ec_rfkj'] = True
            if(fn[1][0].upper() == "F"):
              g.ifile['ec_rfkj'] = False              
          elif(fn[0].upper() == "STRAIN"):
            g.ifile['ec_rfkj_strain'] = float(fn[1])
          elif(fn[0].upper() == "STEPS"):
            g.ifile['ec_rfkj_steps'] = int(fn[1])
          elif(fn[0].upper() == "CALC"):
            g.ifile['ec_rfkj_calc'] = fn[1].lower()



      elif(f[0] == "#DFTADJUST"):
        for fn in f:
          if("=" in fn):
            print(fn)
            fn = fn.split("=")
            label = fn[0].strip().upper()
            fd = fn[1].split(',')
            if(len(fd) == 4):
              dft_energy = units.convert(fd[1], 'ev', float(fd[0]))
              known_energy = units.convert(fd[3], 'ev', float(fd[2]))
              g.adjust[label] = known_energy - dft_energy












