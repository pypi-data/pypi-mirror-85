from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="topsis_yotest",
    version="0.0.6",
    description="A Python package implementing TOPSIS technique.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Yash Shukla",
    author_email="yash981815@gmail.comm",
    url='https://pypi.org/project/topsis-yotest/0.0.1/',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: 3.7",
    ],
    packages=["topsis_yotest"],
    include_package_data=True,
    install_requires=['scipy',
                      'tabulate',
                      'numpy',
                      'pandas',
                      ],
    entry_points={"console_scripts":["topsis=topsis_yotest.topsis:main"]}
)