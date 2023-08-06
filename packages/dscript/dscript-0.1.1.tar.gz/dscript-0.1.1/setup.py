#!/usr/bin/env python

from setuptools import setup, find_packages
from dscript import __version__

def strip_readme_img(fi):
    content = open(fi)
    clean_content = []
    for line in content:
        if '.png' in line:
            continue
        else:
            clean_content.append(line)

    return ''.join(clean_content)

setup(name="dscript",
        version=__version__,
        description="D-SCRIPT: protein-protein interaction prediction",
        long_description=strip_readme_img('README.md'),
        long_description_content_type='text/markdown',
        author="Samuel Sledzieski",
        author_email="samsl@mit.edu",
        url="http://dscript.csail.mit.edu",
        license="GPLv3",
        packages=find_packages(),
        entry_points={
            "console_scripts": [
                "dscript = dscript.__main__:main",
            ],
        },
        include_package_data = True,
        install_requires=[
            "numpy",
            "scipy",
            "pandas",
            "torch",
            "matplotlib",
            "seaborn",
            "tqdm",
            "scikit-learn",
            "h5py",
        ]
    )
