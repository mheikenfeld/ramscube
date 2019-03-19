Installation
==================

Required packages: iris numpy cf_units

If you are using anaconda, the following command should make sure all dependencies are met and up to date:

$ conda install -c conda-forge iris xarray cf_units

You can directly install the package directly from github with pip and either of the two following commands:

$ pip install --upgrade git+ssh://git@github.com/mheikenfeld/ramscube.git
$ pip install --upgrade git+https://github.com/mheikenfeld/ramscube.git


You can also clone the package with any of the two following commands

$ git clone git@github.com:mheikenfeld/ramscube.git 
$ git clone https://github.com/mheikenfeld/ramscube.git

and install the package from the locally cloned version:

$pip install --upgrade ramscube/

(the trailing "/" actually matters here..)
