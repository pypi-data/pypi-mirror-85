from setuptools import setup, find_packages
from package import __version__


long_description = ''
with open('./README.md') as f:
    long_description = f.read()

install_requires = []
with open('./requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(name='tmdt',
    version=__version__,
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    author='',
    author_email='',
    license='PUBLIC',
    packages=find_packages(),
    install_requires=install_requires,
    zip_safe=False)