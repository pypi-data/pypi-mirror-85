# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages  # type: ignore
from easeml import __version__

with open("README.md", "r") as fh:
    README = fh.read()

# The main source of truth for install requirements of this project is the requirements.txt file.
with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.readlines()

setup(
    name='easeml',
    version=__version__+".dev.3",
    description='Client library used to communicate with the ease.ml service.',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Bojan Karlas, Leonel Aguilar',
    author_email='bojan.karlas@gmail.com, leonel.aguilar.m@gmail.com',
    url='https://github.com/DS3Lab/easeml',
    license='MIT',
    install_requires=REQUIREMENTS,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    entry_points={"console_scripts": ["easeml=easeml.commands.client:main"],
                  "easeml": ["download = easeml.commands.download:download_action_group", "show = easeml.commands.show:show_action_group", "create = easeml.commands.create:create_action_group", "init = easeml.commands.batch:easeml_init"],
                  "easeml.download": ["dataset = easeml.commands.download:download_dataset", "model = easeml.commands.download:download_model"],
                  "easeml.show": ["dataset = easeml.commands.show:show_dataset", "job = easeml.commands.show:show_job", "task = easeml.commands.show:show_task"],
                  "easeml.create": ["dataset = easeml.commands.create:create_dataset", "job = easeml.commands.create:create_new_job","module = easeml.commands.create:create_module"],
                  },
)