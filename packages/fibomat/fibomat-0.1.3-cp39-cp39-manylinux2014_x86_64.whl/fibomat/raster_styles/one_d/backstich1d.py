from typing import Tuple

from fibomat.shapes import rasterizedpoints
from fibomat.rasterizing.styles import curvestyle
from fibomat import units
from fibomat import shapes
from fibomat import curve_tools


class Backstitch1d(curvestyle.CurveStyle):
    def __init__(self, pitch: units.QuantityType):
        self._pitch = pitch

        if not units.has_length_dim(self._pitch):
            raise ValueError('Pitch must have [length] as dimension')

        if self._pitch.m <= 0:
            raise ValueError('pitch must be greater than 0.')

    @property
    def pitch(self) -> units.QuantityType:
        return self._pitch

    def rasterize(self, dim_shape: Tuple[shapes.Shape, units.LengthUnit]) -> rasterizedpoints.RasterizedPoints:
        raster = curve_tools.rasterize(shapes.Curve.from_shape(dim_shape[0]), units.scale_to(dim_shape[1], self._pitch))

        # dwell points are indexed by 0, 1, 2, 3, 4, 5, ...
        # with backstich, points should be ordered like 1, 0, 3, 2, 5, 4, ...
        # hence, consecutive pairs of points must be swapped
        for i in range(0, len(raster.dwell_points) - 1, 2):
            raster.dwell_points[i], raster.dwell_points[i + 1] = raster.dwell_points[i + 1], raster.dwell_points[i]

        return raster


