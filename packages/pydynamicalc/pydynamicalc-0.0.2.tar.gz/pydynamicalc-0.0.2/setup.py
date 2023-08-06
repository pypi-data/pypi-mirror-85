from setuptools import setup, find_packages

setup(name='pydynamicalc',
      version='0.0.2',
      description='Pythonic photodynamical model generator, using three different configurations (quasi-circular, eccentric and osculating), in addition - an MCMC-coupled version is also provided, which allows optimization of planetary masses and eccentricities',
      author='Gideon Yoffe',
      author_email='yoffe@mpia.de',
      url='https://github.com/AstroGidi/PyDynamicaLC',
      packages = find_packages(where = 'src'),
      install_requires = ['ttvfaster', 'matplotlib', 'numpy', 'scipy', 'pyastronomy', 'pymultinest', 'corner', 'wheel'],
      license = 'Weizmann Institute of Science',
      package_dir={'': 'src'}
     )
