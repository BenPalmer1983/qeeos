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
from template import template
from pwscf_inout import pwscf_input
from pwscf_inout import pwscf_output
from pwout_read import pwout_read
from pwe import pwe
from transforms import transforms
from adjust_energy import adjust_energy




class ec_rfkj:


  @staticmethod
  def run():
    if(not g.ifile['ec_rfkj']):
      return False
    output.log("Run PWscf for EC RFKJ", verbose=0)

    # Get total strain and steps
    strain = g.ifile['ec_rfkj_strain']
    steps = g.ifile['ec_rfkj_steps']

    # Make
    g.results['ec_rfkj_se'] = {}
    
    # Load template
    ec = template.load_relaxed()
    uv = ec.get_cp_array()

    # Prepare files
    files = []

    for stype in g.rfkj:
      g.results['ec_rfkj_se'][stype] = numpy.zeros((2*steps+1, 2,), dtype=numpy.float64)
      n = 0
      #for i in range(steps):
      for i in range(-steps, steps+1):
        n_str = str(n + 1)
        while(len(n_str)<4):
          n_str = "0" + n_str

        # Make and store strain
        s = strain * (i / steps)
        g.results['ec_rfkj_se'][stype][n, 0] = s

        # Transform
        d = transforms.ec_rfkj(s, stype)
        uv_new = numpy.matmul(d, uv)
      
        # Update pw obj
        ec.set_prefix()
        ec.set_cp_arr(uv_new)
        if(g.ifile['ec_rfkj_calc'] == 'relax'):
          ec.set_calculation("relax")
        else:
          ec.set_calculation("scf")
        ec.save("ec_rfkj_" + stype + "_" + n_str + ".in", g.dirs['ec_rfkj'])
        files.append(os.path.join(g.dirs['ec_rfkj'], "ec_rfkj_" + stype + "_" + n_str + ".in"))

        # Increment
        n = n + 1

    # Run PWscf
    output.log("Running PWscf", verbose=0)
    out = pwe.run(files)

    # Read results
    output.log("Read EC RFKJ results", verbose=0)
    for stype in g.rfkj:
      n = 0
      for i in range(-steps, steps+1):
        o = pwout_read.read(out[n][1])
        vol = units.convert('BOHR3', 'ANG3', o['vpa'])
        energy = adjust_energy.run(o['energy'], o['labels'], unit_in='ry', epa=True)
        g.results['ec_rfkj_se'][stype][n, 1] = energy
        n = n + 1
    
    # Save to file
    output.log("Save EC RFKJ results to file", verbose=0)
    for stype in g.rfkj:
      numpy.savetxt(g.files['ec_rfkj'][stype], g.results['ec_rfkj_se'][stype], delimiter=",")




