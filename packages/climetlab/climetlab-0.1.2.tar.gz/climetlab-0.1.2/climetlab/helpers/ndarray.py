# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#


class NumpyArrayHelper:
    def __init__(self, data):
        self.data = data

    def plot_map(self, driver):
        field = driver.option("field")
        grid = driver.option("grid")
        metadata = driver.option("metadata")

        if metadata is None and field is not None:
            metadata = field.metadata()

        if grid is None and field is not None:
            grid = field.grid_definition()

        driver.bounding_box(
            north=grid["north"],
            south=grid["south"],
            west=grid["west"],
            east=grid["east"],
        )

        driver.plot_numpy(
            self.data,
            north=grid["north"],
            west=grid["west"],
            south_north_increment=grid["south_north_increment"],
            west_east_increment=grid["west_east_increment"],
            metadata=metadata,
        )


helper = NumpyArrayHelper
