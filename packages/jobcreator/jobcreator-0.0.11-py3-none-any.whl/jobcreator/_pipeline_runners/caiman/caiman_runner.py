#!/usr/bin/env python
import argparse
import logging
import glob
import os
import pickle
import sys
from time import sleep

import numpy as np

from .caiman_constants import (
    LOGGER_FORMAT,
    DEFAULT_MCORR_SETTINGS,
    DEFAULT_CNMF_PARAMETERS,
    DEFAULT_QC_PARAMETERS,
)
from jobcreator.utils.misc import get_settings, write_hdf5_movie


def parse_args():
    parser = argparse.ArgumentParser(description="Suite2p parameters")
    parser.add_argument("--file", default=[], type=str, help="options")
    parser.add_argument("--ncpus", default=1, type=int, help="options")
    parser.add_argument("--motion_corr", action="store_true")
    parser.add_argument("--mc_settings", default="", type=str, help="options")
    parser.add_argument("--cnmf_settings", default="", type=str, help="options")
    parser.add_argument("--qc_settings", default="", type=str, help="options")
    parser.add_argument("--job_name", default="", type=str, help="options")
    parser.add_argument("--output", default="", type=str, help="options")
    args = parser.parse_args()

    file_path = args.file
    n_cpus = args.ncpus
    motion_correct = args.motion_corr
    mc_settings = args.mc_settings
    cnmf_settings = args.cnmf_settings
    qc_settings = args.qc_settings
    job_name = args.job_name
    output_dir = args.output

    return (
        file_path,
        n_cpus,
        motion_correct,
        mc_settings,
        cnmf_settings,
        qc_settings,
        job_name,
        output_dir,
    )


def run(
    file_path,
    n_cpus,
    motion_correct: bool = True,
    quality_control: bool = False,
    mc_settings: dict = {},
    cnmf_settings: dict = {},
    qc_settings: dict = {},
    job_name: str = "job",
    output_directory: str = "",
):
    mkl = os.environ.get("MKL_NUM_THREADS")
    blas = os.environ.get("OPENBLAS_NUM_THREADS")
    vec = os.environ.get("VECLIB_MAXIMUM_THREADS")
    print(f"MKL: {mkl}")
    print(f"blas: {blas}")
    print(f"vec: {vec}")

    # we import the pipeline upon running so they aren't required for all installs
    import caiman as cm
    from caiman.source_extraction.cnmf import params as params
    from caiman.source_extraction import cnmf

    # print the directory caiman is imported from
    caiman_path = os.path.abspath(cm.__file__)
    print(f"caiman path: {caiman_path}")
    sys.stdout.flush()

    # setup the logger
    logger_file = os.path.join(output_directory, "caiman.log")
    logging.basicConfig(
        format=LOGGER_FORMAT, filename=logger_file, filemode="w", level=logging.DEBUG,
    )

    # if indices to perform mcorr are set, format them
    if "indices" in mc_settings:
        indices = mc_settings["indices"]

        indices_formatted = ()
        for axis_slice in indices:
            start = axis_slice[0]
            stop = axis_slice[1]
            if len(axis_slice) == 3:
                step = axis_slice[2]
            else:
                step = 1
            indices_formatted += (slice(start, stop, step),)
        mc_settings["indices"] = indices_formatted
    # load and update the pipeline settings
    mc_parameters = DEFAULT_MCORR_SETTINGS
    for k, v in mc_settings.items():
        mc_parameters[k] = v
    cnmf_parameters = DEFAULT_CNMF_PARAMETERS
    for k, v in cnmf_settings.items():
        cnmf_parameters[k] = v
    qc_parameters = DEFAULT_QC_PARAMETERS
    for k, v in qc_settings.items():
        qc_parameters[k] = v
    opts = params.CNMFParams(params_dict=mc_parameters)
    opts.change_params(params_dict=cnmf_parameters)
    opts.change_params(params_dict=qc_parameters)

    # get the filenames
    if os.path.isfile(file_path):
        print(file_path)
        fnames = [file_path]
    else:
        file_pattern = os.path.join(file_path, "*.tif*")
        fnames = sorted(glob.glob(file_pattern))
    print(fnames)
    opts.set("data", {"fnames": fnames})

    if n_cpus > 1:
        print("starting server")
        # start the server
        n_proc = np.max([(n_cpus - 1), 1])
        c, dview, n_processes = cm.cluster.setup_cluster(
            backend="local", n_processes=n_proc, single_thread=False
        )
        print(n_processes)
        sleep(30)
    else:
        print("multiprocessing disabled")
        dview = None
        n_processes = 1

    print("starting analysis")
    print(f"perform motion correction: {motion_correct}")
    print(f"perform qc: {quality_control}")
    sys.stdout.flush()
    cnm = cnmf.CNMF(n_processes, params=opts, dview=dview)
    cnm_results = cnm.fit_file(
        motion_correct=motion_correct, include_eval=quality_control
    )

    print("evaluate components")
    sys.stdout.flush()
    Yr, dims, T = cm.load_memmap(cnm_results.mmap_file)
    images = Yr.T.reshape((T,) + dims, order="F")
    cnm_results.estimates.evaluate_components(images, cnm.params, dview=dview)
    print("Number of total components: ", len(cnm_results.estimates.C))
    print("Number of accepted components: ", len(cnm_results.estimates.idx_components))

    # save the results object
    print("saving results")
    results_filebase = os.path.join(output_directory, job_name)
    cnm_results.save(results_filebase + ".hdf5")

    # if motion correction was performed, save the file
    # we save as hdf5 for better reading performance
    # downstream
    if motion_correct:
        print("saving motion corrected file")
        mcorr_fname = results_filebase + "_mcorr.hdf5"
        dataset_name = cnm_results.params.data["var_name_hdf5"]
        fnames = cnm_results.params.data["fnames"]
        memmap_files = []
        for f in fnames:
            if isinstance(f, bytes):
                f = f.decode()
            base_file = os.path.splitext(f)[0]
            if cnm_results.params.motion["pw_rigid"]:
                memmap_pattern = base_file + "*_els_*"
            else:
                memmap_pattern = base_file + "*_rig_*"
            memmap_files += sorted(glob.glob(memmap_pattern))
        write_hdf5_movie(
            movie_name=mcorr_fname,
            memmap_files=memmap_files,
            frame_shape=cnm_results.dims,
            dataset_name=dataset_name,
            compression="gzip",
        )

    # save the parameters in the same dir as the results
    final_params = cnm.params.to_dict()
    params_file = os.path.join(output_directory, "all_caiman_parameters.pkl")
    with open(params_file, "wb") as fp:
        pickle.dump(final_params, fp)

    print("stopping server")
    cm.stop_server(dview=dview)


def main():
    (
        file_path,
        n_cpus,
        motion_correct,
        mc_settings_path,
        cnmf_settings_path,
        qc_settings_path,
        job_name,
        output_dir,
    ) = parse_args()

    mc_settings = get_settings(mc_settings_path)
    cnmf_settings = get_settings(cnmf_settings_path)
    qc_settings = get_settings(qc_settings_path)

    # run the pipeline
    run(
        file_path=file_path,
        n_cpus=n_cpus,
        motion_correct=motion_correct,
        mc_settings=mc_settings,
        cnmf_settings=cnmf_settings,
        qc_settings=qc_settings,
        job_name=job_name,
        output_directory=output_dir,
    )
