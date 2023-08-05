from typing import Tuple, Sequence

import numpy as np

from fibomat.shapes.rasterizedpoints import RasterizedPoints
from fibomat.raster_styles.rasterstyle import RasterStyle
from fibomat.units import LengthUnit, TimeUnit, scale_to, scale_factor
from fibomat.dimensioned_object import DimObjLike, DimObj
from fibomat.shapes import Shape
from fibomat.mill import Mill


class PreRasterized(RasterStyle):
    def __init__(self):
        pass

    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    @property
    def dimension(self) -> int:
        return 0

    @staticmethod
    def _prepare_and_scale(
        dim_shape: DimObjLike[RasterizedPoints, LengthUnit],
        mill: Mill,
        out_length_unit: LengthUnit,
        out_time_unit: TimeUnit
    ) -> RasterizedPoints:
        dim_shape = DimObj.create(dim_shape)
        points = np.array(dim_shape.obj.dwell_points)

        if not isinstance(dim_shape.obj, RasterizedPoints):
            raise TypeError('Shape must be of type RasterizedPoints for PreRasterized style')

        points[:, :2] *= scale_factor(out_length_unit, dim_shape.unit)
        points[:, 2] *= scale_to(out_time_unit, mill.dwell_time)

        if mill.repeats != 1:
            return RasterizedPoints(np.concatenate([points]*mill.repeats), dim_shape.obj.is_closed)
        else:
            return points

    def rasterize(
        self,
        dim_shape: DimObjLike[RasterizedPoints, LengthUnit],
        mill: Mill,
        out_length_unit: LengthUnit,
        out_time_unit: TimeUnit
    ) -> RasterizedPoints:
        return self._prepare_and_scale(dim_shape, mill, out_length_unit, out_time_unit)

    def explode(
        self,
        dim_shape: DimObjLike[Shape, LengthUnit],
        mill: Mill,
        out_length_unit: LengthUnit,
        out_time_unit: TimeUnit
    ) -> Sequence[Tuple[Shape, RasterStyle]]:
        return [(self._prepare_and_scale(dim_shape, mill, out_length_unit, out_time_unit), self)]
