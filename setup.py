"""A setuptools setup module for MEGUA package.

See:

https://packaging.python.org/en/latest/distributing.html
https://setuptools.readthedocs.io/en/latest/
https://github.com/pypa/sampleproject

SMC and python packages:

https://github.com/sagemathinc/smc/wiki/FAQ#-question-how-can-i-install-python-packages-from-httpspypipythonorgpypi--using-pip

https://github.com/sagemathinc/smc/wiki/FAQ#pip


"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

setup_filepath = path.abspath(path.dirname(__file__))

import sys
sys.executable = "/usr/bin/env sage"
 
 

# Get the long description from the README file
with open(path.join(setup_filepath, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='megua',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    #version='1.2.0',
    use_scm_version=True,
    setup_requires=['setuptools_scm'], #puts setuptools_scm-1.11.0-py2.7.egg in megua root.

    description='MEGUA project for SageMath',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/jpedroan/megua',

    # Author details
    author='Pedro Cruz',
    author_email='pedrocruz@ua.pt',

    # Choose your license
    license='GPLv3', #same as sagemath


    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? 
        'Development Status :: 2 - Pre-Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Education',
        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Text Processing',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        #Reason: http://doc.sagemath.org/html/en/reference/history_and_license/index.html

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',

        'Natural Language :: English',
        'Natural Language :: Portuguese',

        'Operating System :: POSIX :: Linux',

    ],

    # What does your project relate to?
    keywords='megua parameterized exercises development',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
##### correta:    install_requires=['jinja2', 'pil-compat', 'python-aalib'],
    install_requires=['jinja2'],
    ## VER 'PIL.Image'


    #TODO: what is this??
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    #extras_require={
    #    'dev': ['check-manifest'],
    #    'test': ['coverage'],
    #},

    include_package_data = True,    # include everything in source control

#    package_data = {
#        'megua':  ['megua/template/pt_pt/*']
#    },

#    data_files = [ ('template/pt_pt', ['megua/template/pt_pt/*']) ],


    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'megua = megua.scripts.main:main',  #megua is a package; scripts is a subpackage; main.py is a module; :main is a function inside main.py
        ],
    },
)


