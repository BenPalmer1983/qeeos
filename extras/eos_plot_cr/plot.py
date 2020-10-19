import matplotlib.pyplot as plt
import numpy
import os



def read_csv(filename):
  data = []
  if(os.path.isfile(filename)):
    # Read from file into memory
    fh = open(filename, 'r')
    file_data = ""
    for line in fh:
      file_data = file_data + line
    fh.close()
    # Read Data
    lines = file_data.split("\n")
    for line in lines:
      line = line.strip()
      row = []
      if(line != ""):
        r = line.split(",")
        for ri in r:
          row.append(float(ri))
        data.append(row)  
  data = numpy.asarray(data)
  return data


def plot():
  plt.clf()
    
  plt.rc('font', family='serif')
  plt.rc('xtick', labelsize='x-small')
  plt.rc('ytick', labelsize='x-small')

  fig, axs = plt.subplots(1, 1, figsize=(12,9))
  fig.tight_layout(pad=5.0)
  fig.suptitle('Equation of State')    
    
  this_dir = os.getcwd()
  dirs = os.listdir(this_dir) 

  markers = ['.','s','v','x','+','8']
  linestyle = ['solid','dotted','dashdot','dashed']
  colours = ['#006699','#009999','#00CC99','#00CC66','#00CC00']

  n = 0
  for d in dirs:
    if(os.path.isdir(d)):
      data = read_csv(d + '/eos_data.csv')
      fit = read_csv(d + '/eos_fit_data.csv')
      fh = open(d + '/plot.txt')
      for row in fh:
        plot_name = row
        break
      
      plt.plot(data[:,0], data[:,1], color=colours[n],  marker=markers[n], ls='none', label=plot_name)
      plt.plot(fit[:,0], fit[:,1], color=colours[n], ls=linestyle[n])
      n = n + 1
  

  axs.set_xlabel('Volume (Bohr^3/atom)')
  axs.set_ylabel('Energy (Ry/atom)')
  axs.legend()
  plt.savefig('eos.eps')
  plt.savefig('eos.png')



  

plot()


