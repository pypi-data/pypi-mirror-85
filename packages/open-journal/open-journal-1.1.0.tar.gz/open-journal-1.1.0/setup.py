from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='open-journal',
    version='1.1.0',
    install_requires=[
    	'pyqt5',
    	'cryptography'
    ],
    packages=find_packages(),
    scripts=['openjournal/main.py'],
    url='https://github.com/Optimizer-Prime/open-journal',
    license='GPL-3.0',
    author='Stuart Clayton',
    author_email='stu3cla@pm.me',
    description='A simple, private, open-source journal.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=["Programming Language :: Python :: 3"],
    python_requires='>=3.6',
    entry_points = {
    'gui_scripts': [
        'openjournal=openjournal.main:main']
        }
)
