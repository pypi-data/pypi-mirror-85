"""
Provides the :class:`Pattern` class.
"""
# pylint: disable=protected-access
from __future__ import annotations
from typing import Generic, TypeVar, Optional

from fibomat.mill import Mill
from fibomat.units import LengthUnit
from fibomat.boundingbox import BoundingBox
from fibomat.linalg import VectorLike, Transformable, Vector
from fibomat.raster_styles import RasterStyle
from fibomat.dimensioned_object import DimObj, DimObjLike


T = TypeVar('T', bound=Transformable)


class Pattern(Transformable, Generic[T]):
    """
    Class is used to collect a shape with a length unit,  mill settings and optional settings.
    """

    def __init__(
        self,
        dim_shape: DimObjLike[T, LengthUnit],
        shape_mill: Mill,
        raster_style: RasterStyle,
        description: Optional[str] = None,
        **kwargs
    ):
        """

        Args:
            dim_shape (Tuple[ShapeType, units.LengthUnit]):
                tuple of a shape type and its length unit. ShapeType can be any transformable, e.g. a layout.Group or
                shapes.Line, ...
            shape_mill (Mill): mill object
            **kwargs: additional args
        """
        super().__init__(description=description)

        self.dim_shape = dim_shape if isinstance(dim_shape, DimObj) else DimObj(*dim_shape)
        self.shape_mill = shape_mill
        self.raster_style = raster_style
        self.kwargs = kwargs

    @property
    def bounding_box(self) -> BoundingBox:
        return self.dim_shape.obj.bounding_box

    @property
    def center(self) -> Vector:
        return self.dim_shape.obj.center

    def _impl_translate(self, trans_vec: VectorLike) -> None:
        self.dim_shape.obj._impl_translate(trans_vec)

    def _impl_rotate(self, theta: float) -> None:
        self.dim_shape.obj._impl_rotate(theta)

    def _impl_scale(self, fac: float) -> None:
        self.dim_shape.obj._impl_scale(fac)

    def _impl_mirror(self, mirror_axis: VectorLike) -> None:
        self.dim_shape.obj._impl_mirror(mirror_axis)
