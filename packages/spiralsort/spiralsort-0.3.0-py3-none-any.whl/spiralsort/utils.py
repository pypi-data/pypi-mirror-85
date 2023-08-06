# utils.py is part of SpiralSort
#
# SpiralSort is free software; you may redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. You should have received a copy of the GNU
# General Public License along with this program. If not, see
# <https://www.gnu.org/licenses/>.
#
# (C) 2020 Athanasios Mattas
# ======================================================================
"""Houses some helper functions"""

from datetime import timedelta
from functools import wraps
import os
from timeit import default_timer as timer

import click
import numpy as np
import pandas as pd

from spiralsort import config


def check_duplicated_ids(nodes):
    """check node_ids uniqueness"""
    duplicated_ids = nodes[nodes.node_id.duplicated()].node_id.to_list()
    if duplicated_ids:
        raise Exception("node_id column has duplicated entries: {}"
                        .format(duplicated_ids))
    return True


def point_cloud_mock():
    """creates a mock point-cloud"""
    np.random.seed(2)
    num_nodes = config.NUM_NODES

    x = np.random.rand(num_nodes) - 0.5
    y = np.random.rand(num_nodes) - 0.5
    z = np.random.rand(num_nodes) - 0.5

    id_range = np.arange(num_nodes)
    max_length = len(str(num_nodes))
    node_id = ["N_" + (max_length - len(str(x))) * '0' + str(x)
               for x in id_range]

    cloud = pd.DataFrame(
        {
            "node_id": node_id,
            'x': x,
            'y': y,
            'z': z
        }
    )

    cloud["d_squared"] = cloud.x ** 2 + cloud.y ** 2 + cloud.z ** 2

    # exclude an inner sphere and pick the topmost node as the start
    # node, to assist visualization
    cloud = cloud[cloud.d_squared > 0.21]
    start_node_id = cloud.loc[cloud.z.idxmax(), "node_id"]

    # have a sneak peek
    # from spiralsort import spiralsort_post as ssp
    # ssp.quick_scatter(cloud.x, cloud.y, cloud.z)

    return cloud.loc[:, ["node_id", 'x', 'y', 'z']], start_node_id


def create_slices(nodes):
    """segments nodes into slices, not to work on the whole df

    [
        [0, 2000], [2000, 6000], [6000, 14000], [14000, 30000],
        [30000, 62000], [62000, 94000], [94000, 126000], ...
    ]
    """
    BASE = config.BASE
    CONST_WINDOW = config.CONST_WINDOW
    slice_bins = pd.DataFrame({"bins": [2000, 6000, 14000, 30000, np.inf],
                               "max_exponent": [1, 2, 3, 4, 5]})
    num_nodes = len(nodes.index)
    max_exponent = slice_bins.loc[slice_bins.bins.searchsorted(num_nodes),
                                  "max_exponent"]
    slices =                                                                  \
        [slice(BASE * (2 ** n - 1), BASE * (2 ** (n + 1) - 1))
         for n in range(max_exponent)]                                        \
        + [slice(start, start + CONST_WINDOW)
           for start in range(BASE * (2 ** (max_exponent) - 1) + CONST_WINDOW,
                              len(nodes.index),
                              CONST_WINDOW)]
    return slices


def calc_half_slice(slicing_obj):
    """calculates the half of the range of a slice"""
    half_slice = (slicing_obj.indices(int(1e100))[1]
                  - slicing_obj.indices(int(1e100))[0]) // 2
    return half_slice


def delete_images(directory):  # pragma: no cover
    """deletes all images in a given directory (for debugging)"""
    files_list = [f for f in os.listdir(directory)]
    for f in files_list:
        if f.endswith(".png") or f.endswith(".jpg"):
            os.remove(os.path.join(directory, f))


def print_duration(start, end, process):
    """prints the duration of a process"""
    process_name = {
        "main": "Total",
        "spiralsorted": "SpiralSort",
        "animate": "Post-processing"
    }
    if process in process_name:
        prefix = f"{process_name[process]} duration"
    else:
        prefix = f"{process.capitalize()} duration"
    duration = timedelta(seconds=end - start)
    click.echo(f"{prefix:-<30}{duration}"[:40])


def time_this(f):
    """function timer decorator

    - Uses wraps to preserve the metadata of the decorated function
      (__name__ and __doc__)
    - prints the duration

    Args:
        f(funtion)      : the function to be decorated

    Returns:
        wrap (callable) : returns the result of the decorated function
    """
    assert callable(f)

    @wraps(f)
    def wrap(*args, **kwargs):
        start = timer()
        result = f(*args, **kwargs)
        end = timer()
        print_duration(start, end, f.__name__)
        return result
    return wrap
