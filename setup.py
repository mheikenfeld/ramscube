from setuptools import setup

setup(name='ramscube',
      version='0.1',
      description='Load RAMS output into iris cubes',
      url='http://github.com/mheikenfeld/wrfcube',
      author='Max Heikenfeld',
      author_email='max.heikenfeld@physics.ox.ac.uk',
      license='GNU',
      packages=['ramscube'],
      install_requires=[],#['iris','numpy','netCDF4'],
      zip_safe=False)
