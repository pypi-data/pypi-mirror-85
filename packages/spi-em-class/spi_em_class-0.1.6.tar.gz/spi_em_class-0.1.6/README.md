# Installation

Processing scripts require **Python 3.6** or higher.

You can install stable version by:
```
pip install spi_em_class
```

To install from git, clone the repository and run commands:
```
cd spi_em_class
pip install .
```

# EM classification

To classify diffraction images via Expectation-Maximization algorithm please perform the following steps:

## Create new EM classification

Create blank data file for a new EM classification. A data file is HDF5 archive.
It includes EM configuration, temporary data and EM results.
You must provide path for CXI file with input images.
```
spi_em_create.py [-h] [-d DATA] FILE
```

Options:
* `FILE` - CXI file with input images.
* `-d DATA` - path to a new data file. Default: "em_class_data.h5".

## Configure EM classification

You can change configuration of EM classification. There are two possible ways:
1. Edit configuration as text file.
2. Provide parameters in command line.

If you change parameters for EM classification with finished iterations, you may need to reset classification.

```
spi_em_config.py [-h] [-d DATA] [--cxi FILE] [--q_min Q_MIN]
                 [--q_max Q_MAX] [--num_rot NUM_ROT]
                 [--num_class NUM_CLASS] [--friedel] [--no-friedel]
                 [--logscale] [--no-logscale] [--best] [--no-best]
                 [--binning BINNING] [-s] [-e]
```
Options:
* `-d DATA` - path to the data file. Default: "em_class_data.h5".
* `-e` - open configuration editor. This is default behavior when `spi_em_config.py` is run without arguments. You can set your preferred editor via `EDITOR` environment value.
* `-s` - print current configuration and exit.

|Parameter  | CMD option        | Description                           |
|---        |---                |---                                    |
|cxi_file   |--cxi FILE         | Path to CXI file with input images    |
|q_min      |--q_min Q_MIN      | Minimum q-radius used in classification (pixels)  |
|q_max      |--q_max Q_MAX      | Maximum q-radius used in classification (pixels)  |
|num_rot    |--num_rot NUM_ROT  | Number of considered rotation angles  |
|num_class  |--num_class NUM_CLASS      | Number of EM classes          |
|friedel    |--friedel OR --no-friedel  | Force central symmetry (Friedel's law)    |
|logscale   |--logscale OR --no-logscale| Apply log-scaling to input images         |
|best_proba |--best OR --no-best| Consider only one orientation with best probability for each frame|
|binning    |--binning BIN      | Bin input frames (Combine pixels in BIN*BIN groups together)|

## Run EM classification

To start EM classification please run:

```
spi_em_run.py [-h] [-d DATA] iter
```

If there are finished EM iterations, EM process will continue from last iteration.

Options:
* `-d DATA` - path to the data file. Default: "em_class_data.h5".
* `iter` - number of EM iterations to perform.

## Reset EM classification

You may need to reset finished EM iterations and delete temporary data. Please run:

```
spi_em_reset.py [-h] [-d DATA]
```

Options:
* `-d DATA` - path to the data file. Default: "em_class_data.h5".

## Create EM classification report

To check EM results, you can create PDF report. Please run:

```
spi_em_report.py [-h] [-o OUT] [-d DATA]
```

Options:
* `-d DATA` - path to the data file. Default: "em_class_data.h5".
* `-o OUT` - path to a new PDF file. Default: "em_class_report.pdf".

## Save EM classification (manually)

You can save result of last EM iteration into CXI file as a 1D dataset along with input images. By default, results are added to the input CXI file.

```
spi_em_save.py [-h] [-o OUT] [-c CLASS_DSET] [-s SELECT_DSET] [-d DATA]
               select_class [select_class ...]
```

Options:
* `-d DATA` - path to the data file. Default: "em_class_data.h5".
* `-o OUT` - path to a output CXI file. It is a copy of input CXI file with classification data.
* `select_class` - Numbers for selected classes. Result dataset will contain 1 for images in selected classes and 0 for other images.
* `-s SELECT_DSET` - name of a selection dataset within image_n groups in CXI file. Default: "em_class/select".
* `-c CLASS_DSET` - name of a class distribution dataset within image_n groups in CXI file. This dataset will contain class number for every image. Default: "em_class/classes".

## Save EM classification by symmetry of class models.

You can select EM classes automatically by analisys of model symmetry. First, symmetry scores are computed for first 50 symmetry orders by Discrete Cosine Transform of model autocorrelation in polar coordinates. Second, symmetry value is a ratio between symmetry score for selected symmetry order and sum of all symmetry scores. Symmetry value lies in [0,1]. Finally, if symmetry value > threshold, class is selected for saving.

```
spi_em_save_by_symmetry.py [-h] [-t THRESHOLD] [-o OUT] [-c CLASS_DSET]
                                [-s SELECT_DSET] [-d DATA] order
```

Options:
* `-d DATA` - path to the data file. Default: "em_class_data.h5".
* `-o OUT` - path to a output CXI file. It is a copy of input CXI file with classification data.
* `order` - Symmetry order that is used for selection.
* `-t THRESHOLD` - threshold for symmetry values. Default: 0.5.
* `-s SELECT_DSET` - name of a selection dataset within image_n groups in CXI file. Default: "em_class/select".
* `-c CLASS_DSET` - name of a class distribution dataset within image_n groups in CXI file. This dataset will contain class number for every image. Default: "em_class/classes".
