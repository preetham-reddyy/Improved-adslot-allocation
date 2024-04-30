#!/bin/bash
#SBATCH -n 20
#SBATCH --gres=gpu:1
#SBATCH --mem-per-cpu=2048
#SBATCH --time=2-00:00:00
#SBATCH --mail-type=END

python plot_results.py ../test1/bmspos_minfreq_0.02_maxcs_1_maxor_0.1/patterns.txt ../CMineMR-Mapreduce-algorithm-to-extract-coverage-patterns-master/dataset/bmspos.txt $1 4000 3000 $2
