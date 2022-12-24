#!/bin/bash
#SBATCH -n 20
#SBATCH --gres=gpu:1
#SBATCH --mem-per-cpu=2048
#SBATCH --time=2-00:00:00
#SBATCH --mail-type=END

python plot_results.py ../test1/a_minfreq_0.0_maxcs_1_maxor_0.7/patterns.txt ../test1/a.txt 10 5 2
