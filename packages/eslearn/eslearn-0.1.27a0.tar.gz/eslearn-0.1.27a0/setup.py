#-*- coding:utf-8 -*-

"""
Created on 2020/03/03
------
@author: Chao Li; Mengshi Dong
Email:  lichao19870617@gmail.com; dongmengshi1990@163.com
"""

from setuptools import setup, find_packages

with open("README_pypi.md", "r") as fh:
    long_description = fh.read()

setup(
    name='eslearn',
    version='0.1.27.alpha',
    description=(
        'This project is designed for machine learning in resting-state fMRI field'
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Chao Li; Mengshi Dong',
    author_email='lichao19870617@gmail.com',
    maintainer='Chao Li; Mengshi Dong',
    maintainer_email='lichao19870617@gmail.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/easylearn-fmri/',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Natural Language :: English',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],

    install_requires=[
        "imbalanced-learn==0.6.2",
        "joblib==0.14.1",
        "matplotlib==3.2.1",
        "nibabel==3.0.1",
        "numpy==1.18.1",
        "openpyxl==3.0.3",
        "pandas==1.0.1",
        "PyQt5==5.14.2",
        "PyQt5-sip==12.7.2",
        "python-dateutil==2.8.1",
        "scikit-learn==0.22.2",
        "scipy==1.4.1"
    ],

    include_package_data=True,
    python_requires='>=3.5',
)