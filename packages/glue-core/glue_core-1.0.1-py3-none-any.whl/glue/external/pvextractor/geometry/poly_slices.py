from __future__ import print_function

import numpy as np
from astropy.utils.console import ProgressBar

from .polygon import square_polygon_overlap_area


def extract_poly_slice(cube, polygons, return_area=False):
    """
    Extract the values of polygonal chunks from a data cube

    Parameters
    ----------
    cube : np.ndarray
    polygons : 
    return_area : bool
        If set, return the area of each polygon and the sum over that area.
        Otherwise, return the mean.
    """

    nx = len(polygons)
    nz = cube.shape[0]

    total_slice = np.zeros((nz, nx))
    total_area = np.zeros((nz, nx))

    p = ProgressBar(len(polygons))

    for i, polygon in enumerate(polygons):

        p.update()

        # Find bounding box
        bbxmin = int(round(np.min(polygon.x))-1)
        bbxmax = int(round(np.max(polygon.x))+2)
        bbymin = int(round(np.min(polygon.y))-1)
        bbymax = int(round(np.max(polygon.y))+2)

        # Clip to cube box
        bbxmin = max(bbxmin, 0)
        bbxmax = min(bbxmax, cube.shape[2])
        bbymin = max(bbymin, 0)
        bbymax = min(bbymax, cube.shape[1])

        # Loop through pixels that might overlap
        for xmin in np.arange(bbxmin, bbxmax):
            for ymin in np.arange(bbymin, bbymax):

                area = square_polygon_overlap_area(xmin-0.5, xmin+0.5,
                                                   ymin-0.5, ymin+0.5,
                                                   polygon.x, polygon.y)

                if area > 0:
                    dataslice = cube[:, ymin, xmin]
                    good_values = np.isfinite(dataslice)
                    if np.any(good_values):
                        total_slice[good_values, i] += dataslice[good_values] * area
                        total_area[good_values, i] += area

    total_slice[total_area == 0.] = np.nan
    if return_area:
        return total_slice, total_area
    total_slice[total_area > 0.] /= total_area[total_area > 0.]

    print("")

    return total_slice
