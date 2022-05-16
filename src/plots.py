#!/bin/python3

import os
import sys
import numpy
import time
import shutil
import matplotlib.pyplot as plt

from g import g
from ds import ds

from display import display
from output import output
from units import units




class plots:


  @staticmethod
  def run():
    output.log("", verbose=0)
    output.log("", verbose=0)
    output.log("Plots", verbose=0)
    output.log("##########################", verbose=0)

    plots.eos_bm()
    plots.ec_mskp()





  @staticmethod
  def eos_bm():
    path = os.path.join(g.dirs['plots'], 'eos.eps')

    v = numpy.copy(g.results['eos_bm_ve'][:,0])
    e = numpy.copy(g.results['eos_bm_ve'][:,1])

    e0 = g.results['eos_bm_p']['e0']
    v0 = g.results['eos_bm_p']['v0']
    b0 = g.results['eos_bm_p']['b0']
    b0p = g.results['eos_bm_p']['b0p']

    v_fit = numpy.linspace(v[0], v[-1], 1001, dtype=numpy.float64)
    e_fit = plots.bm_calc([v0, e0, b0, b0p], v_fit)


    plt.clf()    
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')
    fig, axs = plt.subplots(1, 1, figsize=(12,9))
    fig.tight_layout(pad=5.0)
    fig.suptitle('Equation of State')        
    plt.plot(v[:], e[:], color='k',  marker="x", ls='')
    plt.plot(v_fit[:], e_fit[:], color='k', ls='solid')
    axs.set_xlabel('Volume (ang^3/atom)')
    axs.set_ylabel('Energy (ev/atom)')
    plt.savefig(path)
    plt.close('all')



  @staticmethod
  def ec_mskp():
    for stype in g.mskp:
      s = numpy.copy(g.results['ec_mskp_se'][stype][:, 0])
      e = numpy.copy(g.results['ec_mskp_se'][stype][:, 1])
      plots.ec_mskp_inner(stype, s, e)

  @staticmethod
  def ec_mskp_inner(stype, s, e):  
    title = "MSKP Elastic Constant Fit " + stype
    path = os.path.join(g.dirs['plots'], 'ec_mskp_' + stype + '.eps')
    plt.clf()    
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')
    fig, axs = plt.subplots(1, 1, figsize=(12,9))
    fig.tight_layout(pad=5.0)
    fig.suptitle(title)        
    plt.plot(s[:], e[:], color='k',  marker="x", ls='')
    axs.set_xlabel('Strain')
    axs.set_ylabel('Energy (ev/atom)')
    plt.savefig(path)
    plt.close('all')





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
