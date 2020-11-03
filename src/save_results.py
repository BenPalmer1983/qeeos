
class save_results:


  @staticmethod
  def run(): 
    file = g.dirs['results'] + "/" + "results.txt" 
    fh = open(file, 'w')
    fh.write("################################################################\n")
    fh.write("#                        RESULTS                               #\n")
    fh.write("################################################################\n")
    fh.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
    fh.write("\n")
    fh.write("\n")
    fh.close()
    
    save_results.settings(file)
    if(g.relaxed['complete']):
      save_results.relaxed(file)
    if(g.eos['complete']):
      save_results.eos(file)
    if(g.ec['complete']):
      save_results.ec(file)
    
    
  def settings(file): 
    ############################################
    # SAVE TO RESULTS
    ############################################
      
    fh = open(file, 'a')
    fh.write("INPUT SETTINGS\n")
    fh.write("################################\n")
    fh.write("\n")
    fh.write("Structure:                    " + str(g.inp['config']['structure']) + "\n")
    fh.write("Size:                         " + str(g.inp['config']['size']) + "\n")
    fh.write("A0:                           " + str(g.inp['config']['alat']) + "\n")
    fh.write("A0 Units:                     " + str(g.inp['config']['alat_units']) + "\n")
    fh.write("A0 (Bohr):                    " + str(g.data['alat_in_bohr']) + "\n")
    fh.write("A0 (Angs):                    " + str(float(g.data['alat_in_bohr']) * 0.529) + "\n")
    fh.write("\n")
    
    fh.write("Ecutwfc:                      " + str(g.inp['settings']['ecutwfc']) +"\n")
    fh.write("Ecutrho:                      " + str(g.inp['settings']['ecutrho']) +"\n")
    fh.write("Degauss:                      " + str(g.inp['settings']['degauss']) +"\n")
    fh.write("Kpoints:                      " + str(g.inp['settings']['kpoints']) +"\n")
    fh.write("Kpoints Type:                 " + str(g.inp['settings']['kpointstype']) +"\n")
    fh.write("EOS Points:                   " + str(g.inp['eos']['points']) +"\n")
    fh.write("EOS Strain:                   " + str(g.inp['eos']['strain']) +"\n")
    fh.write("EC Points:                    " + str(g.inp['ec']['points']) +"\n")
    fh.write("EC Strain:                    " + str(g.inp['ec']['strain']) +"\n")
    fh.write("\n")
    fh.write("\n")
    fh.close()
    
  def relaxed(file): 
  
    fh = open(file, 'a')
    fh.write("RELAXED" + "\n")
    fh.write("################################\n")
    fh.write("\n") 
    fh.write("a0 (Bohr):                    " + str(g.relaxed['alat']) +"\n")
    fh.write("CP:                           " + str(g.relaxed['cp'][0,0]) + "      " 
                                              + str(g.relaxed['cp'][0,1]) + "      " 
                                              + str(g.relaxed['cp'][0,2]) + "\n")
    fh.write("                              " + str(g.relaxed['cp'][1,0]) + "      " 
                                              + str(g.relaxed['cp'][1,1]) + "      " 
                                              + str(g.relaxed['cp'][1,2]) + "\n")
    fh.write("                              " + str(g.relaxed['cp'][2,0]) + "      " 
                                              + str(g.relaxed['cp'][2,1]) + "      " 
                                              + str(g.relaxed['cp'][2,2]) + "\n")
    fh.write("Volume (Bohr^3/unit cell):    " + str(g.relaxed['volume']) + "\n")
    fh.write("Density KG/m^3:               " + str(g.relaxed['density']) +"\n")
    fh.write("AMU per crystal unit:         " + str(g.relaxed['mass_per_crystal']) + "\n")   
    fh.write("Atoms per crystal unit:       " + str(g.relaxed['nat']) + "\n")    
    fh.write("Total Energy/Ry:              " + str(g.relaxed['total_energy']) + "\n")    
    fh.write("Energy per Atom/Ry:           " + str(g.relaxed['energy_per_atom']) + "\n")    
    fh.write("Total Force Ry/Bohr:          " + str(g.relaxed['total_force']) + "\n")    
    fh.write("Force per atom Ry/Bohr:       " + str(g.relaxed['force_per_atom']) + "\n")    
    fh.write("\n")
    fh.write("\n")
    fh.write("a0 primitive (Bohr):          " + str((float(g.relaxed['alat']) / float(g.inp['config']['size']))) +"\n")
    fh.write("a0 primitive (Ang):          " + str((float(g.relaxed['alat']) / float(g.inp['config']['size'])) * 0.529) +"\n")
    fh.write("\n")
    fh.write("\n")
    fh.close()
    
    
    


  def eos(file): 
  
    fh = open(file, 'a')
    fh.write("EOS" + "\n")
    fh.write("################################\n")
    fh.write("\n") 
    fh.write("V0 (Bohr^3 / atom):           " + str(g.eos_results['V0']) +"\n")
    fh.write("E0 (Ry / atom):               " + str(g.eos_results['E0']) +"\n")
    fh.write("B0 (RY/BOHR3):                " + str(g.eos_results['B0']) +"\n")
    fh.write("B0 (GPA):                     " + str(g.eos_results['B0_gpa']) +"\n")
    fh.write("B0P:                          " + str(g.eos_results['B0P']) +"\n")    
    fh.write("\n")
    fh.write("\n")
    fh.close()
    
  
  def ec(file): 
    fh = open(file, 'a')
    fh.write("EC" + "\n")
    fh.write("################################\n")
    fh.write("\n")
    for i in range(6):
      if(i == 0):        
        fh.write("Stiffness (RY/BOHR3):         " + 
        std.float_padded(g.ec_results['stiffness'][i,0], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,1], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,2], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,3], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,4], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,5], 10) + "\n" )
      else:
        fh.write("                              " + 
        std.float_padded(g.ec_results['stiffness'][i,0], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,1], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,2], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,3], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,4], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,5], 10) + "\n" )    
    fh.write("\n")
    for i in range(6):
      if(i == 0):        
        fh.write("Stiffness (GPA):              " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,0], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,1], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,2], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,3], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,4], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,5], 10) + "\n" )
      else:
        fh.write("                              " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,0], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,1], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,2], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,3], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,4], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,5], 10) + "\n" )    
    fh.write("\n")
    for i in range(6):
      if(i == 0):        
        fh.write("Compliance (1/GPA):           " + 
        std.float_padded(g.ec_results['compliance'][i,0], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,1], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,2], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,3], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,4], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,5], 10) + "\n" )
      else:
        fh.write("                              " + 
        std.float_padded(g.ec_results['compliance'][i,0], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,1], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,2], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,3], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,4], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,5], 10) + "\n" )    
    fh.write("\n")
    

      
    c11 = g.ec_results['stiffness_gpa'][0,0]
    c22 = g.ec_results['stiffness_gpa'][1,1]
    c33 = g.ec_results['stiffness_gpa'][2,2]
    c44 = g.ec_results['stiffness_gpa'][3,3]
    c55 = g.ec_results['stiffness_gpa'][4,4]
    c66 = g.ec_results['stiffness_gpa'][5,5]
    c12 = g.ec_results['stiffness_gpa'][0,1]
    c13 = g.ec_results['stiffness_gpa'][0,2]
    c23 = g.ec_results['stiffness_gpa'][1,2]
    
    sa = c11
    sb = (c11*c22)-(c12*c12)
    sc = c11*c22*c33+2*c12*c13*c23-c11*c23*c23-c33*c12*c12
    sd = c44
    se = c55
    sf = c66
    
    fh.write("Stability:\n")
    
    fh.write("C11:                                                " + str(sa) + " ")
    if(sa < 0):
      fh.write("(Unstable)")
    else:
      fh.write("(Stable)")
    fh.write("\n")
      
    fh.write("C11C22 - C12C12:                                    " + str(sb) + " ")
    if(sb < 0):
      fh.write("(Unstable)")
    else:
      fh.write("(Stable)")
    fh.write("\n")
      
    fh.write("C11*C22*C33+2*C12*C13*C23-C11*C23*C23-C33*C12*C12:  " + str(sc) + " ")
    if(sc < 0):
      fh.write("(Unstable)")
    else:
      fh.write("(Stable)")
    fh.write("\n")
      
    fh.write("C44:                                                " + str(sd) + " ")
    if(sd < 0):
      fh.write("(Unstable)")
    else:
      fh.write("(Stable)")
    fh.write("\n")
      
    fh.write("C55:                                                " + str(se) + " ")
    if(se < 0):
      fh.write("(Unstable)")
    else:
      fh.write("(Stable)")
    fh.write("\n")
      
    fh.write("C66:                                                " + str(sf) + " ")
    if(sf < 0):
      fh.write("(Unstable)")
    else:
      fh.write("(Stable)")
    fh.write("\n")
    fh.write("\n")
    
            
      
    
    fh.write("Bulk Modulus B (GPA):         " + str(g.material_properties['B']) + "\n")
    fh.write("BR (GPA):                     " + str(g.material_properties['BR']) + "\n")
    fh.write("BV (GPA):                     " + str(g.material_properties['BV']) + "\n")
    fh.write("\n")
    
    fh.write("Shear Modulus G (GPA):        " + str(g.material_properties['G']) + "\n")
    fh.write("GR:                           " + str(g.material_properties['GR']) + "\n")
    fh.write("GV:                           " + str(g.material_properties['GV']) + "\n")
    fh.write("\n")
    
    fh.write("Young's Modulus E (GPA):      " + str(g.material_properties['E']) + "\n")
    fh.write("\n")
    fh.write("Poisson's Ratio v:            " + str(g.material_properties['v']) + "\n")
    fh.write("\n")
    fh.write("\n")    
    
    fh.write("L Elastic Wave V:             " + str(g.material_properties['vl']) + "\n")
    fh.write("T Elastic Wave V:             " + str(g.material_properties['vt']) + "\n")
    fh.write("M Elastic Wave V:             " + str(g.material_properties['vm']) + "\n")
    fh.write("\n")
    fh.write("Debye Temperature:            " + str(g.material_properties['debye']) + "\n")
    fh.write("\n")
    fh.write("Melting Point:                " + str(round(g.material_properties['melting_point'],0)) + "K \n")
    fh.write("\n")
    fh.write("\n")
    fh.write("\n")
    fh.write("\n")   
    fh.write("\n")
    fh.write("\n")
    fh.write("\n")  
    fh.write("\n")
    fh.write("References \n")
    fh.write("=======================================\n")
    fh.write("\n")
    fh.write("First Principles Calculations of Elastic Properties of Metals\n")
    fh.write("M. J. Mehl, B. M. Klein, D. A. Papaconstantopoulos\n")
    fh.write("1994\n")  
    fh.write("\n")
    fh.write("Ab Initio Study of the Elastic and Mechanical Properties of B19 TiAl\n")  
    fh.write("Y. Wen, L. Wang, H. Liu and L. Song\n")
    fh.write("Crystals\n")
    fh.write("2017\n")
    fh.write("\n")
    fh.write("Density functional theory for calculation of elastic properties of orthorhombic crystals - applications to TiSi2\n")  
    fh.write("P. Ravindran, Lars Fast, P. A. Korzhavyi, B. Johansson\n")
    fh.write("Journal of Applied Physics\n")
    fh.write("1998\n")
    fh.write("\n") 
    fh.close()
    
    