#!/bin/bash
#SBATCH -n 40
#SBATCH --gres=gpu:1
#SBATCH --mem-per-cpu=2048
#SBATCH --time=2-00:00:00
#SBATCH --mail-type=END

python plot_results.py ../test1/kosarak_output_0015 ../test1/kosarak.dat 10 4000 500
#python plot_results.py ../adslot/sclean_bmspos.txt_0.0033_0.0_0.01_output_1.txt ../adslot/sclean_bmspos.txt
#python plot_results.py kosarak.dat_0.0055_0.0_0.05_output.txt ../test1/kosarak.dat 3
