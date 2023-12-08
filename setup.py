__version__ = '0.0.0'

from setuptools import setup, find_packages


setup(
    name="piball",
    version=__version__,
    install_requires=['sqlalchemy', 'gpiozero', 'click', 'click-log'],
    author='Bill Normandin',
    author_email='bill@pokeybill.us',
    url='https://github.com/wnormandin/piball',
    packages=find_packages(),
    license='MIT',
    description='A python webcrawler',
    keywords='spider crawler website indexing load-testing',
    python_requires='~=3.9'
)
