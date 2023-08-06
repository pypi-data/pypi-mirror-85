LOGGER_FORMAT = (
    "%(relativeCreated)12d [%(filename)s:%(funcName)20s():%(lineno)s]"
    "[%(process)d] %(message)s"
)
DEFAULT_MCORR_SETTINGS = {
    "fr": 10,  # movie frame rate
    "decay_time": 0.4,  # length of a typical transient in second
    "pw_rigid": False,  # flag for performing piecewise-rigid motion correction
    "max_shifts": (5, 5),  # maximum allowed rigid shift
    "gSig_filt": (3, 3),  # size of high pass spatial filtering, used in 1p data
    "strides": (48, 48),
    "overlaps": (24, 24),
    "max_deviation_rigid": (
        3
    ),  # maximum deviation allowed for patch with respect to rigid shifts
    "border_nan": "copy",  # replicate values along the boundaries
}
DEFAULT_CNMF_PARAMETERS = {
    "method_init": "corr_pnr",  # use this for 1 photon
    "K": None,  # upper bound on number of components per patch, in general None
    "gSig": (3, 3),  # gaussian width of a 2D gaussian kernel
    "gSiz": (13, 13),  # average diameter of a neuron, in general 4*gSig+1
    "merge_thr": 0.7,  # merging threshold, max correlation allowed
    "p": 1,  # order of the autoregressive system
    "tsub": 2,  # downsampling factor in time for initialization
    "ssub": 1,  # downsampling factor in space for initialization,
    "rf": 40,  # half-size of the patches in pixels
    "stride": 20,  # amount of overlap between the patches in pixels
    "only_init": True,  # set it to True to run CNMF-E
    "nb": 0,  # number of background components (rank) if positive
    "nb_patch": 0,  # number of background components (rank) per patch if gnb>0
    "method_deconvolution": "oasis",  # could use 'cvxpy' alternatively
    "low_rank_background": None,
    "update_background_components": True,
    # sometimes setting to False improve the results
    "min_corr": 0.8,  # min peak value from correlation image
    "min_pnr": 10,  # min peak to noise ration from PNR image
    "normalize_init": False,  # just leave as is
    "center_psf": True,  # leave as is for 1 photon
    "ssub_B": 2,  # additional downsampling factor in space for background
    "ring_size_factor": 1.4,  # radius of ring is gSiz*ring_size_factor,
    "del_duplicates": True,
    "border_pix": 0,
}
DEFAULT_QC_PARAMETERS = {
    "min_SNR": 2.5,  # adaptive way to set threshold on the transient size
    "rval_thr": 0.85,
    "use_cnn": False,
}
