#################################
# Load settings from environment
#################################

import os

class pwscf_settings:
 
  @staticmethod
  def load():
    # Default Settings
        
    s = {
    "omp_num_threads":  1,
    "proc_count":  1,
    "pwscf_scratch": '',
    "pwscf_pp": '',
    "pwscf_cache": '',
    "pwscf_bin": '',
    "pwscf_script": '',
    }

    for k in s.keys():
      try:
        s[k.lower()] = os.environ[k.upper()]
      except:
        pass


    return s
