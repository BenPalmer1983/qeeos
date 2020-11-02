


class calc_eos:



  @staticmethod
  def run(): 
    if(not g.inp['eos']['run']):
      return 0
      
    # Load template  
    try:
      eos_template = pwscf_input()
      eos_template.load("relaxed.in", g.dirs['templates'])
      eos_template.set_dirs()
      eos_template.set_prefix() 
      eos_template.set_calculation("scf")        
      eos_template.save("eos_template.in", g.dirs['templates'])
    except:
      eos_template = pwscf_input()
      eos_template.load("modified_template.in", g.dirs['templates'])
      eos_template.set_dirs()
      eos_template.set_prefix() 
      eos_template.set_calculation("scf")        
      eos_template.save("eos_template.in", g.dirs['templates'])
    
    r_cp = eos_template.get_cp_array()
    
    # STRAIN
    s_val = g.inp['eos']['strain']
    s_points = g.inp['eos']['points']    
    s_arr = numpy.linspace(-s_val, s_val, s_points)

    #
    runfile = []
    f_out_list = []
    f = pwscf_input()
    f.load("eos_template.in", g.dirs['templates'])
    
    g.log_fh.write("\n")
    g.log_fh.write("############################\n")
    g.log_fh.write("EOS Calc\n")
    g.log_fh.write("############################\n")
    g.log_fh.write("\n")
    for n in range(s_points):
      cp = (1.0 + s_arr[n]) * r_cp
      f.set_cp(cp)
      f.set_prefix() 
      nstr = str(n+1)
      while(len(nstr)<3):
        nstr = "0" + nstr
             
      f.save("eos_" + nstr + ".in", g.dirs['eos'])      
      f_out_list.append(g.dirs['eos'] + '/' + "eos_" + nstr + ".out")
      
      run = True
      if(g.inp['eos']['use_existing'] and os.path.exists(f_out_list[-1])):
        fpo = pwscf_output(f_out_list[-1])
        if(fpo.get_job_done()):
          run = False
          printout = "Existing Used - job done"
        elif(fpo.get_job_almost_done()):
          run = False
          printout = "Existing Used - job almost done"
        if(g.inp['eos']['always_use_existing']):
          run = False            
          printout = "Existing Used - forced"
      if(run):
        runfile = [g.dirs['eos'] + "/eos_" + nstr + ".in"]     
        printout = "Skipped"   
        if(g.inp['settings']['pwscf_run']):
          files_out = pwscf_exec.execute(runfile)
          if(pwscf_exec.data['cache_used']):
            printout = "Cache Used"           
          else:
            printout = "PWscf Run"
          
      print(printout + str(" eos_" + nstr + ".in"))    
          
        
        
        
        
      g.log_fh.write("Strain (" + str(n) + "): " + str(s_arr[n]) + "\n")  
    
    # Prepare array to store data
    g.eos = {
             'complete': False,  
             'data': numpy.zeros((s_points, 3,),),
            }
    for n in range(s_points):
      g.eos['data'][n, 0] = float(s_arr[n])

      
    #try:
    if(True):
      print("EOS")
      fh = open(g.dirs['results'] + '/eos.csv', 'w')
      for n in range(len(f_out_list)):
        if(os.path.exists(f_out_list[n])):
          fpo = pwscf_output(f_out_list[n])
          if((g.inp['job_done']['setting'] == 'done' and fpo.get_job_done()) or (g.inp['job_done']['setting'] == 'almost' and fpo.get_job_almost_done())):
            g.eos['data'][n, 1] = fpo.get_volume_per_atom()
            g.eos['data'][n, 2] = fpo.get_energy_per_atom()
            fh.write(str(g.eos['data'][n, 0]) + ',' +  str(g.eos['data'][n, 1]) + ',' +  str(g.eos['data'][n, 2]) + '\n')
            print(str(g.eos['data'][n, 0]) + ',' +  str(g.eos['data'][n, 1]) + ',' +  str(g.eos['data'][n, 2]))
      fh.close()
    #except:
    #  pass

      
    # SAVE DATA
    g.eos['complete'] = True  
    save_load.save(g.eos, g.dirs['data'] + '/' + 'eos.dat')  
    
    
    
