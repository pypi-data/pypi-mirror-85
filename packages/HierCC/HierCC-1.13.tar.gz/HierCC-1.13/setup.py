import os, sys
from setuptools import setup, find_packages
#from PEPPA import __VERSION__
__VERSION__ = '1.13'

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='HierCC',
    version= __VERSION__,
    #scripts=['PEPPA.py'] ,
    author="Zhemin Zhou",
    author_email="zhemin.zhou@warwick.ac.uk",
    description="Hierarchical Clustering of cgMLST profiles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zheminzhou/HierCC",
    packages = ['HierCC'],
    package_dir = {'HierCC':'.'},
    keywords=['bioinformatics', 'microbial', 'genomics', 'MLST', 'hierarhical clustering'],
    install_requires=['matplotlib>=3.2.1', 'scikit-learn>=0.23.1', 'numba>=0.38.0', 'numpy>=1.18.1', 'pandas>=0.24.2', 'scipy>=1.3.2'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'HierCC = HierCC.HierCC:hierCC',
            'HCCeval = HierCC.HCCeval:evalHCC',
    ]},
    package_data={'HierCC': ['LICENSE', 'README.*']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Programming Language :: Python :: 3.8",
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        "Operating System :: OS Independent",
    ],
 )

