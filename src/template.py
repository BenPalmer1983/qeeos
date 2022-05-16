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
from pwscf_inout import pwscf_input
from pwscf_inout import pwscf_output



class template:


  @staticmethod
  def run():

    output.log("Load template and modify.", verbose=0)

    t = pwscf_input()
    t.load(g.ifile['template'])
    t.set_dirs()
    t.set_ecutwfc(g.ifile['ecutwfc'])
    t.set_ecutrho(g.ifile['ecutrho'])
    t.set_k_points(g.ifile['kpoints_type'], g.ifile['kpoints'])
    t.set_degauss(g.ifile['degauss'])

    # Set structure
    if(g.ifile['structure'] is not None):
      s = {
        'type': g.ifile['structure'],
        'labels': g.ifile['labels'],
        'size_x': g.ifile['cxyz'][0],
        'size_y': g.ifile['cxyz'][1],
        'size_z': g.ifile['cxyz'][2],
        }    
      t.set_config(s)

    # Set a0
    a0 = g.ifile['cxyz'][0] * units.convert('angs', 'bohr', g.ifile['a0'])
    t.set_alat(a0)
    t.save("template.in", g.dirs['template'])
 

  @staticmethod
  def load():
    t = pwscf_input()
    t.load(os.path.join(g.dirs['template'], "template.in"))
    return t


  @staticmethod
  def make_relaxed():
    # Load data from results file
    if(not os.path.isfile(g.files['relaxed'])):
      g.end("No relaxed data - unable to continue.")

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

    # Output
    output.log("Making relaxed template using:", verbose=0)
    output.log("{:20s} {:12.6f} ".format("Relaxed a0", a0), verbose=0)
    output.log("{:20s} {:12.6f} ".format("Cx", g.ifile['cxyz'][0]), verbose=0)
    output.log("{:20s} {:12.6f} {:6s} ".format("Relaxed a0 (scaled)", a0_scaled, 'angs'), verbose=0)
    output.log("{:20s} {:12.6f} {:6s}".format("Relaxed a0 (scaled)", a0_scaled_bohr, 'bohr'), verbose=0)
    output.log("{:20s} {:12.6f} {:12.6f} {:12.6f} ".format("Relaxed UV", uv[0,0], uv[0,1], uv[0,2]), verbose=0)
    output.log("{:20s} {:12.6f} {:12.6f} {:12.6f} ".format("", uv[1,0], uv[1,1], uv[1,2]), verbose=0)
    output.log("{:20s} {:12.6f} {:12.6f} {:12.6f} ".format("", uv[2,0], uv[2,1], uv[2,2]), verbose=0)

    t = template.load()
    t.set_alat(a0_scaled_bohr)
    t.set_cp_arr(uv)
    t.save("template_relaxed.in", g.dirs['template'])



  @staticmethod
  def load_relaxed():
    t = pwscf_input()
    t.load(os.path.join(g.dirs['template'],"template_relaxed.in"))
    return t
