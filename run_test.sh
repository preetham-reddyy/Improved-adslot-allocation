#!/bin/bash
#SBATCH -n 10
#SBATCH --gres=gpu:0
#SBATCH --mem-per-cpu=2048
#SBATCH --time=2-00:00:00
#SBATCH --mail-type=END

# python plot_results.py patterns/kosarak.txt dataset/kosarak.dat $1 $2 $3
# python plot_results.py patterns/kosarak.txt dataset/kosarak.dat 500 8000 5000
# python plot_results.py patterns/kosarak.txt dataset/kosarak.dat 500 9000 6000
# python plot_results.py patterns/kosarak.txt dataset/kosarak.dat 500 10000 8000
# python plot_results.py patterns/TIK1.txt dataset/T40I10D100K.txt $1 $2 $3
python plot_results.py patterns/k100_patterns.txt dataset/k100.txt $1 $2 $3
#python plot_results.py ./kosarak.dat_0.0055_0.0_0.05_output.txt dataset/kosarak.dat $1 $2 $3
