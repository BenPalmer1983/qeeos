#!/bin/bash


# Set the number of threads to 1
export OMP_NUM_THREADS=1
export PROC_COUNT=1
export PWSCF_SCRATCH=/opt/scratch
export PWSCF_PP=/opt/pp
export PWSCF_CACHE=/opt/pwscf_cache
export PWSCF_BIN=/rds/homes/b/bxp912/apps/qe-6.3/bin/pw.x
export PWSCF_SCRIPT=/rds/homes/b/bxp912/apps/qe-6.3/bin/pw.sh

python3 qeeos.py input.in
