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



class eos_bm:


  @staticmethod
  def run():
    if(not g.ifile['eos_bm']):
      return False
    output.log("Run PWscf for EoS BM", verbose=0)

    # Get total strain and steps
    eos_strain = g.ifile['eos_bm_strain']
    eos_steps = g.ifile['eos_bm_steps']

    # Make
    g.results['eos_bm_se'] = numpy.zeros((2 * eos_steps + 1, 2,), dtype=numpy.float64)
    g.results['eos_bm_ve'] = numpy.zeros((2 * eos_steps + 1, 2,), dtype=numpy.float64)
    
    # Load template
    eos = template.load_relaxed()
    uv = eos.get_cp_array()

    # Prepare files
    files = []
    n = 0
    for i in range(-eos_steps, eos_steps+1):
      n_str = str(n + 1)
      while(len(n_str)<4):
        n_str = "0" + n_str

      # Make and store strain
      s = eos_strain * (i / eos_steps)
      g.results['eos_bm_se'][n, 0] = s

      # Transform
      d = transforms.eos(s)
      uv_new = numpy.matmul(d, uv)

      # Update pw obj
      eos.set_prefix()
      eos.set_cp_arr(uv_new)
      if(g.ifile['eos_bm_calc'] == 'relax'):
        eos.set_calculation("relax")
      else:
        eos.set_calculation("scf")
      eos.save("eos_bm_" + n_str + ".in", g.dirs['eos_bm'])
      files.append(os.path.join(g.dirs['eos_bm'], "eos_bm_" + n_str + ".in"))

      # Increment
      n = n + 1

    

    # Run PWscf
    output.log("Running PWscf", verbose=0)
    out = pwe.run(files)

    
    output.log("Read EoS BM results", verbose=0)
    # Read results
    for n in range(len(out)):
      o = pwout_read.read(out[n][1])
      vol = units.convert('BOHR3', 'ANG3', o['vpa'])
      energy = adjust_energy.run(o['energy'], o['labels'], unit_in='ry', epa=True)

      g.results['eos_bm_se'][n, 1] = energy
      g.results['eos_bm_ve'][n, 0] = vol
      g.results['eos_bm_ve'][n, 1] = energy

    # Save to file
    output.log("Save EoS BM results to file", verbose=0)
    numpy.savetxt(g.files['eos_bm'], g.results['eos_bm_ve'], delimiter=",")
    

