# nhdpy

[![PyPiVersion](https://img.shields.io/pypi/v/nhdpy.svg)](https://pypi.python.org/pypi/nhdpy/) [![PYPI Downloads](https://img.shields.io/pypi/dm/nhdpy.svg)](https://pypistats.org/packages/nhdpy) [![Build status](https://github.com/jsta/nhdpy/workflows/Python%20package/badge.svg)](https://github.com/jsta/nhdpy/actions)


A python port of the [nhdR](https://jsta.github.io/nhdR) package for querying, downloading, and networking the [National
Hydrography Dataset (NHD)](https://nhd.usgs.gov/) dataset.

## Installation

```
conda env create -n nhdpy -f environment.yml
make install
```

## Usage

``` python
import nhdpy

nhdpy.nhd_get(state = "DC")

nhdpy.nhd_list(state = "DC")

dc_waterbodies = nhdpy.nhd_load("DC", "NHDWaterbody")

# import matplotlib.pyplot as plt
# dc_waterbodies.iloc[1:2].plot()
# plt.show()
```
