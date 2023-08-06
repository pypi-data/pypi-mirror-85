import argparse
import os

import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description="Suite2p parameters")
    parser.add_argument("--ops", default=[], type=str, help="options")
    parser.add_argument("--db", default=[], type=str, help="options")
    parser.add_argument("--tmp", default="", type=str, help="options")
    parser.add_argument("--file", default="", type=str, help="options")
    parser.add_argument("--key", default="", type=str, help="options")
    args = parser.parse_args()

    ops_path = args.ops
    db_path = args.db
    tmp_path = args.tmp
    file_name = args.file
    data_key = args.key
    return ops_path, db_path, tmp_path, file_name, data_key


def update_paths(ops_path, db_path, tmp_path, file_name, data_key):
    if ops_path == "[]":
        from suite2p.run_s2p import default_ops

        ops = default_ops()
    else:
        ops = np.load(ops_path, allow_pickle=True).item()

    if db_path == "[]":
        db = {}
    else:
        db = np.load(db_path, allow_pickle=True).item()

    # Modify the data path to the sciCORE job temp dir
    data_path = tmp_path
    fd_path = os.path.join(tmp_path, "fd")
    print("data: %s \n fd: %s" % (data_path, fd_path))

    ops["batch_size"] = 4000
    ops["input_format"] = "h5"

    db["data_path"] = []
    db["h5py"] = file_name
    db["h5py_key"] = data_key
    db["fast_disk"] = fd_path
    # db["save_folder"] = "/scicore/home/donafl00/yamauc0000/s2p_multisession"
    print(db)

    return ops, db


def main():
    ops_path, db_path, tmp_path, file_name, data_key = parse_args()
    ops, db = update_paths(ops_path, db_path, tmp_path, file_name, data_key)

    # save the files
    np.save("ops_job.npy", ops)
    np.save("db_tmp_job.npy", db)

    # import suite2p just before it is used so it is not required
    from suite2p import run_s2p

    # run the pipeline
    ops_end = run_s2p(ops=ops, db=db)
    np.save("ops_end.npy", ops_end)
