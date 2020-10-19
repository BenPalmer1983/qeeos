#!/bin/bash

#
#  Wrapper Script for PWscf
#
#  What is does:
#
#  clears out scratch directory before running pwscf
#  
#
#


touch bash.log
timestamp=$(date +%s)

echo "=============================================================================" >> bash.log
echo "              START                                 " >> bash.log
echo $timestamp >> bash.log
echo "=============================================================================" >> bash.log

echo $OMP_NUM_THREADS >> bash.log
echo $PROC_COUNT >> bash.log
echo $PWSCF_SCRATCH >> bash.log
echo $PWSCF_PP >> bash.log
echo $PWSCF_CACHE >> bash.log
echo $PWSCF_BIN >> bash.log
echo $PWSCF_SCRIPT >> bash.log

mkdir $PWSCF_SCRATCH
rm -R $PWSCF_SCRATCH/*

echo "" >> bash.log
df -h >> bash.log
lscpu >> bash.log
free -h >> bash.log
echo "=============================================================================" >> bash.log
echo $1 >> bash.log
echo $2 >> bash.log
echo $3 >> bash.log
echo "=============================================================================" >> bash.log
echo "              RUNNING                                 " >> bash.log
mpirun -n $1 $PWSCF_BIN < $2  > $3 
echo "=============================================================================" >> bash.log
df -h >> bash.log
echo "=============================================================================" >> bash.log
echo "              END                                 " >> bash.log
echo $timestamp >> bash.log
echo "=============================================================================" >> bash.log
echo "" >> bash.log
echo "" >> bash.log
echo "" >> bash.log
echo "" >> bash.log
echo "" >> bash.log
echo "" >> bash.log
echo "" >> bash.log
echo "" >> bash.log
echo "" >> bash.log
echo "" >> bash.log
echo "" >> bash.log
