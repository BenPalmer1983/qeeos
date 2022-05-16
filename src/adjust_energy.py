#!/bin/python3

import os
import sys
import numpy
import time
import shutil

from g import g
from ds import ds

from units import units

class adjust_energy:

  # Always takes in total energy, all atoms (usually in Ry)
  # Always outputs in eV
  @staticmethod
  def run(energy, labels, unit_in='ry', epa=False):
 
    energy_out = units.convert(unit_in, 'ev', energy)
    for l in labels:
      l = l.strip().upper()
      if(l in g.adjust.keys()):
        energy_out = energy_out + g.adjust[l]
    if(epa):
      energy_out = energy_out / len(labels)
    return energy_out

