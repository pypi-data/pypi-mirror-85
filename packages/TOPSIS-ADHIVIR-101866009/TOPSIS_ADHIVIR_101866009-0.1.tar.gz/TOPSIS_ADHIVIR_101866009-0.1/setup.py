from setuptools import setup, find_packages
from os import path

URL = 'https://github.com/avsr13/TOPSIS_ADHIVIR_101866009'

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='TOPSIS_ADHIVIR_101866009',
    version='0.1',
    license='MIT',
    author='ADHIVIR SINGH RANA',
    packages=['TOPSIS_ADHIVIR_101866009'],
    author_email='arana60_be18@thapar.edu',
    description='TOPSIS implementation',
    keywords=['TOSPSIS', 'Normalised_Matrix', 'Performance_score', 'Rank', 'Weighted_Normalised_matrix','TOPSIS SCORE'],
    install_requires=[
        'pandas',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],

)
