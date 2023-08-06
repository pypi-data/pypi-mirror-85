#!/usr/bin/env python
import argparse
import logging
import glob
import os
import pickle
import sys
from time import sleep

import numpy as np

from .caiman_constants import LOGGER_FORMAT, DEFAULT_MCORR_SETTINGS
from jobcreator.utils.misc import get_settings, write_hdf5_movie


def parse_args():
    parser = argparse.ArgumentParser(description="Suite2p parameters")
    parser.add_argument("--file", default=[], type=str, help="options")
    parser.add_argument("--ncpus", default=1, type=int, help="options")
    parser.add_argument("--mc_settings", default="", type=str, help="options")
    parser.add_argument("--job_name", default="", type=str, help="options")
    parser.add_argument("--output", default="", type=str, help="options")
    args = parser.parse_args()

    file_path = args.file
    n_cpus = args.ncpus
    mc_settings = args.mc_settings
    job_name = args.job_name
    output_dir = args.output

    return (
        file_path,
        n_cpus,
        mc_settings,
        job_name,
        output_dir,
    )


def run(
    file_path,
    n_cpus,
    motion_correct: bool = True,
    mc_settings: dict = {},
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
    from caiman.motion_correction import MotionCorrect
    from caiman.source_extraction.cnmf import params as params

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

    opts = params.CNMFParams(params_dict=mc_parameters)

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
        sleep(30)
    else:
        print("multiprocessing disabled")
        dview = None
        n_processes = 1
    print(n_processes)
    print("starting motion correction")
    sys.stdout.flush()

    mc = MotionCorrect(fnames, dview=dview, **opts.get_group("motion"))
    mc.motion_correct(save_movie=True)
    pw_rigid = mc_parameters["pw_rigid"]
    fname_mc = mc.fname_tot_els if pw_rigid else mc.fname_tot_rig
    if pw_rigid:
        bord_px = np.ceil(
            np.maximum(np.max(np.abs(mc.x_shifts_els)), np.max(np.abs(mc.y_shifts_els)))
        ).astype(np.int)
    else:
        bord_px = np.ceil(np.max(np.abs(mc.shifts_rig))).astype(np.int)

    border_nan = mc_parameters["border_nan"]
    bord_px = 0 if border_nan == "copy" else bord_px
    _ = cm.save_memmap(fname_mc, base_name="memmap_", order="C", border_to_0=bord_px)

    # if motion correction was performed, save the file
    # we save as hdf5 for better reading performance
    # downstream
    if motion_correct:
        print("saving motion corrected file")
        results_filebase = os.path.join(output_directory, job_name)
        mcorr_fname = results_filebase + "_mcorr.hdf5"
        dataset_name = opts.data["var_name_hdf5"]
        # fnames = opts.data["fnames"]
        # memmap_files = []
        # for f in fnames:
        #     if isinstance(f, bytes):
        #         f = f.decode()
        #     base_file = os.path.splitext(f)[0]
        #     if pw_rigid:
        #         memmap_pattern = base_file + "*_els_*"
        #     else:
        #         memmap_pattern = base_file + "*_rig_*"
        #     memmap_files += sorted(glob.glob(memmap_pattern))

        if pw_rigid:
            memmap_files = mc.fname_tot_els
        else:
            memmap_files = mc.fname_tot_rig

        # get the frame shape
        mov = cm.load(memmap_files[0])
        frame_shape = mov.shape[-2::]

        write_hdf5_movie(
            movie_name=mcorr_fname,
            memmap_files=memmap_files,
            frame_shape=frame_shape,
            dataset_name=dataset_name,
            compression="gzip",
        )

    # save the parameters in the same dir as the results
    final_params = opts.to_dict()
    params_file = os.path.join(output_directory, "all_mcorr_parameters.pkl")
    with open(params_file, "wb") as fp:
        pickle.dump(final_params, fp)

    # deleting mcorr unused memmap files
    if pw_rigid:
        memmap_files = mc.fname_tot_els
    else:
        memmap_files = mc.fname_tot_rig
    print(f"deleting {memmap_files}")
    for f in memmap_files:
        os.remove(f)

    print("stopping server")
    cm.stop_server(dview=dview)


def main():
    (file_path, n_cpus, mc_settings_path, job_name, output_dir,) = parse_args()

    mc_settings = get_settings(mc_settings_path)

    # run the pipeline
    run(
        file_path=file_path,
        n_cpus=n_cpus,
        mc_settings=mc_settings,
        job_name=job_name,
        output_directory=output_dir,
    )
