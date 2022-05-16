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




class ec_mskp:


  @staticmethod
  def run():
    if(not g.ifile['ec_mskp']):
      return False
    output.log("Run PWscf for EC MSKP", verbose=0)

    # Get total strain and steps
    ec_mskp_strain = g.ifile['ec_mskp_strain']
    ec_mskp_steps = g.ifile['ec_mskp_steps']

    # Make
    g.results['ec_mskp_se'] = {}
    
    # Load template
    ec = template.load_relaxed()
    uv = ec.get_cp_array()

    # Prepare files
    files = []

    for stype in g.mskp:
      g.results['ec_mskp_se'][stype] = numpy.zeros((ec_mskp_steps, 2,), dtype=numpy.float64)
      n = 0
      for i in range(ec_mskp_steps):
        n_str = str(n + 1)
        while(len(n_str)<4):
          n_str = "0" + n_str

        # Make and store strain
        s = ec_mskp_strain * (i / ec_mskp_steps)
        g.results['ec_mskp_se'][stype][n, 0] = s

        # Transform
        d = transforms.ec_mskp(s, stype)
        uv_new = numpy.matmul(d, uv)
      
        # Update pw obj
        ec.set_prefix()
        ec.set_cp_arr(uv_new)
        if(g.ifile['ec_mskp_calc'] == 'relax'):
          ec.set_calculation("relax")
        else:
          ec.set_calculation("scf")
        ec.save("ec_mskp_" + stype + "_" + n_str + ".in", g.dirs['ec_mskp'])
        files.append(os.path.join(g.dirs['ec_mskp'], "ec_mskp_" + stype + "_" + n_str + ".in"))

        # Increment
        n = n + 1

    # Run PWscf
    output.log("Running PWscf", verbose=0)
    out = pwe.run(files)

    # Read results
    output.log("Read EC MSKP results", verbose=0)
    n = 0
    for stype in g.mskp:
      m = 0
      for i in range(ec_mskp_steps):
        o = pwout_read.read(out[n][1])
        vol = units.convert('BOHR3', 'ANG3', o['vpa'])
        energy = adjust_energy.run(o['energy'], o['labels'], unit_in='ry', epa=True)
        g.results['ec_mskp_se'][stype][m, 1] = energy
        m = m + 1
        n = n + 1
    
    # Save to file
    output.log("Save EC MSKP results to file", verbose=0)
    for stype in g.mskp:
      numpy.savetxt(g.files['ec_mskp'][stype], g.results['ec_mskp_se'][stype], delimiter=",")




