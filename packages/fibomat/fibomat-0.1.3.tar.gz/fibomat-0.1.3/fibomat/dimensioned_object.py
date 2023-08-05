"""Provide the :class:`DimensionedObj` class."""
from __future__ import annotations

from typing import Generic, TypeVar, Union, Tuple, Type

from dataclasses import dataclass

from fibomat.units import UnitType


ObjT = TypeVar('ObjT')
UnitT = TypeVar('UnitT', bound=UnitType)
DimObjT = TypeVar('DimObjT', bound='DimensionedObj')


@dataclass(frozen=True)
class DimensionedObj(Generic[ObjT, UnitT]):
    """Class should be used if any kind of object must have an associated unit.

    Examples::

        dim_shape = DimensionedObj((Line([0, 0], [1, 1]), U_('µm'))

        # DimObj is an alias of DimensionedObj
        dim_shape = DimObj((Line([0, 0], [1, 1]), U_('µm'))
    """
    obj: ObjT
    unit: UnitT

    @classmethod
    def create(cls: Type[DimObjT], dim_obj: Union[DimObjT, Tuple[ObjT, UnitT]]) -> DimensionedObj[ObjT, UnitT]:
        """Parse a object and create a :class:`DimensionedObj` from a tuple or class instance.

        No checks are performed at the arguments.

        Args:
            dim_obj (DimensionedObj[[ObjT, UnitT], Tuple[ObjT, UnitT]): dimensioned object

        Returns:
            DimensionedObj[ObjT, UnitT]

        Raises:
            TypeError: Raised if `dim_obj` cannot be parsed.
        """
        if isinstance(dim_obj, cls):
            return dim_obj

        if isinstance(dim_obj, tuple):
            return cls(*dim_obj)

        raise TypeError('Cannot parse "dim_obj".')


DimObj = DimensionedObj

DimObjLike = Union[DimensionedObj[ObjT, UnitT], Tuple[ObjT, UnitT]]
