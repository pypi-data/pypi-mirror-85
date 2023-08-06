# A Minimal k-Nearest Neighbor Graph Construction Library
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview
This package will provide a function to construct an approximated k-Nearest Neighbor graph from a list of three dimensional points. The graph construction algorithm is based on _NN-descent_ presented in Dong, Moses, & Li (2011)[^DML2011]. The Euclidean and Manhattan metrics are implemented in the current version, while only the Euclidean one is available in Python. The algorithm efficiently constructs an approximated k-Nearest Neighbor graph. This provides a portable _C++11_ header and a Python interface.


## Dependencies
The library is written in _C++11_ and do not depends on any library outside of the `STL`. The Python interface is depends on `NumPy`, and functional test procedures depend on `Matplotlib`. The library is developed on `g++` version 5.4 installed in Linux Mint 18.1 (serena). The Python interface is developed on Python 3.7.1 and Numpy 1.18.1.


## References
[^DML2011]: Wei Dong, Charikar Moses, & Kai Li, WWW'11: Proceedings of the 20th international conference on World wide web (2011), 577--586 (doi: [10.1145/1963405.1963487](https://doi.org/10.1145/1963405.1963487 "Dong, Moses, & Li (2011)"))
