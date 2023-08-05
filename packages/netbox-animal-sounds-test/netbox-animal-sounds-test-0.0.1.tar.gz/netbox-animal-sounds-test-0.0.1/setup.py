from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='netbox-animal-sounds-test',
    version='0.0.1',
    description='An example NetBox plugin',
    long_description=long_description,
    url='https://github.com/netbox-community/netbox-animal-sounds',
    author='Jeremy Stretch',
    license='Apache 2.0',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
)
