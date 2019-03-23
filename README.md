# ramscube
[![DOI](https://zenodo.org/badge/109262170.svg)](https://zenodo.org/badge/latestdoi/109262170)[![Documentation Status](https://readthedocs.org/projects/wrfcube/badge/?version=latest)](https://wrfcube.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/mheikenfeld/ramscube.svg?branch=master)](https://travis-ci.org/mheikenfeld/ramscube)

ramscube is a python package to allow for a convenient loading of RAMS model output into iris cubes which includes a lot of functionality to compute important variables like that have to be constructed from the output in the RAMS output hdf files. Additionally the package contains many functions to caclulate other quantities such as liquid and ice water path, total surface precipitation and many more.

Installation
------------

Required packages: iris xarray numpy cf_units

If you are using anaconda, the following command should make sure all dependencies are met and up to date:
```
conda install -c conda-forge iris xarray cf_units
```
You can directly install the package directly from github with pip and either of the two following commands:
```
pip install --upgrade git+ssh://git@github.com/mheikenfeld/ramscube.git
pip install --upgrade git+https://github.com/mheikenfeld/ramscube.git
```

You can also clone the package with any of the two following commands
```
git clone git@github.com:mheikenfeld/ramscube.git 
git clone https://github.com/mheikenfeld/ramscube.git
```

and install the package from the locally cloned version:
```
pip install --upgrade ramscube/
```
(the trailing "/" actually matters here..)
