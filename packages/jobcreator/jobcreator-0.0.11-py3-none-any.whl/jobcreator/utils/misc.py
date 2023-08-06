import json
from typing import List, Optional, Tuple, Union

import h5py
import numpy as np


def get_settings(settings_path: str) -> dict:
    """helper function to load settings"""
    if settings_path == "default":
        settings = {}

    else:
        with open(settings_path, "r") as read_file:
            settings = json.load(read_file)

    return settings


def write_hdf5_movie(
    movie_name: str,
    memmap_files: Union[str, List[str]],
    frame_shape: Tuple[int, int],
    dataset_name: str = "mov",
    compression: Optional[str] = None,
):
    """Function to write an hdf5 formatted movie

    Parameters
    ----------
    movie_name : str
        name of the movie to be saved
    memmap_files : str or list
        the memmap files to be saved as an hdf5 movie.
        If a list of files is provided, they will all
        be concatenated into a single file
    frame_shape : tuple
        The shape of a single frame in the movie.
        The hdf5 file will be chunked by frame
    dataset_name : str
        The name of the dataset in the hdf5 file.
        The default value is 'mov'
    compression : Optional[str]
        The compression to be applied to the movie.
        Valid options are: 'gzip', 'lzf'
        See the h5py docs for the more information:
        https://docs.h5py.org/en/stable/high/dataset

    """
    from caiman import load

    with h5py.File(movie_name, mode="w") as h5f:
        _ = h5f.create_dataset(
            dataset_name,
            shape=(0,) + frame_shape,
            maxshape=(None,) + frame_shape,
            dtype=np.uint16,
            compression=compression,
            chunks=(1,) + frame_shape,
        )

    with h5py.File(movie_name, mode="a") as h5f:
        for f in memmap_files:
            mov = load(f)
            mov_array = mov.astype(np.uint16)
            dset = h5f[dataset_name]

            curr_length = dset.shape[0]
            mov_length = mov.shape[0]
            new_length = curr_length + mov_length
            new_shape = (new_length,) + frame_shape

            dset.resize(new_shape)
            dset[curr_length::, :, :] = mov_array

            h5f.flush()
