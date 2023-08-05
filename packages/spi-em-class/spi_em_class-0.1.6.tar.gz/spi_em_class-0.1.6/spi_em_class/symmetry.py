"""
Processing of image data
Author: Sergey Bobkov
"""

import numpy as np
import scipy as sp
from scipy.fftpack import dct
from scipy.ndimage import map_coordinates
from scipy.optimize import differential_evolution
from scipy.signal import argrelextrema


def sphere_form_factor(x_val, sphere_r, scale):
    """Calculate sphere form factor

    Keyword arguments:
    x -- spatial frequency
    r -- sphere radius
    scale -- intensity multiplier

    Return:
    res -- sphere form factor value
    """

    q_by_r = x_val*2*np.pi*sphere_r
    vol = (4/3)*np.pi*(sphere_r**3)
    with np.errstate(divide='ignore', invalid='ignore'):
        res = (scale/vol)*((3*vol*(np.sin(q_by_r) - q_by_r*np.cos(q_by_r))/q_by_r**3)**2)
    return np.nan_to_num(res)


def sphere_size(first_min: int, freq_step: float):
    """Compute size of a sphere by position of first min in sphere form factor

    Keyword arguments:
    first_min_pix -- position of first minimum of form factor (pix)
    freq_step -- Spatial frequency for angle of one detector pixel (1/Angstrom)

    Return:
    size -- sphere size (pixel_size/(wavelength*distance)) (Angstrom)
    """

    return 4.5 / (np.pi*first_min*freq_step)


def get_psd_minima(psd_data):
    """Retrieve index of minima in PSD data by fitting of spherical form-factor

    Keyword arguments:
    psd_data -- array of PSD values, starting from 0 angle. 0 values treated as masked data.

    Return:
    min_values -- indexes of minima in psd_data
    """
    size_min = sphere_size(psd_data.shape[0], 1)
    size_max = sphere_size(6, 1)
    bounds = [(size_min, size_max)]
    x_coord = np.arange(len(psd_data))[psd_data > 0]
    data_to_fit = psd_data[psd_data > 0]

    def r_qual(x):
        fit = sphere_form_factor(x_coord, x, 1)
        fit *= data_to_fit.mean()/fit.mean()
        return np.abs(data_to_fit - fit).sum()

    result = differential_evolution(r_qual, bounds)
    sphere_r = result.x[0]
    data_sphere = sphere_form_factor(x_coord, sphere_r, 1)

    return x_coord[argrelextrema(data_sphere, np.less)[0]]


def get_symmetry_scores(image_data, center=None, num_components=50):
    """Compute vestor of symmetry scores by autocorrelation and fourier decomposition

    Keyword arguments:
    image_data -- 2D image array
    center -- tuple of center coordinates [default: center of image]
    num_components -- number of symmetry components in output

    Retuns:
    symmetry_scores -- 1D array of symmetry scores
    """

    if center is None:
        center = [(x-1)/2 for x in image_data.shape]

    edge_distance = min(image_data.shape[0] - center[0], center[0], \
                        image_data.shape[1] - center[1], center[1])

    polar_data = polar_projection(image_data, center, r_max=edge_distance, cval=0)
    polar_mask = polar_projection(image_data > 0, center, r_max=edge_distance, cval=1)

    psd_data = polar_data.sum(axis=1)
    psd_norm = polar_mask.sum(axis=1)
    psd_data[psd_norm > 0] /= psd_norm[psd_norm > 0]

    min_vals = list(get_psd_minima(psd_data))
    for val in [0, len(psd_data)]:
        if val not in min_vals:
            min_vals.append(val)
    fringe_edges = sorted(min_vals)
    fringe_ranges = list(zip(fringe_edges[:-1], fringe_edges[1:]))

    scores = np.zeros((len(fringe_ranges), num_components))

    for i, val in enumerate(fringe_ranges):
        start, end = val
        selected_data = polar_data[start:end]
        selected_data = selected_data[selected_data.min(axis=1) > 0]

        corr_data = np.zeros((selected_data.shape[0], selected_data.shape[1]+1))
        for j, polar_line in enumerate(selected_data):
            corr_data[j, :] = sp.correlate(polar_line, np.concatenate((polar_line, polar_line)))

        corr_t = np.mean(corr_data, axis=0)
        if corr_t[0] > 0:
            fringe_scores = dct(corr_t, type=1)[::2]
            scores[i] = fringe_scores[:num_components]
        else:
            scores[i] = 0

    return scores


def polar_projection(data, center, r_max=None, cval=None):
    """Compute polar projection

    Keyword arguments:
    data -- 2D image
    center -- tuple of center coordinates
    r_max -- maximum radius value in polar coordinates
    cval -- default value to fill missed areas

    Return:
    polar_data -- 2d image in polar coordinates with shape = (r_max, int(2*np.pi*r_max))
    """

    if r_max is None:
        x_max = max(data.shape[1] - center[1], center[1])
        y_max = max(data.shape[0] - center[0], center[0])
        r_max = np.sqrt(x_max**2 + y_max**2)

    r_max = int(r_max)

    r_i = np.arange(r_max)

    t_max = np.pi
    t_min = -np.pi
    t_num = int(2*np.pi*r_max)
    t_i = np.linspace(t_min, t_max, t_num, endpoint=False)

    t_grid, r_grid = np.meshgrid(t_i, r_i)

    x_grid = r_grid * np.cos(t_grid)
    y_grid = r_grid * np.sin(t_grid)

    x_grid, y_grid = x_grid.flatten(), y_grid.flatten()
    coords = np.vstack((y_grid + center[0], x_grid + center[1]))
    mapped_data = map_coordinates(data, coords, order=0, cval=cval)

    return mapped_data.reshape((r_max, t_num))
