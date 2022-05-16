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
from ifile import ifile
from pwe import pwe

from template import template

from relax import relax
from eos_bm import eos_bm
from ec_mskp import ec_mskp
from ec_rfkj import ec_rfkj

from process_results import process_results
from plots import plots

class qeeos:


  @staticmethod
  def main():
    display.clear()
    qeeos.setup()
    #######################################
    ifile.run()              # Read input file
    template.run()           # Prepare main template file
    
    relax.run()              # Run vc-relax
    template.make_relaxed()  # Make relaxed template

    eos_bm.run()             # EoS BM PWscf run
    ec_mskp.run()            # EC MSKP PWscf run
    ec_rfkj.run()            # EC RFKJ PWscf run

    process_results.run()
    plots.run()

    #######################################
    qeeos.end()

   

  @staticmethod
  def setup():
    # Start time
    g.start = time.time()

    # Set main output dir
    g.dirs['out'] = os.path.join(os.getcwd(), "out")
    #if(os.path.isdir(g.dirs['out'])):
    #  shutil.rmtree(g.dirs['out'])

    # Fill in full paths
    for k in g.dirs.keys():
      g.dirs[k] = os.path.join(os.getcwd(), g.dirs[k]) 
      os.makedirs(g.dirs[k], exist_ok=True)

    # Log file    
    g.fh = open(os.path.join(g.dirs['out'],'log.txt'), 'w')
    output.log("QEEOS", verbose=0)

    # Clean log file
    pwe.clean_log()

    # Result files
    g.files['relaxed'] = os.path.join(g.dirs['data'], "relaxed.dat")
    g.files['eos_bm'] = os.path.join(g.dirs['data'], "eos_bm.csv")
    g.files['ec_mskp'] = {}
    for stype in g.mskp:
      g.files['ec_mskp'][stype] = os.path.join(g.dirs['data'], "ec_mskp_" + stype + ".csv")
    g.files['ec_rfkj'] = {}
    for stype in g.rfkj:
      g.files['ec_rfkj'][stype] = os.path.join(g.dirs['data'], "ec_rfkj_" + stype + ".csv")


  @staticmethod
  def end():
    g.end(msg=None)




if __name__ == "__main__":
  qeeos.main()    

