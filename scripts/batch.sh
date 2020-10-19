#!/bin/bash
#
#
# Batch file for bluebear uses SBATCH scheduler
#
#
#
#SBATCH --job-name=pwaltest
#SBATCH --output=jobout.txt
#SBATCH --account=readmsd02
#
#SBATCH --ntasks 20
#SBATCH --nodes 1
#SBATCH --time=30:00
#SBATCH --cpus-per-task=1

#
#SBATCH --get-user-env
#SBATCH --export=NONE
#
unset SLURM_EXPORT_ENV

module purge; module load bluebear
module load bear-apps/2018a
module load iomkl/2018a
module load Python/3.6.3-iomkl-2018a
module load matplotlib/2.1.1-iomkl-2018a-Python-3.6.3



# Change to $PBS_O_WORKDIR
cd "$PBS_O_WORKDIR"

mkdir /scratch/bxp912

#BB_SCRATCH=$(mktemp -d /scratch/${USER}/${SLURM_JOBID})

# Set the number of threads to 1
export OMP_NUM_THREADS=1
export PROC_COUNT=20
export PWSCF_SCRATCH=/scratch/bxp912
export PWSCF_PP=/rds/homes/b/bxp912/pp
export PWSCF_CACHE=/rds/homes/b/bxp912/pwscf_cache
export PWSCF_BIN=/rds/homes/b/bxp912/apps/qe-6.3/bin/pw.x
export PWSCF_SCRIPT=/rds/homes/b/bxp912/apps/qe-6.3/bin/pw.sh

python /rds/homes/b/bxp912/apps/python/qeeos.py input.in > result.txt
