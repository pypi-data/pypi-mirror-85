from setuptools import setup
setup(name="TOPSIS_Mehak_101983050",
version="1.0.1",
licence="MIT",
description="Assignment06",
long_desription="Calculating Topsis Score can help in understanding best and worst data entries in a dataset.In this package ,we are calculating topsis rank by taking input csv file,weights and impacts from the user.-Weights and impacts must be comma separated -Number of Columns in the dataset should be equal to number of weights and number of impacts passed.",
keywords="Topsis, Vector, normalization, score",
url="https://github.com/Mehak-Munjal/TOPSIS",
author="Mehak",
classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
packages=['TOPSIS_Mehak_101983050'],
install_requires=['pandas'])
