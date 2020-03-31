from setuptools import setup

setup(name='ramscube',
      use_scm_version=True,
      setup_requires=['setuptools_scm'],
      description='Load RAMS output into iris cubes',
      url='http://github.com/mheikenfeld/ramscube',
      author='Max Heikenfeld',
      author_email='maxheikenfeld@web.de',
      license='BSD-3-Clause',
      packages=['ramscube'],
      install_requires=[],
      zip_safe=False)
