from setuptools import setup,find_packages

setup(name="gcom",
      description="Libreria Geometría Computacional",
      packages= find_packages(where='src'),
      package_dir={'': 'src'},
      )