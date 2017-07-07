from setuptools import setup, find_packages


setup(
    name='fmap',
    version='0.1.0',
    description='lazy map for Iterable and Sequence',
    packages=find_packages(exclude=['test'])
)
