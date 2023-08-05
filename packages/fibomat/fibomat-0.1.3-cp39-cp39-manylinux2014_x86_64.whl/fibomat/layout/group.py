"""Provide the :class:`Group` class."""
# pylint: disable=protected-access
from __future__ import annotations
from typing import Optional, List, Iterator

from fibomat.layout.layoutbase import LayoutBase
from fibomat.linalg import Vector, VectorLike, Transformable


class Group(LayoutBase):
    """Class to group Transformable objects together."""
    def __init__(
        self,
        elements: List[Transformable],
        description: Optional[str] = None
    ):
        super().__init__(description)

        self._elements: List[Transformable] = elements

    def _layout_elements(self) -> Iterator[Transformable]:
        for element in self._elements:
            yield element

    @property
    def center(self) -> Vector:
        if not self._elements:
            raise RuntimeError('Cannot calculate center of empty Group.')

        center = self._elements[0].center
        for element in self._elements[1:]:
            center += element.center
        return center / len(self._elements)

    def _impl_translate(self, trans_vec: VectorLike) -> None:
        for element in self._elements:
            element._impl_translate(trans_vec)

    def _impl_rotate(self, theta: float) -> None:
        for element in self._elements:
            element._impl_rotate(theta)

    def _impl_scale(self, fac: float) -> None:
        for element in self._elements:
            element._impl_scale(fac)

    def _impl_mirror(self, mirror_axis: VectorLike) -> None:
        for element in self._elements:
            element._impl_mirror(mirror_axis)
