# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

from climetlab import load_source

from . import Dataset


class WeatherBench(Dataset):
    """
    This is an attempt to reproduce this research: https://arxiv.org/abs/2002.00469.
    See https://raspstephan.github.io/blog/weatherbench/
    There is a notebook available at: https://binder.pangeo.io/v2/gh/pangeo-data/WeatherBench/master?filepath=quickstart.ipynb
    """

    home_page = "https://raspstephan.github.io/blog/weatherbench/"
    citation = """@article{rasp2020weatherbench,
  title={WeatherBench: A benchmark dataset for data-driven weather forecasting},
  author={Rasp, Stephan and Dueben, Peter D and Scher, Sebastian and Weyn, Jonathan A and Mouatadid, Soukayna and Thuerey, Nils},
  journal={arXiv preprint arXiv:2002.00469},
  year={2020}
}
"""

    def __init__(self, parameter="geopotential_500", resolution=5.625):
        url = "https://dataserv.ub.tum.de/s/m1524895/download?path=%2F{resolution}deg%2F{parameter}&files={parameter}_{resolution}deg.zip".format(
            resolution=resolution, parameter=parameter
        )
        self.source = load_source("url", url, unpack=True)


dataset = WeatherBench
