from typing import Tuple, Sequence

from fibomat.shapes.rasterizedpoints import RasterizedPoints
from fibomat.raster_styles.rasterstyle import RasterStyle
from fibomat.units import LengthUnit, TimeUnit, scale_to, has_length_dim, QuantityType, scale_factor
from fibomat.dimensioned_object import DimObjLike, DimObj
from fibomat.shapes import Shape
from fibomat.mill import Mill
from fibomat.curve_tools import rasterize


class Linear(RasterStyle):
    def __init__(self, pitch: QuantityType):
        self._pitch = pitch

        if not has_length_dim(self._pitch):
            raise ValueError('Pitch must have [length] as dimension')

        if self._pitch.m <= 0:
            raise ValueError('pitch must be greater than 0.')

    def __repr__(self):
        return '{}(pitch={!r})'.format(self.__class__.__name__, self._pitch)

    @property
    def dimension(self) -> int:
        return 1

    @property
    def pitch(self) -> QuantityType:
        return self._pitch

    def rasterize(
        self,
        dim_shape: DimObjLike[Shape, LengthUnit],
        mill: Mill,
        out_length_unit: LengthUnit,
        out_time_unit: TimeUnit
    ) -> RasterizedPoints:
        dim_shape = DimObj.create(dim_shape)

        pitch_scaled = scale_to(dim_shape.unit, self._pitch)

        points = rasterize(dim_shape.obj, pitch_scaled)

        points._dwell_points[:, :2] *= scale_factor(out_length_unit, dim_shape.unit)
        points._dwell_points[:, 2] = scale_to(out_time_unit, mill.dwell_time)

        return points.repeats_applied(mill.repeats)

    def explode(
        self,
        dim_shape: DimObjLike[Shape, LengthUnit],
        mill: Mill,
        out_length_unit: LengthUnit,
        out_time_unit: TimeUnit
    ) -> Sequence[Tuple[Shape, RasterStyle]]:
        raise NotImplementedError

