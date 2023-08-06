import os


def caiman_job_file_bz(
    data_path: str,
    jobcreator_output_dir: str,
    job_name: str,
    email: str,
    n_cpu: int = 8,
    mem_per_cpu: int = 25,
    tmp_size: int = 150,
    job_time: str = "04:00:00",
    environment: str = "caiman",
    qos: str = "6hours",
    log_file: str = "myrun.o",
    error_file: str = "myrun.e",
    motion_correct: bool = True,
    mc_settings_file: str = "default",
    cnmf_settings_file: str = "default",
    qc_settings_file: str = "default",
):
    mem_per_cpu = str(mem_per_cpu) + "G"
    tmp_size = str(tmp_size) + "G"

    # get the name of the file and make the path to the temp dir
    data_pattern = os.path.join(data_path, "*.tif*")

    # create the flag for motion correction
    if motion_correct:
        mcorr_flag = "--motion_corr"
    else:
        mcorr_flag = ""

    # save the error and log files to the results dir
    log_file = os.path.join(jobcreator_output_dir, log_file)
    error_file = os.path.join(jobcreator_output_dir, error_file)

    # stub for naming the environment file
    env_file_stub = os.path.join(jobcreator_output_dir, "job_")

    job_file = f"""#!/bin/bash

#SBATCH --job-name={job_name}                   #This is the name of your job
#SBATCH --cpus-per-task={n_cpu}                  #This is the number of cores reserved
#SBATCH --mem-per-cpu={mem_per_cpu}              #This is the memory reserved per core.
#SBATCH --tmp={tmp_size}

#SBATCH --time={job_time}        #This is the time that your task will run
#SBATCH --qos={qos}           #You will run in this queue

# Paths to STDOUT or STDERR files should be absolute or relative to current working directory
#SBATCH --output={log_file}%j     #These are the STDOUT and STDERR files
#SBATCH --error={error_file}%j
#SBATCH --mail-type=END,FAIL,TIME_LIMIT
#SBATCH --mail-user={email}        #You will be notified via email when your task ends or fails


#Remember:
#The variable $TMPDIR points to the local hard disks in the computing nodes.
#The variable $HOME points to your home directory.
#The variable $SLURM_JOBID stores the ID number of your job.

# set environment variables
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1

#load your required modules below
#################################
module purge
module load Anaconda3

#add your command lines below
#############################
echo "moving files"
echo "moving files"
for file in {data_pattern}; do cp "$file" $TMP;done

echo "analysis"
source activate {environment}
conda env export > {env_file_stub}$SLURM_JOBID_env.yml

caiman_runner --file $TMP --ncpus {n_cpu} --mc_settings {mc_settings_file} --cnmf_settings {cnmf_settings_file} --qc_settings {qc_settings_file} --output {jobcreator_output_dir} --job_name {job_name} {mcorr_flag}

"""

    return job_file


def caiman_job_file_fmi(
    data_path: str,
    jobcreator_output_dir: str,
    job_name: str,
    email: str,
    n_cpu: int = 8,
    mem_per_cpu: int = 25,
    tmp_size: int = 150,
    job_time: str = "04:00:00",
    environment: str = "",
    qos: str = "cpu_short",
    log_file: str = "myrun.o",
    error_file: str = "myrun.e",
    motion_correct: bool = True,
    mc_settings_file: str = "default",
    cnmf_settings_file: str = "default",
    qc_settings_file: str = "default",
):

    # make sure the output directory is different from the data directory
    if os.path.samefile(data_path, jobcreator_output_dir):
        raise ValueError("data_path and output directory should not be the same")

    mem_per_cpu = str(mem_per_cpu) + "G"

    # set the default environment name if none specified
    if environment == "":
        environment = "/tungstenfs/scratch/garber/keviny/caiman_test/.venv/bin/activate"

    # get the name of the file and make the path to the temp dir
    data_pattern = os.path.join(data_path, "*.tif*")

    # create the flag for motion correction
    if motion_correct:
        mcorr_flag = "--motion_corr"
    else:
        mcorr_flag = ""

    # save the error and log files to the results dir
    log_file = os.path.join(jobcreator_output_dir, log_file)
    error_file = os.path.join(jobcreator_output_dir, error_file)

    # stub for naming the environment file
    env_file_stub = os.path.join(jobcreator_output_dir, "job_")

    job_file = f"""#!/bin/bash

#SBATCH --job-name={job_name}                   #This is the name of your job
#SBATCH --account=arber-caiman

#SBATCH --cpus-per-task={n_cpu}                  #This is the number of cores reserved
#SBATCH --mem-per-cpu={mem_per_cpu}              #This is the memory reserved per core.

#SBATCH --time={job_time}        #This is the time that your task will run
#SBATCH --partition={qos}           #You will run in this queue

#SBATCH --output={log_file}%j     #These are the STDOUT and STDERR files
#SBATCH --error={error_file}%j
#SBATCH --mail-type=END,FAIL,TIME_LIMIT
#SBATCH --mail-user={email}        #You will be notified via email when your task ends or fails

# set the environment variables
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1

echo "loading env"
source {environment}

echo "saving environment information"
env_file_extension="_env.txt"
pip freeze > "{env_file_stub}$SLURM_JOB_ID$env_file_extension"

# move the files
for file in {data_pattern}; do cp "$file" {jobcreator_output_dir};done

echo "analysis"
caiman_runner --file {jobcreator_output_dir} --ncpus {n_cpu} --mc_settings {mc_settings_file} --cnmf_settings {cnmf_settings_file} --qc_settings {qc_settings_file} --output {jobcreator_output_dir} --job_name {job_name} {mcorr_flag}

# remove the copied raw movies and memmap files
rm {jobcreator_output_dir}/*.tif*
rm {jobcreator_output_dir}/*.mmap
"""

    return job_file
