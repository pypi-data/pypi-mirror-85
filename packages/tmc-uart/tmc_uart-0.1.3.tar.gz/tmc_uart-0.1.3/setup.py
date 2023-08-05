from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='tmc_uart',
      version='0.1.3',
      description=u"Read/Write to Trinamic motion controller TMC5160 via the uart interface",
      long_description=long_description,
      classifiers=[],
      keywords='tmc5160 trinamic',
      author=u"Steve Troxel",
      author_email='troxel@perlworks.com',
      url='',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[ "pySerial" ],
      
      )
