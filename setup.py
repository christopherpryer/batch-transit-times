from batch_transit_times import __version__
from setuptools import setup

long_description = ''
with open('./README.md') as f:
    long_description = f.read()

setup(name='batch_transit_times',
    version=__version__,
    description='Python package that leverages python-fedex to process ground transit times for shipment data.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/christopherpryer/batch-transit-times',
    author='Chris Pryer',
    author_email='christophpryer@gmail.com',
    license='PUBLIC',
    packages=['batch_transit_times'],
    zip_safe=False)
