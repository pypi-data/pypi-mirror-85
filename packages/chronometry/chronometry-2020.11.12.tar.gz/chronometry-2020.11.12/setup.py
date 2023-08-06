from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='chronometry',
	version='2020.11.12',
	description='Python library for tracking time and displaying progress bars',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/idin/chronometry',
	author='Idin',
	author_email='py@idin.ca',
	license='MIT',
	packages=find_packages(exclude=("jupyter_tests", ".idea", ".git")),
	install_requires=[
		'pandas', 'numpy', 'slytherin', 'colouration', 'sklearn', 'ravenclaw', 'func-timeout', 'matplotlib'
	],
	python_requires='~=3.6',
	zip_safe=False
)