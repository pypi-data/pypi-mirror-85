from setuptools import setup, find_packages

setup(name='py2dash',
      version='0.0.2',
      description='Tools to produce dash (plot.ly) interfaces from existing python functionality',
      url='https://github.com/i2mint/py2dash',
      author='Thor Whalen',
      license='Apache',
      platforms='any',
      install_requires=['flask', 'dash', 'argh'],
      packages=find_packages())
