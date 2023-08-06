import setuptools
import sys
import os

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

PATH_ROOT = PATH_ROOT = os.path.dirname(__file__)
builtins.__SIMPLE_REC_SETUP__ = True

import simple_rec

def load_description(path_dir=PATH_ROOT, filename='DOCS.md'):
    """Load long description from readme in the path_dir/ directory

    """
    with open(os.path.join(path_dir, filename)) as f:
        long_description = f.read()
    return long_description


def load_requirements(filename='requirements.txt', comment_char='#'):
    """From pytorch-lightning repo: https://github.com/PyTorchLightning/pytorch-lightning.
       Load requirements from text file in the path_dir/requirements/ directory.

    """
    with open(filename, 'r') as file:
        lines = [ln.strip() for ln in file.readlines()]
    reqs = []
    for ln in lines:
        # filer all comments
        if comment_char in ln:
            ln = ln[:ln.index(comment_char)].strip()
        # skip directly installed dependencies
        if ln.startswith('http'):
            continue
        if ln:  # if requirement is not empty
            reqs.append(ln)
    return reqs


if __name__ == '__main__':
    
    name = 'simple_rec'
    version = simple_rec.__version__
    description = simple_rec.__doc__

    author = 'Philipp Wirth'
    author_email = 'philipp.m.wirth@gmail.com'
    description = "A light-weight collection of simple recommender systems."

    long_description = load_description()

    python_requires = '>=3.6'
    install_requires = load_requirements()

    packages = [
        'simple_rec'
    ]

    project_urls = {}

    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License"
    ]

    setuptools.setup(
        name=name,
        version=version,
        author=author,
        author_email=author_email,
        description=description,
        license='MIT',
        long_description=long_description,
        long_description_content_type='text/markdown',
        install_requires=install_requires,
        python_requires=python_requires,
        packages=packages,
        classifiers=classifiers,
        include_package_data=True,
        project_urls=project_urls,
    )


