try:
    from setuptools import setup
except BaseException:
    print('Setuptools not found - falling back to distutils')
    from distutils.core import setup

import re

VERSIONFILE = "skeletor/__init__.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    requirements = [l for l in requirements if not l.startswith('#')]

setup(
    name='skeletor',
    version=verstr,
    packages=['skeletor', ],
    license='GNU GPL V3',
    description='Python 3 implementation of Skeleton Extraction by Mesh contraction algorithm',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/schlegelp/skeletor',
    author='Philipp Schlegel',
    author_email='pms70@cam.ac.uk',
    keywords='mesh skeletonization mesh contraction skeleton extraction',
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',

        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=requirements,
    python_requires='>=3.6',
    package_data={'skeletor': ['templates/*template*']},
    zip_safe=False
)
