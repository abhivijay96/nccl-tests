# Nccl performance test

This bash script runs the collective performance test with different number of GPUs and saves the output to log files.

## Usage: example All-to-all

To run the script, you need to have the `alltoall_perf` executable in the `../build` directory. You also need to pass an argument to the script, which is the maximum number of GPUs to use.

For example, to run the test from 2 to 8 GPUs, you can use:

    ./alltoall_test.sh 8

This will create log files named `alltoall_2.log`, `alltoall_3.log`, ..., `alltoall_8.log` in the current directory.

## Viewing results

The results can be viewed on a plot after the experiment is complete and the log files are generated. The following python command can be used to generate the plot.

    python3 plot.py alltoall <minimum_number_of_gpus_in_logs> <maximum_number_of_gpus_in_logs>
