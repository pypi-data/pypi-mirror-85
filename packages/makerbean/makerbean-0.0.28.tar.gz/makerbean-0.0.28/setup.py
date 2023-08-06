# -*- coding: utf-8 -*-
# @Author: Anderson
# @Date:   2019-11-14 17:45:03
# @Last Modified by:   ander
# @Last Modified time: 2020-11-16 19:32:06
import setuptools


setuptools.setup(
    name="makerbean",
    version="0.0.28",
    author="MakerBi",
    author_email="andersonby@163.com",
    description="A small educational purpose package",
    long_description_content_type="text/markdown",
    url="https://makerbean.com",
    packages=setuptools.find_packages(),
    install_requires=['openpyxl', 'requests', 'beautifulsoup4', 'lxml', 'jieba', 'pyecharts', 'pdfplumber', 'PyPDF2', 'python-docx'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
