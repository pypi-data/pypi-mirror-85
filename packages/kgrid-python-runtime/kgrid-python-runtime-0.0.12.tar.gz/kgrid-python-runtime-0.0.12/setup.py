import os
import setuptools

this_dir = os.path.dirname(os.path.realpath(__file__))
requirements = this_dir + '/requirements.txt'

with open("README.md", "r") as fh:
    long_description = fh.read()

reqs = []
if os.path.isfile(requirements):
    with open(requirements) as file:
        reqs = file.read().splitlines()

setuptools.setup(
    name="kgrid-python-runtime",
    version="0.0.12",
    author="Kgrid Developers",
    author_email="kgrid-developers@umich.edu",
    description="A runtime for python-based Knowledge Objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kgrid/kgrid-python-runtime",
    packages=[
        'kgrid_python_runtime'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Framework :: Flask",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Medical Science Apps."
    ],
    python_requires='>=3.8',
    install_requires=reqs

)
