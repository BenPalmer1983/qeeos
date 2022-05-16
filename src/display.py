#!/bin/python3

import numpy
import time
import os

from g import g
from ds import ds

class display:

  w = 150

  @staticmethod
  def hr():
    for i in range(display.w):
      print("-", end="")
    print()

  @staticmethod
  def hrr():
    for i in range(display.w):
      print("#", end="")
    print()

  @staticmethod
  def clear():
    os.system('cls' if os.name == 'nt' else 'clear') 
    