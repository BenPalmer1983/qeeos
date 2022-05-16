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
from adjust_energy import adjust_energy

class relax:


  @staticmethod
  def run():
    if(not g.ifile['relax']):
      return False
    
    output.log("PWscf Relaxation", verbose=0)
    relax_pw = template.load()

    relax_pw.set_prefix()
    relax_pw.set_calculation("vc-relax")
    relax_pw.save("relax.in", g.dirs['relax'])

    output.log("saving: " + os.path.join(g.dirs['relax'],"relax.in" ), verbose=0)

    # Run pwscf
    out = pwe.run([os.path.join(g.dirs['relax'], 'relax.in')])

    # Read output file 
    o = pwout_read.read(out[0][1])
    output.log("reading: " + out[0][1], verbose=0)
    output.log(str(o), verbose=0)

    a0_bohr = o['a0'] 
    a0 = units.convert('bohr', 'angs', a0_bohr)    
    output.log("Relaxed a0 (bohr): " + str(a0_bohr), verbose=0)
    output.log("Relaxed a0 (angs): " + str(a0), verbose=0)

    g.results['relaxed_a0'] = a0 / float(g.ifile['cxyz'][0])
    g.results['relaxed_uv'] = o['uv']

    # Adjust a0
    g.results['relaxed_nat'] = int(o['nat'])
    g.results['relaxed_a0'] = g.results['relaxed_a0'] / g.ifile['cxyz'][0]
    g.results['relaxed_volperatom'] = units.convert('BOHR3', 'ang3', float(o['vpa']))
    g.results['relaxed_energy_dft'] = units.convert('ry', 'ev', float(o['energy']))
    g.results['relaxed_energy'] = adjust_energy.run(o['energy'], o['labels'])
    g.results['relaxed_epa'] = g.results['relaxed_energy'] / g.results['relaxed_nat']

    # Output
    output.log("{:20s} {:8d} ".format("Relaxed nat", g.results['relaxed_nat']), verbose=0)
    output.log("{:20s} {:12.6f} ".format("Relaxed a0", g.results['relaxed_a0']), verbose=0)
    output.log("{:20s} {:12.6f} {:12.6f} {:12.6f} ".format("Relaxed UV", g.results['relaxed_uv'][0,0], g.results['relaxed_uv'][0,1], g.results['relaxed_uv'][0,2]), verbose=0)
    output.log("{:20s} {:12.6f} {:12.6f} {:12.6f} ".format("", g.results['relaxed_uv'][1,0], g.results['relaxed_uv'][1,1], g.results['relaxed_uv'][1,2]), verbose=0)
    output.log("{:20s} {:12.6f} {:12.6f} {:12.6f} ".format("", g.results['relaxed_uv'][2,0], g.results['relaxed_uv'][2,1], g.results['relaxed_uv'][2,2]), verbose=0)
    output.log("{:20s} {:12.6f} ".format("Vol/atom", g.results['relaxed_volperatom']), verbose=0)
    output.log("{:20s} {:12.6f} ".format("Relaxed e (dft)", g.results['relaxed_energy_dft']), verbose=0)
    output.log("{:20s} {:12.6f} ".format("Relaxed e", g.results['relaxed_energy']), verbose=0)
    output.log("{:20s} {:12.6f} ".format("Relaxed epa", g.results['relaxed_epa']), verbose=0)

    
    # Save relaxed parameters
    output.log("Saving relaxed data a0 and uv", verbose=0)
    fh = open(g.files['relaxed'], 'w')
    fh.write("{:8d}\n".format(g.results['relaxed_nat']))
    fh.write("{:20.10f}\n".format(g.results['relaxed_a0']))   # a0 angs
    fh.write("{:20.10f}\n".format(a0))                        # a0 scaled angs
    fh.write("{:20.10f}\n".format(a0_bohr))                   # a0 scaled bohr
    for i in range(3):
      for j in range(3):
        fh.write("{:20.10f}\n".format(g.results['relaxed_uv'][i,j]))
    fh.write("{:20.10f}\n".format(g.results['relaxed_volperatom']))
    fh.write("{:20.10f}\n".format(g.results['relaxed_energy_dft']))
    fh.write("{:20.10f}\n".format(g.results['relaxed_energy']))
    fh.write("{:20.10f}\n".format(g.results['relaxed_epa']))
    fh.close()


    # NOTE - in future, add relaxed coords here too



