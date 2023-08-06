import argparse
import json
import os
import subprocess

from ._job_templates import (
    suite2p_job_file,
    caiman_job_file_bz,
    caiman_job_file_fmi,
    caiman_mcorr_job_fmi,
)
from ._pipeline_runners.caiman.caiman_desktop_runner import caiman_desktop_runner
from ._pipeline_checks import check_caiman

JOB_FILE_GENERATORS = {
    "suite2p": suite2p_job_file,
    "caiman": caiman_job_file_bz,
    "caiman-fmi": caiman_job_file_fmi,
    "caiman-mcorr-fmi": caiman_mcorr_job_fmi,
}
PIPELINE_CHECKERS = {"caiman": check_caiman}
DESKTOP_RUNNERS = {"caiman": caiman_desktop_runner}


def parse_args():
    parser = argparse.ArgumentParser(description="Pipeline parameters")
    parser.add_argument("--pipeline", default="", type=str, help="options")
    parser.add_argument("--settings", default="", type=str, help="options")
    parser.add_argument("--output", default=".", type=str, help="options")
    parser.add_argument("--test", action="store_true")

    args = parser.parse_args()

    pipeline_name = args.pipeline
    settings_path = args.settings
    output_dir = args.output
    test = args.test

    return pipeline_name, settings_path, output_dir, test


def main():
    pipeline_name, settings_path, output_dir, test = parse_args()

    if test is True:
        checker_function = PIPELINE_CHECKERS[pipeline_name]
        checker_function()
    else:
        # make the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        else:
            raise ValueError("output must be saved to a new directory")

        job_file_path = os.path.join(output_dir, "job_file.sh")

        with open(settings_path, "r") as read_file:
            job_settings = json.load(read_file)

        # add the output directory to the job file settings
        job_settings["jobcreator_output_dir"] = output_dir

        # get the file text
        job_file_gen = JOB_FILE_GENERATORS[pipeline_name]
        job_file_text = job_file_gen(**job_settings)

        # make the file job file
        with open(job_file_path, "w") as text_file:
            text_file.write(job_file_text)

        # run the job
        subprocess.run(["sbatch", job_file_path])


def desktop_runner():
    pipeline_name, settings_path, output_dir, test = parse_args()

    if test is True:
        checker_function = PIPELINE_CHECKERS[pipeline_name]
        checker_function()
    else:
        # make the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        else:
            raise ValueError("output must be saved to a new directory")

        with open(settings_path, "r") as read_file:
            job_settings = json.load(read_file)

        # add the output directory to the job file settings
        job_settings["jobcreator_output_dir"] = output_dir

        # get the file text
        runner = DESKTOP_RUNNERS[pipeline_name]
        runner(**job_settings)
