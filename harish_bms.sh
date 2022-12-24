#!/bin/bash
#SBATCH -n 10
#SBATCH --gres=gpu:1
#SBATCH --mem-per-cpu=2048
#SBATCH --time=2-00:00:00
#SBATCH --mail-type=END

ADS=$1
NA=20
while [ $NA -le 400 ]
do
	python plot_results.py ../test1/bmspos_minfreq_0.0025_maxcs_1_maxor_0.01/patterns.txt ../CMineMR-Mapreduce-algorithm-to-extract-coverage-patterns-master/dataset/bmspos.txt $NA 4000 3000 $ADS
	((NA = NA + 20))	
done
#python plot_results.py ../test1/kosarak_minfreq_0.005_maxcs_1_maxor_0.04/patterns.txt ../CMineMR-Mapreduce-algorithm-to-extract-coverage-patterns-master/dataset/kosarak.txt $1 7000 6000
