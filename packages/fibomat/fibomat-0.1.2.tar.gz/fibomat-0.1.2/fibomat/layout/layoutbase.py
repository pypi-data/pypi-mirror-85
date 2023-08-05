"""Provide the :class:`LayoutBase` class."""
from __future__ import annotations
from typing import Optional, Iterator, Union
import abc

from fibomat.linalg import Transformable, Vector
from fibomat import boundingbox
from fibomat.shapes import Shape


class LayoutBase(Transformable, abc.ABC):
    """
    ABC for all layout related classes.

    It can be used to arrange :class:`fibomat.site.Site`, :class:`fibomat.pattern.Pattern` and
    :class:`fibomat.shapes.Shape`.

    The saved are accessed via the :meth:`LayoutBase.layout_elements` method which returns a generator containing all
    included elements.

    What kind of elements and how these are set must be specified in child classes.

    """

    def __init__(self, description: Optional[str] = None):
        """
        Args:
            description (str, optional): description
        """
        super().__init__(description=description)

    @abc.abstractmethod
    def _layout_elements(self) -> Iterator[Transformable]:
        raise NotImplementedError

    def layout_elements(self) -> Iterator[Transformable]:
        """Access to the saved elements.

        Yields:
            Any: Type depends on saved element.
        """
        for element in self._layout_elements():
            if isinstance(element, LayoutBase):
                for sub_element in element._layout_elements():  # pylint: disable=protected-access
                    yield sub_element
            else:
                yield element

    @property
    def bounding_box(self) -> boundingbox.BoundingBox:
        """Bounding box of shape (getter)

        Access:
            get

        Returns:
            BoundingBox

        Raises:
            RuntimeError: Raised if Layout object does not contain any elements
        """
        element_iter = self.layout_elements()

        try:
            bbox = next(element_iter).bounding_box
        except StopIteration:
            raise RuntimeError('Cannot calculate bounding box of empty Layout.')  # pylint: disable=raise-missing-from

        for element in element_iter:
            bbox = bbox.extended(element.bounding_box)

        return bbox
