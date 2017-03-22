from distutils.core import setup

setup(
  name='servo-dependency-tool',
  description='Tool for automatically upgrading Cargo dependencies.',
  install_requires=['gitpython','github3.py'],
)
