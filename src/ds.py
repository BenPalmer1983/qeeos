#!/bin/python3
"""
Dictionaries and Lists
"""

import numpy


class ds:


  @staticmethod
  def dirs():
    return {
    'out': 'out', 
    'template': 'out/template', 
    'relax': 'out/relax', 
    'eos_bm': 'out/eos_bm', 
    'ec_mskp': 'out/ec_mskp', 
    'ec_rfkj': 'out/ec_rfkj', 
    'data': 'out/RESULTS/data', 
    'plots': 'out/RESULTS/plots', 
    }


  @staticmethod
  def units():
    return {
    'energy': 'ev', 
    'length': 'ang', 
    'pressure': 'gpa',
    }


  @staticmethod
  def ifile():
    return {
    # Template etc
    'path': None,
    'template': None,
    # Structure
    'structure': None,
    'a0': None,
    'cxyz': None,
    'labels': None,
    # DFT SETTINGS
    'ecutwfc': 50,
    'ecutrho': 200,
    'kpoints': [9,9,9,1,1,1],
    'kpoints_type': 'automatic',
    'degauss': 0.01,
    # Relax
    'relax': True,
    # EOS BM
    'eos_bm': True,
    'eos_bm_strain': 0.01,
    'eos_bm_steps': 4,     # total = 2 * steps + 1
    'eos_bm_calc': 'scf',
    # EC MSKP
    'ec_mskp': True,
    'ec_mskp_strain': 0.01,
    'ec_mskp_steps': 9,     # total = 1 * steps
    'ec_mskp_calc': 'scf',
    # EC RFKJ
    'ec_rfkj': True,
    'ec_rfkj_strain': 0.01,
    'ec_rfkj_steps': 5,     # total = 1 * steps
    'ec_rfkj_calc': 'scf',
    
    }


  @staticmethod
  def results():
    return {
    # Relaxed
    'relaxed_nat': None, 
    'relaxed_a0': None, 
    'relaxed_uv': None,
    'relaxed_volperatom': None,
    'relaxed_energy_dft': None,     # Total energy (all atoms)v
    'relaxed_energy': None,         # Total energy (all atoms, adjusted)
    'relaxed_epa': None,            # Total energy (per atom, adjusted)
    # EOS BM
    'eos_bm_se': None,
    'eos_bm_ve': None,
    'eos_bm_p': {'e0': 0, 'v0': 0, 'b0': 0, 'b0p': 0,},
    # EC MSKP
    'ec_mskp_se': None,
    'ec_mskp_ec': None,
    'ec_mskp_ec_gpa': None,
    # EC MSKP
    'ec_rfkj_se': None,
    }


  @staticmethod
  def files():
    return {
    'relaxed': None,   # File path
    'eos_bm': None,    # File path
    'ec_mskp': None,   # File paths
    'ec_rfkj': None,   # File paths
    }


  @staticmethod
  def mskp():
    return ['c11_c12', 'c44']



  @staticmethod
  def rfkj():
    return ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9']


  @staticmethod
  def config_cxyz(cxyz):
    cxyz = numpy.asarray(cxyz, dtype=numpy.int32)
    if(cxyz.size == 3):
      return cxyz
    if(cxyz.size == 1):
      cxyz_out = numpy.zeros((3), dtype=numpy.int32) 
      cxyz_out[0] = cxyz[0]
      cxyz_out[1] = cxyz[0]
      cxyz_out[2] = cxyz[0]
      return cxyz_out
 

  @staticmethod
  def kpoints(k):
    if("," in k):
      k = k.split(",")
    for n in range(len(k)):
      k[n] = int(k[n])   
    return k


  @staticmethod
  def ec(ec=None):
    if(ec is None):
      return numpy.zeros((6, 6,), dtype=numpy.float64, order='F')
    ec = numpy.asarray(ec, dtype=numpy.float64, order='F')
    ec_out = numpy.zeros((6, 6,), dtype=numpy.float64, order='F')
    if(ec.ndim == 1 and ec.size == 3):
      ec_out[0,0] = ec[0]
      ec_out[1,1] = ec[0]
      ec_out[2,2] = ec[0]
      ec_out[0,1] = ec[1]
      ec_out[0,2] = ec[1]
      ec_out[1,2] = ec[1]
      ec_out[1,0] = ec[1]
      ec_out[2,0] = ec[1]
      ec_out[2,1] = ec[1]
      ec_out[3,3] = ec[2]
      ec_out[4,4] = ec[2]
      ec_out[5,5] = ec[2]
    elif(ec.ndim == 1 and ec.size == 9):
      ec_out[0,0] = ec[0]
      ec_out[1,1] = ec[1]
      ec_out[2,2] = ec[2]
      ec_out[3,3] = ec[3]
      ec_out[4,4] = ec[4]
      ec_out[5,5] = ec[5]
      ec_out[1,2] = ec[6]
      ec_out[0,2] = ec[7]
      ec_out[0,1] = ec[8]
      ec_out[2,1] = ec[6]
      ec_out[2,0] = ec[7]
      ec_out[1,0] = ec[8]
    elif(ec.ndim == 2 and ec.size == 36):
      ec_out[:,:] = ec[:,:]
    return ec_out




