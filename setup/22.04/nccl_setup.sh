#!/bin/bash

wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt-get update

sudo apt install libnccl2=2.18.1-1+cuda12.1 libnccl-dev=2.18.1-1+cuda12.1