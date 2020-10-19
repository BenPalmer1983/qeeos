


class calc_ec:



  @staticmethod
  def run(): 
    if(not g.inp['ec']['run']):
      return 0
      
    # Load template  
    try:
      ec_template = pwscf_input()
      ec_template.load("relaxed.in", g.dirs['templates'])
      ec_template.set_dirs()
      ec_template.set_prefix() 
      ec_template.set_calculation("scf")        
      ec_template.save("ec_template.in", g.dirs['templates'])
    except:
      ec_template = pwscf_input()
      ec_template.load("modified_template.in", g.dirs['templates'])
      ec_template.set_dirs()
      ec_template.set_prefix() 
      ec_template.set_calculation("scf")        
      ec_template.save("ec_template.in", g.dirs['templates'])
        
    #R_CP
    r_cp = ec_template.get_cp_array()
    
    # STRAIN
    s_val = g.inp['ec']['strain']
    s_points = g.inp['ec']['points']    
    s_arr = numpy.linspace(0.0, s_val, s_points)
    
    
    
    g.log_fh.write("\n")
    g.log_fh.write("############################\n")
    g.log_fh.write("EC Calc\n")
    g.log_fh.write("############################\n")
    g.log_fh.write("\n")
    
       
    # MAKE FILES
    f = pwscf_input()
    f.load("ec_template.in", g.dirs['templates'])
    runfile = []
    f_out_list = []
    for dn in range(9):
      g.log_fh.write("#############\n")
      g.log_fh.write(str(dn) + "\n")
      g.log_fh.write("#############\n")
      for j in range(s_points):
        sigma = s_arr[j]
        d = calc_ec.distortion(sigma, dn + 1)
        cp = numpy.matmul(d, r_cp)
        f.set_cp(cp)
        f.set_prefix() 
        
        nstr = str(j+1)
        while(len(nstr)<3):
          nstr = "0" + nstr
        
        file_name_in = "ec_" + str(dn+1) + "_" + nstr + ".in"
        file_name_out = "ec_" + str(dn+1) + "_" + nstr + ".out"
        f.save(file_name_in, g.dirs['ec'])  
        f_out_list.append(g.dirs['ec'] + '/' + file_name_out)
                
        run = True
        if(g.inp['ec']['use_existing'] and os.path.exists(f_out_list[-1])):
          fpo = pwscf_output(f_out_list[-1])
          if(fpo.get_job_done()):
            run = False
            printout = "Existing Used - job done"
          elif(fpo.get_job_almost_done()):
            run = False
            printout = "Existing Used - job almost done"
          if(g.inp['ec']['always_use_existing']):
            run = False            
            printout = "Existing Used - forced"
        if(run):
          runfile = [g.dirs['ec'] + "/" + file_name_in]     
          printout = "Skipped"   
          if(g.inp['settings']['pwscf_run']):
            files_out = pwscf_exec.execute(runfile)
            if(pwscf_exec.data['cache_used']):
              printout = "Cache Used"           
            else:
              printout = "PWscf Run"
          
        print(printout + str(file_name_in))       
        
       
        
        g.log_fh.write("Sigma: " + str(sigma) + "\n")
      
      g.log_fh.write("\n")  
        
    
    # Prepare arrays to store data
    g.ec = {'complete': False, }
              
    for dn in range(9):
      key = str(dn)
      g.ec[key] = numpy.zeros((s_points, 4,),)
      for n in range(s_points):
        g.ec[key][n, 0] = float(s_arr[n])
   
    try:
      fh = open(g.dirs['results'] + '/ec.csv', 'w')
      s = 0
      for file in f_out_list:
        fpo = pwscf_output(file)
        if(fpo.get_job_done() and fpo.get_job_converged()):        
          dn = s // s_points
          g.log_fh.write("#############\n")
          g.log_fh.write(str(dn) + "\n")
          g.log_fh.write("#############\n")
          key = str(dn)
          n = s % s_points
          g.ec[key][n, 1] = fpo.get_volume_per_atom()
          g.ec[key][n, 2] = fpo.get_energy_per_atom()
          g.ec[key][n, 3] = fpo.get_total_energy()
          fh.write(str(s) + ',' + str(dn) + ',' + str(n) + ',' + str(g.ec[key][n, 0]) + ',' + str(g.ec[key][n, 1]) + ',' +  str(g.ec[key][n, 2]) + ',' +  str(g.ec[key][n, 3]) + '\n')
          g.log_fh.write(str(s) + ',' + str(dn) + ',' + str(n) + ',' + str(g.ec[key][n, 0]) + ',' + str(g.ec[key][n, 1]) + ',' +  str(g.ec[key][n, 2]) + ',' +  str(g.ec[key][n, 3]) + '\n')
          s = s + 1  
      fh.close()
      g.log_fh.write("\n") 
    except:
      pass
      
    # SAVE DATA
    g.ec['complete'] = True
    save_load.save(g.ec, g.dirs['data'] + '/' + 'ec.dat') 

  
  @staticmethod
  def distortion(sigma, dn):
    d = numpy.zeros((3,3),)
    if(dn == 1):
      d[0,0] = 1.0 + sigma
      d[1,1] = 1.0
      d[2,2] = 1.0
    elif(dn == 2):
      d[0,0] = 1.0
      d[1,1] = 1.0 + sigma
      d[2,2] = 1.0
    elif(dn == 3):
      d[0,0] = 1.0
      d[1,1] = 1.0
      d[2,2] = 1.0 + sigma
    elif(dn == 4):
      a = ((1 - sigma**2)**(1/3))
      d[0,0] = 1.0 / a
      d[1,1] = 1.0 / a
      d[2,2] = 1.0 / a
      d[1,2] = sigma / a
      d[2,1] = sigma / a
    elif(dn == 5):
      a = ((1 - sigma**2)**(1/3))
      d[0,0] = 1.0 / a
      d[1,1] = 1.0 / a
      d[2,2] = 1.0 / a
      d[0,2] = sigma / a
      d[2,0] = sigma / a
    elif(dn == 6):
      a = ((1 - sigma**2)**(1/3))
      d[0,0] = 1.0 / a
      d[1,1] = 1.0 / a
      d[2,2] = 1.0 / a
      d[0,1] = sigma / a
      d[1,0] = sigma / a
    elif(dn == 7):
      a = ((1 - sigma**2)**(1/3))
      d[0,0] = (1.0 + sigma) / a
      d[1,1] = (1.0 - sigma) / a
      d[2,2] = (1.0) / a
    elif(dn == 8):
      a = ((1 - sigma**2)**(1/3))
      d[0,0] = (1.0 + sigma) / a
      d[1,1] = (1.0) / a
      d[2,2] = (1.0 - sigma) / a
    elif(dn == 9):
      a = ((1 - sigma**2)**(1/3))
      d[0,0] = (1.0) / a
      d[1,1] = (1.0 + sigma) / a
      d[2,2] = (1.0 - sigma) / a
    return d
    
    
    
    
    
    
    
    