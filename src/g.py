from ds import ds
import time

class g:
  
  # main
  dirs = ds.dirs()
  start = None
  end = None
  fh = None        # g.fh is the main log file
  verbose = {'print': 0, 'file': 1}
  units = ds.units()
  adjust = {}

  # Input file
  ifile = ds.ifile()

  # Results
  results = ds.results()
  files = ds.files()       # data files 
  output = ''

  # Strains
  mskp = ds.mskp()
  rfkj = ds.rfkj()
  


  @staticmethod
  def end(msg=None):
    g.end = time.time()
  
    if(msg is not None):
      line = str(msg)
      g.fh.write(line + "\n")
      print(line)

    line = "Time elapsed: {:12.4f}s".format(g.end - g.start)
    g.fh.write(line + "\n")
    print(line)

    line = "End."
    g.fh.write(line + "\n")
    print(line)

    g.fh.close()
    exit()

