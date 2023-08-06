import glob
import os
import shutil

from jobcreator.utils.misc import get_settings
from jobcreator._pipeline_runners.caiman.caiman_runner import run as cm_runner


def caiman_desktop_runner(
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
    file_path = jobcreator_output_dir
    n_cpus = n_cpu

    # get the name of the file and make the path to the temp dir
    data_pattern = os.path.join(data_path, "*.tif*")
    image_files = glob.glob(data_pattern)
    for file in image_files:
        shutil.copy(file, jobcreator_output_dir)

    # load the settings files
    mc_settings = get_settings(mc_settings_file)
    cnmf_settings = get_settings(cnmf_settings_file)
    qc_settings = get_settings(qc_settings_file)

    cm_runner(
        file_path=file_path,
        n_cpus=n_cpus,
        motion_correct=motion_correct,
        mc_settings=mc_settings,
        cnmf_settings=cnmf_settings,
        qc_settings=qc_settings,
        job_name=job_name,
        output_directory=jobcreator_output_dir,
    )

    # delete redundant copied raw video
    copied_movies = glob.glob(os.path.join(jobcreator_output_dir, "*.tif*"))
    for mov in copied_movies:
        os.remove(mov)

    # delete mmap files
    mmap_files = glob.glob(os.path.join(jobcreator_output_dir, "*.mmap"))
    for mmap in mmap_files:
        os.remove(mmap)
