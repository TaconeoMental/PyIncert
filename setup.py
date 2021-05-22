from os import path
from setuptools import setup

lib_root = path.abspath(path.dirname(__file__))

def read_file(*paths):
    with open(path.join(*paths), encoding="utf-8") as file:
        return file.read()

setup(
    name = 'pyincert',
    packages = ['pyincert'],
    version = read_file(lib_root, "RELEASE"),
    license= 'GNU General Public License v3.0',
    description = 'Pequeña librería para trabajar con propagación de errores',
    long_description = read_file(lib_root, "README.md"),
    long_description_content_type = 'text/markdown',
    author = 'Mateo Contenla',
    author_email = 'mcontenlaf@gmail.com',
    url = 'https://github.com/TaconeoMental/PyIncert',
    keywords = ['error propagation', 'Propagation of uncertainty', 'standard deviation'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
)
