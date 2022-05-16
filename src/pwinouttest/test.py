from pwscf_inout import pwscf_output

fname = ["scf.out", "relax.out", "vcrelax.out"]
for fn in fname:
  f = pwscf_output(fn)
  ftype = f.get_type()
  energy = f.get_final_epa()
  nat = f.get_nat()
  labels = f.get_labels()
  vol = f.get_final_vpa()
  print(ftype)
  print(energy)
  print(nat)
  print(labels)
  print(vol)
  print()
