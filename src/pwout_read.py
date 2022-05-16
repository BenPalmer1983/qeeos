import numpy

class pwout_read:



  def read(path):
    d = []
    fh = open(path, "r")
    for line in fh:
      d.append(line)
    fh.close()
    
    # Version
    for dn in d:
      if("Program PWSCF v.6.4.1" in dn):
        v = "6.4.1"
        break
      if("Program PWSCF v.6.6" in dn):
        v = "6.6"
        break
     
    # Output type
    pwtype = 'SCF'
    a = 0
    b = 0
    for dn in d:
      if("BFGS Geometry Optimization" in dn):
        a = 1
      if("final scf calculation" in dn.lower()):
        b = 1
    if(a == 1 and b == 0):
      pwtype = "RELAX"
    elif(a == 1 and b == 1):
      pwtype = "VC-RELAX"

    out = {
          'pwtype': pwtype,
          'nat': None,
          'energy': None,
          'a0': None,
          'uv': None,
          'vol': None,
          'labels': [],
          'vpa': None,
          'epa': None,
          }


    if(pwtype == 'SCF'):
      out = pwout_read.read_scf(d, out)
    elif(pwtype == 'RELAX'):
      out = pwout_read.read_relax(d, out)
    elif(pwtype == 'VC-RELAX'):
      out = pwout_read.read_vcrelax(d, out)

    out['vpa'] = out['vol'] / float(out['nat'])
    out['epa'] = out['energy'] / float(out['nat'])
    return out


  def read_scf(d, out):
    out['uv'] = numpy.zeros((3,3,), dtype=numpy.float64)
    for dn in d:
      if("number of atoms/cell" in dn):
        out['nat'] = int(dn[32:50])
      elif("celldm(1)=" in dn):
        out['a0'] = float(dn[15:28])
      elif("a(1) = (" in dn):
        out['uv'][0,0] = float(dn[23:34])
        out['uv'][0,1] = float(dn[34:45])
        out['uv'][0,2] = float(dn[45:56])
      elif("a(2) = (" in dn):
        out['uv'][1,0] = float(dn[23:34])
        out['uv'][1,1] = float(dn[34:45])
        out['uv'][1,2] = float(dn[45:56])
      elif("a(3) = (" in dn):
        out['uv'][2,0] = float(dn[23:34])
        out['uv'][2,1] = float(dn[34:45])
        out['uv'][2,2] = float(dn[45:56])
      elif("!    total energy" in dn):
        out['energy'] = float(dn[32:50])
      elif("tau(" in dn):
        out['labels'].append(dn[10:24].strip())     
    m = out['uv'][0,0]
    out['a0'] = out['a0'] * m 
    out['uv'][:,:] = out['uv'][:,:] / m
    out['vol'] = numpy.dot(numpy.cross(out['a0'] * out['uv'][0,:], out['a0'] * out['uv'][1,:]), out['a0'] * out['uv'][2,:])
    return out



  def read_relax(d, out):
    out['uv'] = numpy.zeros((3,3,), dtype=numpy.float64)
    for dn in d:
      if("number of atoms/cell" in dn):
        out['nat'] = int(dn[32:50])
      elif("celldm(1)=" in dn):
        out['a0'] = float(dn[15:28])
      elif("a(1) = (" in dn):
        out['uv'][0,0] = float(dn[23:34])
        out['uv'][0,1] = float(dn[34:45])
        out['uv'][0,2] = float(dn[45:56])
      elif("a(2) = (" in dn):
        out['uv'][1,0] = float(dn[23:34])
        out['uv'][1,1] = float(dn[34:45])
        out['uv'][1,2] = float(dn[45:56])
      elif("a(3) = (" in dn):
        out['uv'][2,0] = float(dn[23:34])
        out['uv'][2,1] = float(dn[34:45])
        out['uv'][2,2] = float(dn[45:56])
      elif("Final energy" in dn):
        out['energy'] = float(dn[21:40])

    read = False
    for dn in d:
      if(read == False and "ATOMIC_POSITIONS" in dn):
        read = True
      elif(read == True and "End final coordinates" in dn):
        read = False
        break
      elif(read == True):
        out['labels'].append(dn[:9].strip())   

    m = out['uv'][0,0]
    out['a0'] = out['a0'] * m 
    out['uv'][:,:] = out['uv'][:,:] / m
    out['vol'] = numpy.dot(numpy.cross(out['a0'] * out['uv'][0,:], out['a0'] * out['uv'][1,:]), out['a0'] * out['uv'][2,:])
    return out



  def read_vcrelax(d, out):
    out['uv'] = numpy.zeros((3,3,), dtype=numpy.float64)
    in_final = False
    for dn in d:
      if("number of atoms/cell" in dn):
        out['nat'] = int(dn[32:50])
      elif("final scf calculation" in dn.lower()):
        in_final = True
      elif("celldm(1)=" in dn):
        out['a0'] = float(dn[15:28])
      elif("a(1) = (" in dn):
        out['uv'][0,0] = float(dn[23:34])
        out['uv'][0,1] = float(dn[34:45])
        out['uv'][0,2] = float(dn[45:56])
      elif("a(2) = (" in dn):
        out['uv'][1,0] = float(dn[23:34])
        out['uv'][1,1] = float(dn[34:45])
        out['uv'][1,2] = float(dn[45:56])
      elif("a(3) = (" in dn):
        out['uv'][2,0] = float(dn[23:34])
        out['uv'][2,1] = float(dn[34:45])
        out['uv'][2,2] = float(dn[45:56])
      elif("!    total energy" in dn):
        out['energy'] = float(dn[32:50])
      elif(in_final and "tau(" in dn):
        out['labels'].append(dn[10:24].strip()) 


    m = out['uv'][0,0]
    out['a0'] = out['a0'] * m 
    out['uv'][:,:] = out['uv'][:,:] / m
    out['vol'] = numpy.dot(numpy.cross(out['a0'] * out['uv'][0,:], out['a0'] * out['uv'][1,:]), out['a0'] * out['uv'][2,:])
    return out


    
    
    
    

if __name__ == "__main__":
  out = pwout_read.read("relax.out")
  print(out)

  """
  out = pwout_read.read("scf.out")
  print(out)
  out = pwout_read.read("relax.out")
  print(out)
  out = pwout_read.read("vcrelax.out")
  print(out)
  out = pwout_read.read("relaxbb.out")
  print(out)
  out = pwout_read.read("vcrelaxbb.out")
  print(out)
  """


