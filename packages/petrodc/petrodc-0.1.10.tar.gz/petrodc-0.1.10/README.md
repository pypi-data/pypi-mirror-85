![](https://user-images.githubusercontent.com/52009346/69100304-2eb3e800-0a5d-11ea-9a3a-8e502af2120b.png)

[![PyPI version](https://badge.fury.io/py/petrodc.svg)](https://badge.fury.io/py/petrodc)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Webapp](https://img.shields.io/badge/WebApp-On-green.svg)](https://pwp-opensource.herokuapp.com/)

## Introduction
PetroDC is a LGPL licensed tool to get datasets from public sources. 
New sources are added as they are tested; suggestions and contributions of 
all kinds are very welcome.

## Documentation

Check here for the [complete petrodc package documentation](https://petrodc.readthedocs.io/en/latest/).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Get petrodc

* Users: Wheels for Python from [PyPI](https://pypi.python.org/pypi/petrodc/) 
    * `pip install petrodc`
* Developers: Source code from [Github](https://github.com/pro-well-plan/petrodc)
    * `git clone https://github.com/pro-well-plan/petrodc`

## Quick Use

> import petrodc.npd as dc
>
> dataframe = dc.wellbore(3)

* 3 is the dataset with lithostratigraphy, check [here](https://github.com/pro-well-plan/petrodc/blob/master/petrodc/npd/wellbore.py)
to see the respective number for the different datasets.

## License

This project is licensed under the GNU Lesser General Public License v3.0 - see the [LICENSE](LICENSE.md) file for details


*for further information contact juan@prowellplan.com*
