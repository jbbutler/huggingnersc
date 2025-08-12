#!/bin/bash 
#SBATCH -C gpu 
#SBATCH -A dasrepo
#SBATCH -q debug
#SBATCH -N 2
#SBATCH --ntasks-per-node 4
#SBATCH --cpus-per-task 32
#SBATCH --gpus-per-node 4
#SBATCH --time=00:01:00
#SBATCH --image=nersc/pytorch:24.08.01
#SBATCH --module=gpu,nccl-plugin
#SBATCH -o test.out

export MASTER_ADDR=$(hostname)
export MASTER_PORT=12355
export CUDA_VISIBLE_DEVICES=3,2,1,0

srun shifter bash -c "
    source export_vars.sh
    python distributed_dataloader.py
"