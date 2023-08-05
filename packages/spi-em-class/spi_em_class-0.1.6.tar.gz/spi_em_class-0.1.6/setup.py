from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='spi_em_class',
      version='0.1.6',
      description='Module for EM classification of diffraction images in CXI format.',
      long_description=readme(),
      long_description_content_type="text/markdown",
      url='https://gitlab.com/spi_xfel/spi_em_class',
      author='Sergey Bobkov',
      author_email='s.bobkov@grid.kiae.ru',
      license='MIT',
      python_requires='>=3.6',
      install_requires=['numba',
                        'numpy',
                        'scipy',
                        'matplotlib',
                        'h5py',
                        'tqdm'],
      packages=['spi_em_class'],
      scripts=['scripts/spi_em_create.py',
               'scripts/spi_em_config.py',
               'scripts/spi_em_report.py',
               'scripts/spi_em_reset.py',
               'scripts/spi_em_run.py',
               'scripts/spi_em_save.py',
               'scripts/spi_em_save_by_symmetry.py'],
      include_package_data=True,
      zip_safe=False)
