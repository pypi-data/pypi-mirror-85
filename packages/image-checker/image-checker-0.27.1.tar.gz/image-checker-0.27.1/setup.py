# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os.path

readme = ''
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, 'README.rst')
if os.path.exists(readme_path):
    with open(readme_path, 'rb') as stream:
        readme = stream.read().decode('utf8')

setup(
    long_description=readme,
    name='image-checker',
    version='0.27.1',
    description='Check for corrupted images using Nvidia DALI',
    python_requires='==3.*,>=3.5.0',
    project_urls={"repository": "https://github.com/cceyda/image-checker"},
    author='Ceyda Cinarel',
    author_email='snu-ceyda@users.noreply.github.com',
    license='MIT',
    keywords='image checker image integrity checker',
    entry_points={
        "console_scripts": ["image-checker = image_checker.cli:main"]
    },
    packages=['image_checker'],
    package_dir={"": "."},
    package_data={"image_checker": ["*.json"]},
    install_requires=['more-itertools==8.*,>=8.6.0', 'tqdm==4.*,>=4.51.0'],
)
