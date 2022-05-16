#!/bin/bash
export OMP_NUM_THREADS=1
export PROC_COUNT=4
export NPOOL=2
export PWSCF_SCRATCH=/opt/scratch
export PWSCF_PP=/opt/pp
export PWSCF_CACHE=/opt/pwscf_cache
export PWSCF_BIN=/opt/qe/bin/pw.x


python3 ../../src/qeeos.py test.in
