"""
Processing of image data
Author: Sergey Bobkov
"""

import os
import h5py
import numpy as np
from tqdm import tqdm

from . import config

DEFAULT_DATA = 'em_class_data.h5'
CONVERT_ROOT = 'converted_data'
CONVERT_PARAMS = ['q_max', 'q_min', 'binning', 'logscale']
ITERATION_PARAMS = ['model', 'rotations', 'classes', 'scale', 'mutual_info', 'loglh']
REPORT_PARAMS = ['rotations', 'classes', 'mutual_info']


def check_cxi_file(cxi_file):
    """Check if CXI file is present and include required data

    Keyword arguments:
    cxi_file -- CXI file

    Retuns:
    status -- True if everything correct, False otherwise
    """
    try:
        with h5py.File(cxi_file, 'r') as h5file:
            if 'entry_1/image_1/data' not in h5file:
                raise OSError
        return True
    except OSError:
        return False


def convert_cxi_data(data_file):
    """Convert data from CXI file into format suited for classification and save in in data_file

    Keyword arguments:
    data_file -- hdf5 file with classification data
    """

    params = config.load_config(data_file)

    with h5py.File(data_file, 'a') as h5file:
        if CONVERT_ROOT in h5file:
            del h5file[CONVERT_ROOT]

        convert_group = h5file.create_group(CONVERT_ROOT)
        for key in CONVERT_PARAMS:
            convert_group[key] = params[key]

        with h5py.File(params['cxi_file'], 'r') as cxi_file:
            entry = cxi_file['entry_1']
            image_keys = [k for k in entry.keys() if k.startswith('image_')]
            for k in tqdm(image_keys):
                cxi_image = entry[k]
                convert_image = convert_group.create_group(k)
                convert_image_group(cxi_image, convert_image, params)
                create_sparse_data(convert_image)
                # Remove dense data
                del convert_image['data']


def convert_image_group(cxi_image, convert_image, params, chunk_size=1000):
    """Convert image group from CXI file and save result in convert_image group

    Keyword arguments:
    cxi_image -- image group in CXI file
    convert_image -- empty group to save converted data
    params -- dict with parameters
    chunk_size -- number of frames processed at once
    """
    data_dset = cxi_image['data']
    mask = cxi_image['mask'][:]
    center = cxi_image['image_center'][:]

    assert center.shape == (3,)
    assert mask.ndim == 2
    assert data_dset.ndim == 3
    assert data_dset.shape[1:] == mask.shape

    num_frames = data_dset.shape[0]

    q_max = params['q_max']

    if q_max != 0:
        eff_width = 2*q_max + 2
        x_start = max(np.floor(center[0] - eff_width//2).astype(int), 0)
        x_end = min(np.floor(center[0] + eff_width//2).astype(int), data_dset.shape[2])
        y_start = max(np.floor(center[1] - eff_width//2).astype(int), 0)
        y_end = min(np.floor(center[1] + eff_width//2).astype(int), data_dset.shape[1])
        corr_center = np.array([center[0] - x_start, center[1] - y_start, 0])
        mask_buf = mask[y_start:y_end, x_start:x_end]
    else:
        corr_center = center
        mask_buf = mask

    for chunk_start in tqdm(range(0, num_frames, chunk_size), position=1):
        chunk_end = chunk_start + chunk_size
        if q_max != 0:
            data_buf = data_dset[chunk_start:chunk_end, y_start:y_end, x_start:x_end]
        else:
            data_buf = data_dset[chunk_start:chunk_end]

        q_values, t_values, converted_data_buf = \
            convert_data(data_buf, mask_buf, corr_center, params)

        if chunk_start == 0:
            convert_image.create_dataset('q_values', data=q_values, compression="lzf")
            convert_image.create_dataset('t_values', data=t_values, compression="lzf")
            converted_data_dset = convert_image.create_dataset(
                'data', shape=(num_frames, len(q_values)),
                chunks=(1, len(q_values)), compression="lzf")

        if params['logscale']:
            converted_data_buf = np.log(converted_data_buf + 1)

        converted_data_dset[chunk_start:chunk_end] = converted_data_buf
        del converted_data_buf


def convert_data(data, mask, center, params):
    """Convert 3D image array into set of points with polar coordinates

    Keyword arguments:
    data -- 3D image array (index, y, x)
    mask -- 2D mask for image array
    center -- image center coordinates
    params -- dict with parameters

    Return:
    q_values -- point radius in polar coordinates
    t_values -- point angles in polar coordinates
    converted_data_buf -- 2D array with intensity values (image_index, point_index)
    """

    binning = params['binning']
    q_max = params['q_max']
    q_min = params['q_min']
    friedel = params['friedel']

    if binning > 1:
        mask = (apply_binning(mask, binning) > 0)

    q_grid, t_grid = polar_coords(mask.shape, center/binning)
    q_values = q_grid[mask == 0]
    t_values = t_grid[mask == 0]

    if friedel:
        q_values = np.concatenate([q_values, q_values])
        t_values = np.concatenate([t_values, t_values + np.pi])

    q_filter = np.ones_like(q_values, dtype=bool)
    if q_max != 0:
        q_filter *= (q_values <= q_max/binning)
    if q_min != 0:
        q_filter *= (q_values >= q_min/binning)

    q_values = q_values[q_filter]
    t_values = t_values[q_filter]

    converted_data_buf = np.zeros((len(data), len(q_values)), dtype=data.dtype)

    for j, data_frame in enumerate(data):
        frame_vals = apply_binning(data_frame, binning)[mask == 0]
        if friedel:
            frame_vals = np.concatenate([frame_vals, frame_vals])

        converted_data_buf[j] = frame_vals[q_filter]

    return q_values, t_values, converted_data_buf


def polar_coords(shape, center):
    """Compute polar coordinates for grid with defined shape and center

    Keyword arguments:
    shape -- 2D grid shape
    center -- center coordinates

    Return:
    q_grid -- array of point radius in polar coordinates
    t_grid -- array of point angles in polar coordinates
    """
    assert len(shape) == 2
    assert center.shape == (3,)

    size_y, size_x = shape

    x_range = np.arange(size_x) - center[0]
    y_range = np.arange(size_y) - center[1]

    x_grid, y_grid = np.meshgrid(x_range, y_range)

    q_grid = np.sqrt(x_grid**2 + y_grid**2)
    t_grid = np.arctan2(y_grid, x_grid)

    return q_grid, t_grid


def apply_binning(data, binning):
    """Apply binning to 2D image, combine groups of x*x pixels
    and return sum of intensities in each group

    Keyword arguments:
    data -- 2D image
    binning -- size of binned group, i.e. 2 for 2 by 2 binning.

    Return:
    binned_data -- binned image
    """
    size_y, size_x = data.shape

    bin_x = size_x//binning #+ (1 if X%bin_value > bin_value//2 else 0)
    bin_y = size_y//binning #+ (1 if Y%bin_value > bin_value//2 else 0)

    binned_data = data[:bin_y*binning, :bin_x*binning]
    binned_data = binned_data.reshape(bin_y, binning, bin_x, binning).sum(axis=(1, 3))

    return binned_data


def create_sparse_data(convert_image):
    """Replace 'data' with sparse 'values' and 'indexes' datasets

    Keyword arguments:
    convert_image -- group with 'data' to process
    """
    data_dset = convert_image['data']
    num_frames = len(data_dset)
    max_npix = np.count_nonzero(data_dset, axis=1).max()

    values_dest = convert_image.create_dataset('values', dtype=data_dset.dtype,
                                               shape=(num_frames, max_npix), chunks=(1, max_npix),
                                               compression="lzf")
    index_dest = convert_image.create_dataset('indexes', dtype='i4',
                                              shape=(num_frames, max_npix), chunks=(1, max_npix),
                                              compression="lzf")

    for i, frame in enumerate(data_dset):
        idx = np.nonzero(frame > 0)[0]
        index_dest[i, :len(idx)] = idx
        values_dest[i, :len(idx)] = frame[idx]


def load_convert_params(data_file):
    """Load params of convertion for data_file

    Keyword arguments:
    data_file -- hdf5 file with classification data

    Return:
    convert_params -- dict with convert params (None if not available)
    """
    convert_params = {}
    with h5py.File(data_file, 'r') as h5file:
        if CONVERT_ROOT not in h5file:
            return None

        convert_group = h5file[CONVERT_ROOT]
        for key in convert_group:
            if key.startswith('image_'):
                image = convert_group[key]
                if 'values' not in image or 'indexes' not in image:
                    return None

        for key in CONVERT_PARAMS:
            if key not in convert_group:
                return None
            convert_params[key] = convert_group[key][()]

        return convert_params


def get_converted_group_names(data_file):
    """Get names of groups in converted data

    Keyword arguments:
    data_file -- hdf5 file with classification data

    Return:
    converted_group_names -- list of group names
    """

    with h5py.File(data_file, 'r') as h5file:
        if CONVERT_ROOT not in h5file:
            raise ValueError('Converted data is not available')

        convert_group = h5file[CONVERT_ROOT]

        converted_group_names = [name for name in convert_group.keys()
                                 if isinstance(convert_group[name], h5py.Group)]

    return converted_group_names


def get_num_frames(data_file, group_name):
    """Get number of frames in group

    Keyword arguments:
    data_file -- hdf5 file with classification data
    group_name -- name of group in converted data

    Return:
    length -- number of frames
    """

    with h5py.File(data_file, 'r') as h5file:
        if CONVERT_ROOT not in h5file:
            raise ValueError('Converted data is not available')

        convert_group = h5file[CONVERT_ROOT]
        data_group = convert_group[group_name]

        return data_group['values'].shape[0]


def _load_converted_data(data_file, group_name, dataset, start=0, end=0):
    """Load data from converted dataset

    Keyword arguments:
    data_file -- hdf5 file with classification data
    group_name -- name of group in converted data
    dataset -- name of dataset to read
    start -- start index for dataset slice
    end -- end index index for dataset slice

    Return:
    data -- loaded data
    """

    with h5py.File(data_file, 'r') as h5file:
        if CONVERT_ROOT not in h5file:
            raise ValueError('Converted data is not available')

        convert_group = h5file[CONVERT_ROOT]
        data_group = convert_group[group_name]
        data_dset = data_group[dataset]

        if end == 0:
            end = data_dset.shape[0]

        return data_dset[start:end]


def load_q_values(data_file, group_name):
    """Load 'q_values' datasets from converted data

    Keyword arguments:
    data_file -- hdf5 file with classification data
    group_name -- name of group in converted data

    Return:
    q_values -- loaded data
    """
    return _load_converted_data(data_file, group_name, 'q_values')


def load_t_values(data_file, group_name):
    """Load 'q_values' datasets from converted data

    Keyword arguments:
    data_file -- hdf5 file with classification data
    group_name -- name of group in converted data

    Return:
    q_values -- loaded data
    """
    return _load_converted_data(data_file, group_name, 't_values')


def load_data_values(data_file, group_name, start=0, end=0):
    """Load sparse data from group in converted data

    Keyword arguments:
    data_file -- hdf5 file with classification data
    group_name -- name of group in converted data
    start -- start index for dataset slice
    end -- end index index for dataset slice

    Return:
    values -- data values
    indexes -- indexes for data values
    """
    values = _load_converted_data(data_file, group_name, 'values', start, end)
    indexes = _load_converted_data(data_file, group_name, 'indexes', start, end)
    return values, indexes


def reset_data(data_file):
    """Replace data_file with new file with same config

    Keyword arguments:
    data_file -- hdf5 file with classification data
    """
    param = config.load_config(data_file)
    os.remove(data_file)
    config.save_config(data_file, param)


def load_iteration_data(data_file, iteration, for_report=False):
    """Load iteration result from data_file

    Keyword arguments:
    data_file -- hdf5 file with classification data
    iteration -- iteration number
    for_report -- load only data for report

    Return:
    it_data -- dict with iteration data
    """
    if iteration <= 0:
        raise ValueError("Iteration cannot be <= 0, got {}".format(iteration))
    elif iteration > get_num_saved_iterations(data_file):
        raise ValueError("Data for itaration {} is not available".format(iteration))

    with h5py.File(data_file, 'r') as h5file:
        it_group = h5file['iter_{}'.format(iteration)]
        it_data = {}
        for k in ITERATION_PARAMS:
            if for_report and k not in REPORT_PARAMS:
                continue
            it_data[k] = it_group[k][...]

        return it_data


def get_num_saved_iterations(data_file):
    """Return number of saved iterations in data_file

    Keyword arguments:
    data_file -- hdf5 file with classification data

    Return:
    iter_num -- number of saved iterations
    """
    with h5py.File(data_file, 'r') as h5file:
        iter_numbers = []
        for k in h5file.keys():
            if k.startswith('iter_'):
                iter_numbers.append(int(k[5:]))

        if not iter_numbers:
            return 0

        return max(iter_numbers)


def save_iteration_data(data_file, it_data):
    """Save iteration result to data_file

    Keyword arguments:
    data_file -- hdf5 file with classification data
    it_data -- dict with iteration data

    Return:
    iteration -- number of saved iteration
    """
    iteration = get_num_saved_iterations(data_file) + 1
    with h5py.File(data_file, 'a') as h5file:
        it_group = h5file.require_group('iter_{}'.format(iteration))

        for k in ITERATION_PARAMS:
            it_group[k] = it_data[k]

    return iteration


def save2cxi(cxi_file, data, dset_name):
    """Save classification result into CXI file

    Keyword arguments:
    cxi_file -- CXI file
    data -- 1D array with data, length should be equal to number of frames in CXI file
    dset_name -- name for result dataset within image_n group
    """

    start = 0

    with h5py.File(cxi_file, 'a') as cxi_file:
        entry = cxi_file['entry_1']
        for k in entry.keys():
            if k.startswith('image_'):
                cxi_image = entry[k]
                if dset_name in cxi_image:
                    del cxi_image[dset_name]

                num_frames = cxi_image['data'].shape[0]
                end = start + num_frames
                cxi_image[dset_name] = data[start:end]
                start += num_frames

    if end != len(data):
        raise ValueError('Data lenght not equal to frames number: {} != {}'.format(end, len(data)))
