# Fast Directed Line Segment Grouping Method
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview
This package will provide an algorithm and interface to group elementary line segments in terms of direction and vicinity. The algorithm used is based on the algorithm developed by Jang & Hong (2002)[^JH2002]. The software efficiently finds line segments from a bunch of elemental directed line segments placed in a three-dimensional space.


## Dependencies
The library is written in _C++11_ and do not depends on any library outside of the `STL`. The Python interface is depends on `NumPy`. The library is developed on `g++` version 5.4 installed in Linux Mint 18.1 (serena). The Python interface is developed on Python 3.7.1 and Numpy 1.18.1.


## References
[^JH2002]: Jeong-Hun Jang & Ki-Sang Hong, Pattern Recognition 35 (2002), 2235--2247 (doi: [10.1016/S0031-3203(01)00175-3](https://doi.org/10.1016/S0031-3203(01)00175-3 "Jand & Hong (2002)"))
