"""
Functions for EM computation
Author: Sergey Bobkov
"""
import numpy as np
from numba import njit, prange


@njit(parallel=True, fastmath=True)
def extract_all_model(model, q_vals, t_vals, rotations, out_data):
    """Extract model for all classes in all rotations

    Keyword arguments:
    model -- 3D model array (num_class, y, x)
    q_vals -- radius values for extraction
    t_vals -- angle values for extraction
    rotations -- array with values of angles for rotations
    out_data -- result will be written here
    """
    num_class = len(model)
    num_rot = len(rotations)
    for i in prange(num_class*num_rot):
        k = i // num_rot
        j = i % num_rot
        rot = rotations[j]
        extract_model(model[k], q_vals, t_vals + rot, out_data[k, j])


@njit(fastmath=True)
def extract_model(model, q_vals, t_vals, out_data):
    """Extract model for particular class in particular rotation

    Keyword arguments:
    model -- 2D model array (y, x)
    q_vals -- radius values for extraction
    t_vals -- angle values for extraction
    out_data -- result will be written here
    """
    assert len(q_vals) == len(t_vals)

    center = (model.shape[0]-1) // 2
    out_data[:] = 0

    for i in range(len(q_vals)):
        x_val = q_vals[i]*np.cos(t_vals[i]) + center
        y_val = q_vals[i]*np.sin(t_vals[i]) + center

        x_fl = int(np.floor(x_val))
        y_fl = int(np.floor(y_val))

        x_frac = x_val - x_fl
        y_frac = y_val - y_fl

        res = 0

        if test_valid(y_fl, model.shape[0]) and test_valid(x_fl, model.shape[1]):
            res += (1 - x_frac)*(1 - y_frac)*model[y_fl, x_fl]

        if test_valid(y_fl, model.shape[0]) and test_valid(x_fl + 1, model.shape[1]):
            res += (x_frac)*(1 - y_frac)*model[y_fl, x_fl + 1]

        if test_valid(y_fl + 1, model.shape[0]) and test_valid(x_fl, model.shape[1]):
            res += (1 - x_frac)*(y_frac)*model[y_fl + 1, x_fl]

        if test_valid(y_fl + 1, model.shape[0]) and test_valid(x_fl + 1, model.shape[1]):
            res += (x_frac)*(y_frac)*model[y_fl + 1, x_fl + 1]

        out_data[i] = res


@njit
def test_valid(value, max_val):
    """Test if 0 <= value < max_val"""
    if 0 <= value < max_val:
        return True
    return False


@njit(parallel=True, fastmath=True) # fastmath=True cause dead stuck with MPI
def compute_all_loglh(data_vals, data_idx, data_scale, model_slice, out_loglh):
    """Compute log-likelihood for all frames against all classes in all orientations

    Keyword arguments:
    data_vals -- values of data intensity
    data_idx -- indexes for data values against model_slice values
    data_scale -- scale of individual frames in data
    model_slice -- slice of model computed at all requred rotations
    num_class -- number of classes (number of models)
    num_rot -- number of rotations
    out_loglh -- result will be written here
    """
    num_class, num_rot = model_slice.shape[:2]
    for i in prange(num_class*num_rot):
        k = i // num_rot
        j = i % num_rot
        compute_loglh(data_vals, data_idx, data_scale,
                      model_slice[k, j], out_loglh[k, j])


@njit(fastmath=True) # fastmath=True cause dead stuck with MPI
def compute_loglh(data_vals, data_idx, data_scale,
                  model_slice, out_loglh):
    """Compute log-likelihood for all frames against one model in one orientation

    Keyword arguments:
    data_vals -- values of data intensity
    data_idx -- indexes for data values against model_slice values
    data_scale -- scale of individual frames in data
    model_slice -- slice of one model in one orientation
    out_loglh -- result will be written here
    """
    n_frames = data_vals.shape[0]
    model_sum = model_slice.sum()
    for k in range(n_frames):
        out_loglh[k] = frame_loglh(data_vals[k], data_idx[k], data_scale[k], model_slice) - \
                        model_sum*data_scale[k]



@njit(fastmath=True)
def frame_loglh(frame_vals, frame_idx, frame_scale, model_slice):
    """Compute log-likelihood for one frames against one model in one orientation

    Keyword arguments:
    frame_vals -- values of frame intensity
    frame_idx -- indexes for frame values against model_slice values
    frame_scale -- scale of a frame
    model_slice -- slice of one model in one orientation

    Return:
    loglh -- computed value of log-likelihood
    """
    frame_len = frame_vals.shape[0]
    loglh = 0
    for i in range(frame_len):
        if frame_vals[i] == 0:
            break
        loglh += frame_vals[i]*np.log(model_slice[frame_idx[i]]*frame_scale)

    return loglh


@njit(parallel=True, fastmath=True)
def maximise_data_chunk(data_vals, data_idx, data_scale,
                        q_vals, t_vals, prob_vals,
                        num_class, rotations,
                        next_model, next_model_norm):
    """Add data values to model based on probability values

    Keyword arguments:
    data_vals -- values of data intensity
    data_idx -- indexes for data values against model_slice values
    data_scale -- scale of individual frames in data
    q_vals -- radius values
    t_vals -- angle values
    prob_vals -- probability values
    num_class -- number of classes (number of models)
    rotations -- array with values of angles for rotations
    next_model -- sum of all intensities with prob_vals weights will be written here
    next_model_norm -- sum of all prob_vals weights will be written here
    """
    num_rot = len(rotations)
    for k in prange(num_class):
        new_slice = np.zeros(q_vals.shape)
        new_slice_norm = np.zeros(q_vals.shape)
        for j in range(num_rot):
            rot = rotations[j]
            if np.amax(prob_vals[k, j]) == 0:
                continue

            new_slice[:] = 0
            new_slice_norm[:] = 0

            compute_new_slice(data_vals, data_idx, data_scale,
                              prob_vals[k, j], new_slice, new_slice_norm)

            project_add_to_model(new_slice, q_vals, t_vals + rot, next_model[k])
            project_add_to_model(new_slice_norm, q_vals, t_vals + rot, next_model_norm[k])


@njit(fastmath=True)
def compute_new_slice(data_vals, data_idx, data_scale,
                      prob_vals, new_slice, new_slice_norm):
    """Compute one orientation to add data values to model based on probability values

    Keyword arguments:
    data_vals -- values of data intensity
    data_idx -- indexes for data values against model_slice values
    data_scale -- scale of individual frames in data
    prob_vals -- probability values
    new_slice -- sum of all intensities with prob_vals weights will be written here
    new_slice_norm -- sum of all prob_vals weights will be written here
    """
    n_frames, frame_len = data_vals.shape
    new_slice[:] = 0
    slice_prob = 0
    for k in range(n_frames):
        prob = prob_vals[k]
        if prob > 0:
            for i in range(frame_len):
                if data_vals[k, i] == 0:
                    break
                new_slice[data_idx[k, i]] += data_vals[k, i] * prob
            slice_prob += prob * data_scale[k]

    new_slice_norm[:] = slice_prob


@njit(parallel=True, fastmath=True)
def project_add_to_model(frame_vals, q_vals, t_vals, out_model):
    """Add values to model by polar coordinates

    Keyword arguments:
    frame_vals -- values of data intensity
    q_vals -- radius values
    t_vals -- angle values
    out_model -- result will be added to this array inplace
    """
    assert len(frame_vals) == len(q_vals)
    assert len(q_vals) == len(t_vals)

    center = (out_model.shape[0]-1) // 2

    for i in prange(len(frame_vals)):
        x_val = q_vals[i]*np.cos(t_vals[i]) + center
        y_val = q_vals[i]*np.sin(t_vals[i]) + center

        x_fl = int(np.floor(x_val))
        y_fl = int(np.floor(y_val))

        x_frac = x_val - x_fl
        y_frac = y_val - y_fl

        if test_valid(y_fl, out_model.shape[0]) and test_valid(x_fl, out_model.shape[1]):
            out_model[y_fl, x_fl] += (1 - x_frac)*(1 - y_frac)*frame_vals[i]

        if test_valid(y_fl, out_model.shape[0]) and test_valid(x_fl + 1, out_model.shape[1]):
            out_model[y_fl, x_fl + 1] += (x_frac)*(1 - y_frac)*frame_vals[i]

        if test_valid(y_fl + 1, out_model.shape[0]) and test_valid(x_fl, out_model.shape[1]):
            out_model[y_fl + 1, x_fl] += (1 - x_frac)*(y_frac)*frame_vals[i]

        if test_valid(y_fl + 1, out_model.shape[0]) and test_valid(x_fl + 1, out_model.shape[1]):
            out_model[y_fl + 1, x_fl + 1] += (x_frac)*(y_frac)*frame_vals[i]
