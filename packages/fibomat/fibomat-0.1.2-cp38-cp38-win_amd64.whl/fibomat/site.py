"""
Provides the :class:`Site` class.
"""
from __future__ import annotations

from typing import Optional, List, Tuple, Union
from copy import deepcopy

from fibomat.boundingbox import BoundingBox
from fibomat.linalg import VectorLike, Vector, Transformable
from fibomat.units import LengthUnit, UnitType
from fibomat.shapes import Shape
from fibomat import mill
from fibomat import layout
from fibomat.pattern import Pattern

from fibomat.dimensioned_object import DimObj, DimObjLike


class Site(Transformable):
    """
    The `Site` class is used to collect shapes with its patterning settings.

    .. note:: All shape positions added to each site are interpreted relative to the site's position!

    .. note:: If fov is not passed, it will be determined by the bounding box of the added patterns.

    Args:
        position (VectorLike):
            Center coordinate of the site.
        unit(UnitType):
            length unit to be used for positioning of the site
        fov (VectorLike, optional):
            the fov (field of view) to be used
        description (str, optional):
            description of the layer

    """
    def __init__(
            self,
            dim_position: DimObjLike[VectorLike, LengthUnit],
            dim_fov: DimObjLike[VectorLike] = None,
            description: Optional[str] = None
    ):
        super().__init__(description=description)

        dim_position = DimObj.create(dim_position)
        dim_fov = DimObj.create(dim_fov)

        self._center = Vector(dim_position.obj)
        # if position_unit.dimensionality != '[length]':
        #     raise ValueError('position_unit must have dimension [length]')
        self._position_unit = dim_position.unit
        self._fov = Vector(dim_fov.obj) if dim_fov is not None else None
        self._fov_unit = dim_fov.unit if dim_fov is not None else None
        # self._description: Optional[str] = str(description) if description else None

        self._patterns: List[Pattern] = []

    @property
    def description(self) -> Optional[str]:
        """
        str: Description of the object

        Access: get/set
        """
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def center(self) -> Vector:
        """
        :class:`~fibomat.linalg.linalg.Vector`: site's center

        Access: get
        """
        return self._center

    @property
    def fov(self) -> DimObj[Vector, LengthUnit]:
        """
        :class:`~fibomat.linalg.linalg.Vector`: fov

        Access: get
        """
        if self._fov:
            return DimObj(self._fov, self._fov_unit)
        else:
            raise NotImplementedError
            # TODO: what todo if self.empty ?
            # bbox = self.bounding_box
            # ll = bbox.lower_left
            # up = bbox.upper_right
            #
            # bbox.extend(2*self._center - ll)
            # bbox.extend(2*self._center - up)
            #
            # scale_fac = units.scale_factor(self._fov_unit, self._)
            #
            # return linalg.Vector(bbox.width, bbox.height), self._fov_unit

    @property
    def fov_unit(self) -> LengthUnit:
        return self._fov_unit

    @property
    def squrare_fov(self) -> DimObj[Vector, LengthUnit]:
        """
        :class:`~fibomat.linalg.linalg.Vector`: fov

        Access: get
        """
        fov = self.fov.obj
        return DimObj(Vector(fov.x, fov.x) if fov.x > fov.y else Vector(fov.y, fov.y), self._fov_unit)

    @property
    def unit(self) -> UnitType:
        """
        UnitType: length unit to be used for positioning of the site

        Access: get
        """
        return self._position_unit

    @property
    def empty(self) -> bool:
        """
        bool: True if site does not contain any pattern

        Access: get
        """
        return not bool(self._patterns)

    @property
    def bounding_box(self) -> Optional[BoundingBox]:
        """
        Optional[BoundingBox]: bounding box of the added shapes, not of the site.

        Access: get
        """
        raise NotImplementedError

        # # TODO: account for shape units
        # if self._patterns:
        #     bbox: BoundingBox = self._patterns[0].shape.bounding_box
        #     for pattern in self._patterns:
        #         bbox.extend(pattern.shape.bounding_box)
        #     return bbox
        # else:
        #     return None

    @property
    def patterns(self):
        """
        List[patterns]: contained patterns in site

        Access: get
        """
        return self._patterns

    def create_pattern(
        self,
        dim_shape: DimObjLike[Transformable, LengthUnit],
        shape_mill: Mill,
        raster_style: RasterStyle,
        description: Optional[str] = None,
        **kwargs
    ) -> Pattern:
        pattern = Pattern(dim_shape, shape_mill, raster_style, description=description, **kwargs)
        self.add_pattern(pattern)
        return pattern

    def add_pattern(self, ptn: Union[Pattern, layout.LayoutBase], copy: bool = True) -> None:
        """
        Adds a :class:`fibomat.pattern.Pattern` to the site.

        Args:
            ptn (Pattern):
                new pattern
            copy (bool):
                if pattern is deep copied

        Returns:
            None
        """
        if copy:
            ptn = deepcopy(ptn)

        if isinstance(ptn, layout.LayoutBase):
            for extracted_pattern in ptn.layout_elements():
                self._patterns.append(extracted_pattern)
        else:
            self._patterns.append(ptn)

    def __iadd__(self, ptn:  Union[Pattern, layout.LayoutBase]) -> Site:
        """
        Adds a :class:`fibomat.pattern.Pattern` to the site.
        `ohter` is deep copied.

        Args:
            other: new pattern

        Returns:
            None
        """
        self.add_pattern(ptn, copy=True)
        return self

    def _impl_translate(self, trans_vec: VectorLike) -> None:
        self._center += trans_vec

    def _impl_rotate(self, theta: float) -> None:
        raise NotImplementedError

    def _impl_scale(self, fac: float) -> None:
        raise NotImplementedError

    def _impl_mirror(self, mirror_axis: VectorLike) -> None:
        raise NotImplementedError
