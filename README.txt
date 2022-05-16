QEEOS
=================================

Quantum Espresso - Equation of State (and Elastic Constants)

Python code.

This code uses pwscf from the Quantum Espresso suite to calculate crystal energies using DFT.

For a full run, this is what the code does:

1.   Reads in the user's input
2.   Creates a template file for PWscf based on the user's input and supplied template file
3.   Creates a vc-relax input file and runs this to find the relaxed a0 and cell parameters
     Also calculates the density of the material based on the DFT results
4.   Creates and executes a series of SFC or RELAX input files over a range of strains 
     in order to calculate the equation of state
5.   Creates and executes a series of SFC or RELAX input files over a range of strains from MSKP 
     in order to calculate the cubic elastic constants
6.   Creates and executes a series of SFC or RELAX input files over a range of strains from RFKJ 
     in order to calculate the orthorhombic elastic constants
7.   Processes the results
8.   Creates plots
9.   Using the elastic constants, other material properties are calculated or estimated


Melh, Singh, Klein, Papaconstatopolous
Ravindran, Fast, Korzhavyi, Johansson
