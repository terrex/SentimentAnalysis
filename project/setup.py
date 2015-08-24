from codecs import open
from os import path

from setuptools import find_packages
from cx_Freeze import setup, Executable
try:
    from setup_morefiles import morefiles
except ImportError:
    morefiles = []

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    zip_includes=morefiles,
)

import sys

base = 'Win32GUI' if sys.platform == 'win32' else None

import pfcsamr

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

executables = [
    Executable('pfcsamr/gui.py', base=base, targetName='Sentiment Analysis',
        packages=['scipy', 'numpy', 'scikit-learn', 'nltk', 'PyYAML'])
]

setup(
    name='pfcsamr',
    version=pfcsamr.__version__,
    description='Sentiment Analysis on Movie Reviews',
    long_description=long_description,
    url='https://bitbucket.org/terrex/pfc-sent-anal-movie-rev',

    # Author details
    author='Guillermo Gutierrez-Herrera',
    author_email='xiterrex@gmail.com',

    # Choose your license
    license='GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 3.4',

        'Topic :: Text Processing :: Linguistic',
    ],

    keywords='sentiment analysis',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'numpy',
        'scipy',
        'scikit-learn',
        'nltk>=3.0.0',
        'PyYAML',
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [],
        'test': ['nose'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        '': ['*.txt', '*.rst', 'logging.conf'],
        'pfcsamr': ['*.qml', 'License.txt', 'logging.conf'],
        'pfcsamr.data': ['*.*'],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'gui_scripts': [
            'pfcsamr-gui = pfcsamr.gui:main',
        ],
    },

    # cx_Freeze
    options=dict(build_exe=buildOptions, bdist_mac={
        'bundle_name': 'Sentiment Analysis',
        # 'include_frameworks': [
        #     '/Library/Frameworks/Python.framework',
        # ] + list(glob.glob('/Users/terrex/Qt5.5.0/5.5/clang_64/lib/*.framework')),
    }),
    executables=executables,
)
