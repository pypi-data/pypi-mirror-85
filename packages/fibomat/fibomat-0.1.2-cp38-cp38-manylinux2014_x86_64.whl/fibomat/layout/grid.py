"""Provide the :class:`Grid` class."""
# pylint: disable=invalid-name,protected-access
from __future__ import annotations
from typing import Optional, Iterator, Tuple
import itertools

import numpy as np

from fibomat.linalg import Transformable, VectorLike, Vector
from fibomat.layout.layoutbase import LayoutBase
from fibomat.layout._grid_coordinates import GridCoordinates


class Grid(LayoutBase):
    """
    A grid layout. It is specified by the lengths of the basis vectors (du and dv) and the enclosed angle (alpha).

    E.g. ::

        grid = Grid[Shape](nu=2, nv=2, du=10, dv=10)

    would result in a 2 by 2 grid with spacing of 10.

    Elements get be set by ::

        grid.set_element((0, 0), Spot(...))
        grid.set_element((1, 0), Line(...))

        rect = Rect(...)
        grid.set_element((1, 0), Line(...), copy=True)  # by default, copy is False. Hence, rect would be translated if
                                                        # added to grid

    .. warning:: Each shape element will be shifted automatically so that it's pivot is equal to the grid coordinate.

    Internally, the added elements will be accessed by the :meth:`Grid.layout_elements` method. If any elem is not set,
    it will be skipped. ::

                 ----v--->

        |   ( 0,  0) | ( 0,  1) | ( 0,  2)
        u    ---------+----------+---------
        V   ( 1,  0) | ( 1,  1) | ( 1,  2)
            ---------+----------+---------
            ( 2,  0) | ( 2,  1) | ( 2,  2)
            ---------+----------+---------
            ( 3,  0) | ( 3,  1) | ( 3,  2)

        alpha = enclosed angle by \\vec{u}, \\vec{v}
        |\\vec{u}| = du, |\\vec{v}| = dv,

    .. warning:: This class is not immutable!

    .. warning:: Transformations will be applied to grid and stored elements.

    """
    def __init__(
            self,
            nu: int, nv: int,
            du: float, dv: float,
            element: Optional[Transformable] = None,
            alpha: Optional[float] = np.pi / 2,
            center: Optional[VectorLike] = None,
            description: Optional[str] = None):
        """

        Args:
            nu (int): elements in `u` direction
            nv (int): elements in `v` direction
            du (float): length of basis linalg in u direction
            dv (float): length of basis linalg in v direction
            element (Optional[Transformable]): if given, element is copied to all grid sites
            alpha (float, optional): angle between basis linalg, default to pi/2
            center (VectorLike, optional): center of grid
            description (str, optional): description
        """
        super().__init__(description)

        self._grid_coords = GridCoordinates(nu, nv, du, dv, alpha, center)

        self._elements = list(np.full_like(self._grid_coords.grid, None, dtype=object))

        if element:
            for iu in range(self._grid_coords.nu):
                for iv in range(self._grid_coords.nv):
                    self._set_element((iu, iv), element)

    def __getitem__(self, point: Tuple[int, int]) -> Transformable:
        iu, iv = point
        return self._elements[iu][iv]

    def _set_element(self, point: Tuple[int, int], element: Transformable):
        iu, iv = point

        trans_vec = self._grid_coords[iu, iv] - element.pivot

        self._elements[iu][iv] = element.translated(trans_vec)

    def __setitem__(self, point: Tuple[int, int], element: Transformable):
        self._set_element(point, element)

    def _layout_elements(self) -> Iterator[Transformable]:
        for iu in range(self._grid_coords.nu):
            for iv in range(self._grid_coords.nv):
                # yield iu, iv, self._grid_coords[iu, iv], self._elements[iu, iv]
                elem = self._elements[iu][iv]
                if elem:
                    # trans_vec = self._grid_coords[iu, iv] - elem.pivot
                    yield elem  # .translate(trans_vec)

    @property
    def center(self) -> Vector:
        return self._grid_coords.center

    def _impl_translate(self, trans_vec: VectorLike) -> None:
        self._grid_coords._impl_translate(trans_vec)

        for element in itertools.chain.from_iterable(self._elements):
            if element:
                element._impl_translate(trans_vec)

        # with np.nditer(self._elements, op_flags=['readwrite'], flags=["refs_ok"], op_dtypes=['object']) as it:
        #     for element in it:
        #         print(len(element))
        #         element._impl_translate(trans_vec)

    # def rotated(self, theta: float, origin: Optional[Union[VectorLike, str]] = None) -> None:
    #     for element in itertools.chain.from_iterable(self._elements):
    #         if element:
    #             # element._impl_translate(-self.center)
    #             element._impl_rotate(theta)
    #             # element._impl_translate(self.center)
    #
    #     return self

    def _impl_rotate(self, theta: float) -> None:
        self._grid_coords._impl_rotate(theta)

        for element in itertools.chain.from_iterable(self._elements):
            if element:
                element._impl_rotate(theta)

    def _impl_scale(self, fac: float) -> None:
        self._grid_coords._impl_scale(fac)

        for element in itertools.chain.from_iterable(self._elements):
            if element:
                element._impl_scale(fac)

    def _impl_mirror(self, mirror_axis: VectorLike) -> None:
        self._grid_coords._impl_mirror(mirror_axis)

        for element in itertools.chain.from_iterable(self._elements):
            if element:
                element._impl_mirror(mirror_axis)
