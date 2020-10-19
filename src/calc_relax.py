


class calc_relax:



  @staticmethod
  def run():  
   
    # CREATE 
    
    relaxed_template = pwscf_input()
    relaxed_template.load("modified_template.in", g.dirs['templates'])
    relaxed_template.set_dirs()
    relaxed_template.set_prefix() 
    relaxed_template.set_calculation("scf")
    relaxed_template.save("relaxed.in", g.dirs['templates'])    
  

    if(not g.inp['relax']['run']):
      return 0
      
      
    relax_file = pwscf_input()
    relax_file.load("modified_template.in", g.dirs['templates'])
    relax_file.set_dirs()
    relax_file.set_prefix() 
    relax_file.set_calculation("vc-relax")
    relax_file.save("relax.in", g.dirs['relax'])   

    # RUN PWSCF
    runfile = []
    runfile.append(g.dirs['relax'] + '/relax.in')
    
    if(g.inp['settings']['pwscf_run']):
      files_out = pwscf_exec.execute(runfile)
    else:
      files_out = []

    if(files_out[0]['status'] == 'complete'):     
      relaxed_file = pwscf_output(files_out[0]['file'])   
      g.relaxed['complete'] = True 
      
      
      o = relaxed_file.get_relaxed_data_full()
      
      g.relaxed['nat'] = o['nat']
      g.relaxed['alat'] = o['alat_adj']
      g.relaxed['cp'] = o['cp_adj']
      g.relaxed['mass_per_crystal'] = o['mass_per_crystal']
      g.relaxed['volume'] = o['volume']
      g.relaxed['density'] = o['density']
      g.relaxed['total_energy'] = o['total_energy']
      g.relaxed['energy_per_atom'] = o['energy_per_atom']
      g.relaxed['total_force'] = o['total_force']
      g.relaxed['force_per_atom'] = o['force_per_atom']
      
      
      relaxed_file.get_data("r.txt")
      save_load.save(g.relaxed, g.dirs['data'] + '/' + 'relax.dat')

      relaxed_template.load_from_relaxed(files_out[0]['file'])
      relaxed_template.save("relaxed.in", g.dirs['templates'])    
  
    
    
    else:
      save_load.save({'ERROR': True,}, g.dirs['data'] + '/' + 'relax.dat')

      


    #exit()





#d = save_load.load(g.dirs['data'] + '/' + 'relax.dat')

