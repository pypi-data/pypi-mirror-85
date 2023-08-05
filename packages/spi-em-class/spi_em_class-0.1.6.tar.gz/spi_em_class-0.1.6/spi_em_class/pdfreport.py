"""
Code for PDF reports
Author: Sergey Bobkov
"""

import datetime
from typing import Optional
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable

from . import em_data, log_writer

mpl.rcParams['image.cmap'] = 'viridis'
mpl.rcParams['image.interpolation'] = 'nearest'

PDF_REPORT_NAME = 'em_class_report.pdf'

class ReportWriter():
    """Produce PDF reports with matplotlib figures"""
    def __init__(self, filename: str):
        self._create_file(filename)

    def _create_file(self, filename: str):
        self.pdf_pages = PdfPages(filename)
        pdf_dict = self.pdf_pages.infodict()
        pdf_dict['CreationDate'] = datetime.datetime.today()
        pdf_dict['ModDate'] = datetime.datetime.today()


    def save_figure(self, figure: plt.Figure):
        """Add a page to PDF with matplotlib figure

        Keyword arguments:
        figure -- figure to be saved
        """

        self.pdf_pages.savefig(figure)
        plt.close(figure)


    def close(self):
        """Closes PDF document"""
        self.pdf_pages.close()


def plot_image(image: np.ndarray, axis: plt.Axes, logscale: bool = True,
               colorbar: bool = True, vmin: Optional[float] = None, vmax: Optional[float] = None,
               **kwargs):
    """Plot image to axis with optional logscale and colorbar

    Keyword arguments:
    image -- 2D array with data to show
    axis -- matplotlib axis to plot
    logscale -- use logscale
    colorbar -- add colorbar to image
    vmin -- minimal value of colormap
    vmax -- miximum value of colormap
    kwargs -- arguments for imshow
    """
    if vmin is None and logscale:
        vmin = max(1, np.amin(image))
    elif vmin is None:
        vmin = np.amin(image)

    if vmax is None:
        vmax = np.amax(image)

    if logscale:
        norm = colors.LogNorm(vmin=vmin, vmax=vmax)
    else:
        norm = colors.Normalize(vmin=vmin, vmax=vmax)

    im_handle = axis.imshow(image, norm=norm, **kwargs)
    axis.set_xticks([])
    axis.set_yticks([])

    if colorbar:
        divider = make_axes_locatable(axis)
        cb_axis = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(im_handle, cax=cb_axis)


def em_summary_fig(rotations, class_numbers, mutual_info):
    """Create figure with results summary

    Keyword arguments:
    rotations -- 2D array with rotation distribution over iterations
    class_numbers -- 2D array with class distribution over iterations
    mutual_info -- array with mutual info history
    """
    fig, axes = plt.subplots(1, 3, figsize=(12, 6))
    rot_axis, class_axis, info_axis = axes.flatten()

    sorted_rots = rotations[:, rotations[-1].argsort()]
    rot_axis.imshow(sorted_rots.T)
    rot_axis.set_yticks([])
    rot_axis.set_aspect('auto', 'box')
    rot_axis.set_xlabel('Iteration')
    rot_axis.set_ylabel('Pattern number')
    rot_axis.set_title('Most likely orientations of data')

    sorted_class = class_numbers[:, class_numbers[-1].argsort()]
    class_axis.imshow(sorted_class.T)
    class_axis.set_yticks([])
    class_axis.set_aspect('auto', 'box')
    class_axis.set_xlabel('Iteration')
    class_axis.set_ylabel('Pattern number')
    class_axis.set_title('Most likely classes of data')

    info_axis.plot(np.arange(1, mutual_info.size), mutual_info[1:])
    info_axis.set_aspect('auto', 'box')
    info_axis.set_xlabel('Iteration')
    info_axis.set_ylabel('I(K,W)')

    fig.tight_layout()
    return fig


def em_progress_fig(iter_num, model_data, class_numbers, rotations):
    """Create figure with iteration results

    Keyword arguments:
    iter_num -- index of iteration for title
    model_data -- 3D array with model images
    class_numbers -- array with class distribution
    rotations -- array with rotation distribution
    """
    n_classes = model_data.shape[0]
    n_rot = rotations.max()
    class_ids = np.arange(n_classes) + 1
    class_counts = [np.sum(class_numbers == i) for i in class_ids]

    plot_x = int(np.ceil(np.sqrt(n_classes)))
    plot_y = int(np.ceil(n_classes / plot_x))
    rot_bins = np.arange(n_rot)

    fig, axes = plt.subplots(plot_y, plot_x, figsize=(plot_x*3, plot_y*3))
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.90, top=0.85, wspace=0.2, hspace=0.2)
    fig.suptitle('Iteration {}'.format(iter_num), fontsize=20)

    for i in range(plot_x*plot_y):
        axis = axes.flatten()[i]
        if i >= n_classes:
            axis.set_axis_off()
        else:
            class_model = model_data[i]
            class_rotations = rotations[class_numbers == i + 1]
            vmin = class_model.mean() * 0.01
            if vmin > 0:
                plot_image(class_model, axis, vmin=vmin)
            else:
                plot_image(class_model, axis, logscale=False)

            if (class_rotations.size == 0) or (np.std(class_rotations) == 0):
                continue

            ax2 = axis.twinx()
            hist, _ = np.histogram(class_rotations, bins=rot_bins)
            # rot_unev = np.round(hist.max()/hist.mean(), 2)
            x_values = rot_bins[:-1] * (0.95 * class_model.shape[0] / rot_bins[-1])
            ax2.bar(x_values, hist, color='r', width=1, alpha=0.5)
            ax2.set_axis_off()
            ax2.set_ylim([0, hist.max()*2])
            axis.set_frame_on(False)

            axis.set_title('№{}, {} frames'.format(class_ids[i], class_counts[i]))

    return fig


def create_pdf_report(data_file, pdf_file):
    """Create figure with iteration results

    Keyword arguments:
    data_file -- file with EM class data
    pdf_file -- output pdf file
    """
    rotations = []
    classes = []
    mutual_info = []

    num_completed = em_data.get_num_saved_iterations(data_file)
    if num_completed == 0:
        log_writer.show_message('No iterations data in file: {}'.format(data_file))
        return

    for i in range(1, num_completed + 1):
        it_data = em_data.load_iteration_data(data_file, i, for_report=True)
        rotations.append(it_data['rotations'][:])
        classes.append(it_data['classes'][:])
        mutual_info.append(it_data['mutual_info'][()])

    rotations = np.stack(rotations)
    classes = np.stack(classes)
    mutual_info = np.stack(mutual_info)

    report = ReportWriter(pdf_file)
    report.save_figure(em_summary_fig(rotations, classes, mutual_info))

    it_data = em_data.load_iteration_data(data_file, num_completed)
    report.save_figure(em_progress_fig(num_completed, it_data['model'],
                                       it_data['classes'], it_data['rotations']))
    report.close()
