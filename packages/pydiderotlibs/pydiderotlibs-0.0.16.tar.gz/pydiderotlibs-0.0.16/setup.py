# -*- coding: utf-8 -*-

import os.path
from setuptools import setup, find_packages

# import pydiderotlib


SETUPDIR = os.path.dirname(__file__)

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

requirements = []
for line in open(os.path.join(SETUPDIR, 'requirements.txt'), encoding="UTF-8"):
    if line.strip() and not line.startswith('#'):
        requirements.append(line)

setup(
    name='pydiderotlibs',
    version='0.0.16',
    packages=find_packages(),
    packages_dir={'' : 'pydiderotlibs'},
    author='Professeurs de Mathématiques du lycée Denis Diderot (Marseille)',
    description="Librairies utilisées dans l'enseignement de l'informatique",
    url='https://github.com/cspaier/pydiderotlibs',
    license='MIT',
    keywords=["python", "teaching"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Topic :: Education",
    ],
    install_requires=requirements,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    # Active la prise en compte du fichier MANIFEST.in
    include_package_data=True,
    python_requires='>=3.0',
    )
