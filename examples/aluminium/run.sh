#!/bin/bash

# Set the number of threads to 1
export OMP_NUM_THREADS=1
export PROC_COUNT=1
export PWSCF_SCRATCH=/opt/scratch
export PWSCF_PP=/opt/pp
export PWSCF_CACHE=/opt/pwscf_cache
export PWSCF_BIN=/opt/qe/bin/pw.x
#export PWSCF_SCRIPT=/opt/qe/bin/pw.sh


thisdir=$(pwd)
echo $thisdir
cd ../../
qeeos=$(pwd)
echo $qeeos
./package.sh
cd $thisdir
cp ../../qeeos.py qeeos.py

python3 qeeos.py input.in all
