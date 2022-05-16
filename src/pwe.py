################################################################
#    Processing PWscf input file
#
#
#
#
################################################################

import os
import datetime
import re
import sys
import hashlib 
import time
from shutil import copyfile

############################
#  pwscf_input
############################

class pwe:

  fh = None
  omp_num_threads = 1
  proc_count = 1
  npool = 1
  pwscf_scratch = ''
  pwscf_pp = ''
  pwscf_cache = ''
  pwscf_bin = ''
  pwscf_script = ''
  

  @staticmethod
  def clean_log():
    pwe.fh = open('pwscflog.txt', 'w')

  @staticmethod
  def run(files, use_cache=True, log=True):
    pwe.fh = open('pwscflog.txt', 'w+')

    if('OMP_NUM_THREADS' in os.environ.keys()): pwe.omp_num_threads = os.environ['OMP_NUM_THREADS']
    if('PROC_COUNT' in os.environ.keys()): pwe.proc_count = os.environ['PROC_COUNT']
    if('NPOOL' in os.environ.keys()): pwe.npool = os.environ['NPOOL']
    if('PWSCF_SCRATCH' in os.environ.keys()): pwe.pwscf_scratch = os.environ['PWSCF_SCRATCH']
    if('PWSCF_PP' in os.environ.keys()): pwe.pwscf_pp = os.environ['PWSCF_PP']
    if('PWSCF_CACHE' in os.environ.keys()): pwe.pwscf_cache = os.environ['PWSCF_CACHE']
    if('PWSCF_BIN' in os.environ.keys()): pwe.pwscf_bin = os.environ['PWSCF_BIN']
    if('PWSCF_SCRIPT' in os.environ.keys()): pwe.pwscf_script = os.environ['PWSCF_SCRIPT']

    out = []
    for file in files:
      hash = pwe.hash(file)
      pwe.fh.write(file + "\n")
      pwe.fh.write(hash + "\n")
      if(use_cache):
        out_file, job_done = pwe.load_cache(file, hash)
      else:
        out_file, job_done = pwe.exec(file, hash)
      out.append([file, out_file, job_done])

    pwe.fh.close()
    return out

  @staticmethod
  def load_cache(in_file, hash):
    out_file = in_file[:-2] + "out"
    cache_in = os.path.join(pwe.pwscf_cache, hash + ".in")
    cache_out = os.path.join(pwe.pwscf_cache, hash + ".out")

    if(os.path.isfile(cache_in) and os.path.isfile(cache_out)):    
      copyfile(cache_out, out_file)
      job_done = True
      pwe.fh.write("CACHE USED\n")
      pwe.fh.write(cache_out + "\n")
    else:
      out_file, job_done = pwe.exec(in_file, hash)
    return out_file, job_done


  @staticmethod
  def exec(in_file, hash):
    out_file = in_file[:-2] + "out"
    cmd = 'mpirun -n '
    cmd = cmd + str(pwe.proc_count) + ' '
    cmd = cmd + str(pwe.pwscf_bin) + ' ' 
    if(int(pwe.npool) > 1):
      cmd = cmd + '-npool ' + str(pwe.npool) + ' ' 
    cmd = cmd + '-in ' + str(in_file) + ' ' 
    cmd = cmd + '> ' + str(out_file) + '' 
    
    # Run pwscf
    
    pwe.fh.write(cmd + "\n")
    pwe.fh.flush()
    a = time.time()
    os.system(cmd)
    pwe.fh.write("time to complete: " + str(time.time() - a) + "\n")
    pwe.fh.flush()

    t = []
    fh = open(out_file, 'r')
    for line in fh:
      t.append(line.strip())
    fh.close()
    
    job_done = False
    for n in range(len(t)-10, len(t)):
      if("JOB DONE." in t[n]):
        job_done = True
    if(job_done):
      pwe.fh.write("**** JOB DONE ****\n")
    else:
      pwe.fh.write("**** JOB FAILED ****\n")

    if(job_done and os.path.isdir(pwe.pwscf_cache)):
      copyfile(in_file, os.path.join(pwe.pwscf_cache, hash + ".in"))
      copyfile(out_file, os.path.join(pwe.pwscf_cache, hash + ".out"))
    return out_file, job_done

  @staticmethod
  def hash(file):
    ctext = ''
    fh = open(file, 'r')
    for line in fh:
      line = line.split("!")
      line = line[0].strip().replace(" ", "")
      if(not('outdir' in line or 'prefix' in line or 'wfcdir' in line or 'pseudo_dir' in line)): 
        ctext = ctext + line.upper()
    fh.close() 
    
    ctext = ctext.encode('utf-8')
    chash = hashlib.md5()
    chash.update(ctext)
    
    hex = chash.hexdigest()

    return pwe.base64(hex)


  @staticmethod
  def base64(inp):
    out = ''
    dec = "0123456789"
    hex = {'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}
    base = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"
    while(len(inp) % 3 == 0):
      inp = inp + "0"
    for n in range(len(inp) // 3):
      chunk = inp[n:n+3]
      chunkv = 0
      for k in range(3):
        if(chunk[k] in dec):
          chunkv = chunkv + 16**k * int(chunk[k])
        else:
          chunkv = chunkv + 16**k * hex[chunk[k]]
      A = chunkv // 64
      B = chunkv % 64
      out = out + base[A] + base[B]

    return out