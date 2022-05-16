#!/bin/python3

import os
import sys
import numpy
import time
import shutil

from g import g
from ds import ds

from display import display
from output import output
from units import units




class process_results:


  @staticmethod
  def run():
    output.log("", verbose=0)
    output.log("", verbose=0)
    output.log("Process Results", verbose=0)
    output.log("##########################", verbose=0)
     
    if(not os.path.isfile(g.files['relaxed'])):
      g.end("No relaxed data - unable to continue.")

    # Clear output
    g.output =            '#################################################################\n'
    g.output = g.output + '#                       QEEOS Results                           #\n'
    g.output = g.output + '#################################################################\n'
    g.output = g.output + '\n'

    process_results.relaxed()
    process_results.eos_bm()
    process_results.ec_mskp()
    process_results.ec_rfkj()

    fh = open(os.path.join(g.dirs['out'], "output.txt"), 'w')
    fh.write(g.output)
    fh.close()
    


  

  @staticmethod
  def relaxed():
    # Load data from file    
    output.log("Relaxed", verbose=0)
    output.log("Loading data from file.", verbose=0)
    d = []
    fh = open(g.files['relaxed'], 'r')
    for line in fh:
      d.append(line.strip())
    fh.close()
    nat = float(d[0])
    a0 = float(d[1])
    a0_scaled = float(d[2])
    a0_scaled_bohr = float(d[3])
    uv = numpy.zeros((3,3,), dtype=numpy.float64,)
    n = 4
    for i in range(3):
      for j in range(3):
        uv[i,j] = float(d[n])
        n = n + 1
    vpa = float(d[13])
    relaxed_energy_dft = float(d[14])
    relaxed_energy = float(d[15])
    relaxed_epa = float(d[16])

    g.output = g.output + 'Relaxed Cell\n'
    g.output = g.output + '***********************\n'
    g.output = g.output + '{:20s} {:12.6f}\n'.format("nat", nat)
    g.output = g.output + '{:20s} {:12.6f}\n'.format("a0", a0)
    g.output = g.output + '{:20s} {:12.6f} {:12.6f} {:12.6f}\n'.format("Relaxed UV", uv[0,0], uv[0,1], uv[0,2])
    g.output = g.output + '{:20s} {:12.6f} {:12.6f} {:12.6f}\n'.format("Relaxed UV", uv[1,0], uv[1,1], uv[1,2])
    g.output = g.output + '{:20s} {:12.6f} {:12.6f} {:12.6f}\n'.format("Relaxed UV", uv[2,0], uv[2,1], uv[2,2])
    g.output = g.output + '{:20s} {:12.6f}\n'.format("Vol per atom", vpa)
    g.output = g.output + '{:20s} {:12.6f}\n'.format("Energy (DFT)", relaxed_energy_dft)
    g.output = g.output + '{:20s} {:12.6f}\n'.format("Energy (adjusted)", relaxed_energy)
    g.output = g.output + '{:20s} {:12.6f}\n'.format("Energy per atom", relaxed_epa)
    g.output = g.output + '\n'

 
    g.results['relaxed_a0'] = a0
    g.results['relaxed_uv'] = uv
    g.results['relaxed_volperatom'] = vpa
  



  """#######################################
  EOS BM
  #######################################"""

  @staticmethod
  def eos_bm():
    output.log("EoS BM", verbose=0)

    g.output = g.output + 'EoS BM\n'
    g.output = g.output + '***********************\n'

    if(not os.path.isfile(g.files['eos_bm'])):
      output.log("...no EoS BM data file...", verbose=0)
      g.output = g.output + 'NO DATA\n'
      g.output = g.output + '\n'
      return False

    # Load data from file
    output.log("Loading data from file.", verbose=0)
    g.results['eos_bm_ve'] = numpy.loadtxt(g.files['eos_bm'], dtype=numpy.float64, delimiter=",")

    # Fit
    poly = numpy.polyfit(g.results['eos_bm_ve'][:,0], g.results['eos_bm_ve'][:,1], 2)

    if(poly[0] == 0):
      poly[0] = 1.0e-20
    v0 = (-1 * poly[1]) / (2 * poly[0])
    e0 = (poly[0] * v0 * v0) + (poly[1] * v0) + poly[2]
    b0 = 2.0 * poly[0] * v0
    b0p = 2.0
    
    output.log("e0 " + str(e0), verbose=0)
    output.log("v0 " + str(v0), verbose=0)
    output.log("b0 " + str(b0), verbose=0)
    output.log("b0p " + str(b0p), verbose=0)

    g.results['eos_bm_p']['e0'] = e0
    g.results['eos_bm_p']['v0'] = v0
    g.results['eos_bm_p']['b0'] = b0
    g.results['eos_bm_p']['b0p'] = b0p
    b0_gpa = units.convert("EV/ANG3", "GPA", b0)

    g.output = g.output + '{:20s} {:12.6f}\n'.format("e0", e0)
    g.output = g.output + '{:20s} {:12.6f}\n'.format("v0", v0)
    g.output = g.output + '{:20s} {:12.6f} ({:12.6f} GPa)\n'.format("b0", b0, b0_gpa)
    g.output = g.output + '{:20s} {:12.6f}\n'.format("b0p", b0p)
    g.output = g.output + '\n'





  """#######################################
  EC MSKP
  #######################################"""

  @staticmethod
  def ec_mskp():
    output.log("EC MSKP", verbose=0)

    g.output = g.output + 'EC MSKP\n'
    g.output = g.output + '***********************\n'

    for stype in g.mskp:
      if(not os.path.isfile(g.files['ec_mskp'][stype])):
        output.log("...no EC MSKP data file...", verbose=0)
        g.output = g.output + 'NO DATA\n'
        g.output = g.output + '\n'
        return False

    
    output.log("Loading data from files.", verbose=0)
    coeffs = {}
    for stype in g.mskp:
      # Load data from file
      g.results['ec_mskp_se'][stype] = numpy.loadtxt(g.files['ec_mskp'][stype], dtype=numpy.float64, delimiter=",")

      # Fit
      poly = numpy.polyfit(g.results['ec_mskp_se'][stype][:,0], g.results['ec_mskp_se'][stype][:,1], 2)
      coeffs[stype] = poly[0]

    #v0 = g.results['eos_bm_p']['v0']
    v0 = g.results['relaxed_volperatom']
    b0 = g.results['eos_bm_p']['b0']

    A = numpy.zeros((3, 3,), dtype=numpy.float64)
    A[0,0] = 1.0
    A[0,1] = 2.0
    A[1,0] = 1.0
    A[1,1] = -1.0
    A[2,2] = 1.0
    c = numpy.asarray([3.0*b0, coeffs['c11_c12'] / v0, (2.0 * coeffs['c44']) / v0])
    A_inv = numpy.linalg.inv(A)
    b = numpy.matmul(A_inv, c)

    g.results['ec_mskp_ec'] = ds.ec(b)
    g.results['ec_mskp_ec_gpa'] = units.convert('EV/ANG3', 'GPA', g.results['ec_mskp_ec'])

    g.output = g.output + 'Stiffness Matrix\n'
    for i in range(6):
      for j in range(6):
        g.output = g.output + '{:8.3f} '.format(g.results['ec_mskp_ec'][i, j])
      g.output = g.output + '    '
      for j in range(6):
        g.output = g.output + '{:8.3f} '.format(g.results['ec_mskp_ec_gpa'][i, j])
      g.output = g.output + '\n'
    g.output = g.output + '\n'




  """#######################################
  EC RFKJ
  #######################################"""

  @staticmethod
  def ec_rfkj():
    output.log("EC RFKJ", verbose=0)

    g.output = g.output + 'EC RFKJ\n'
    g.output = g.output + '***********************\n'

    for stype in g.rfkj:
      if(not os.path.isfile(g.files['ec_rfkj'][stype])):
        output.log("...no EC RFKJ data file...", verbose=0)
        g.output = g.output + 'NO DATA\n'
        g.output = g.output + '\n'
        return False


    
    output.log("Loading data from files.", verbose=0)
    coeffs = []
    for stype in g.rfkj:
      # Load data from file
      g.results['ec_rfkj_se'][stype] = numpy.loadtxt(g.files['ec_rfkj'][stype], dtype=numpy.float64, delimiter=",")

      # Fit
      poly = numpy.polyfit(g.results['ec_rfkj_se'][stype][:,0], g.results['ec_rfkj_se'][stype][:,1], 2)
      coeffs.append(poly[0])

    # Get volume
    #v0 = g.results['eos_bm_p']['v0']
    v0 = g.results['relaxed_volperatom']

    A = numpy.zeros((9,9,), dtype=numpy.float64)
    A[0,0] = v0/2
    A[1,1] = v0/2
    A[2,2] = v0/2
    A[3,3] = 2*v0
    A[4,4] = 2*v0
    A[5,5] = 2*v0
    A[6,6] = -1.0*v0
    A[7,7] = -1.0*v0
    A[8,8] = -1.0*v0
    A[6,0] = v0 / 2
    A[6,1] = v0 / 2
    A[7,0] = v0 / 2
    A[7,2] = v0 / 2
    A[8,1] = v0 / 2
    A[8,2] = v0 / 2
    c = numpy.asarray(coeffs, dtype=numpy.float64)
    A_inv = numpy.linalg.inv(A)
    b = numpy.matmul(A_inv, c)

    g.results['ec_rfkj_ec'] = ds.ec(b)
    g.results['ec_rfkj_ec_gpa'] = units.convert('EV/ANG3', 'GPA', g.results['ec_rfkj_ec'])

    g.output = g.output + 'Stiffness Matrix\n'
    for i in range(6):
      for j in range(6):
        g.output = g.output + '{:8.3f} '.format(g.results['ec_rfkj_ec'][i, j])
      g.output = g.output + '    '
      for j in range(6):
        g.output = g.output + '{:8.3f} '.format(g.results['ec_rfkj_ec_gpa'][i, j])
      g.output = g.output + '\n'
    g.output = g.output + '\n'






  @staticmethod
  def bm_calc(p, V):
    V0 = p[0]
    E0 = p[1]
    B0 = p[2]
    B0P = p[3]
    if(V0 == 0.0):
      V0 = 1.0e-20
    try:
      eta = (V/V0)**(1.0/3.0)
    except:
      eta = 1.0e10
    return E0 + (9.0/16.0) * (B0 * V0) * ((eta*eta - 1)*(eta*eta - 1)) * (6.0 + B0P * (eta * eta - 1) - 4.0 * eta * eta ) 

