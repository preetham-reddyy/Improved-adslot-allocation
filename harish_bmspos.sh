#!/bin/bash
#SBATCH -n 30
#SBATCH --gres=gpu:0
#SBATCH --mem-per-cpu=2048
#SBATCH --time=2-00:00:00
#SBATCH --mail-type=END

python plot_results.py ../test1/bmspos_minfreq_0.015_maxcs_1_maxor_0.15/patterns.txt ../CMineMR-Mapreduce-algorithm-to-extract-coverage-patterns-master/dataset/bmspos.txt 400 5000 2000
