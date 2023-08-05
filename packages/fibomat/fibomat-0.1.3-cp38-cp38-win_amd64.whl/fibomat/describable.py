"""Provides the :class:`Describable` class."""
from typing import Optional


class Describable:
    """This class handles optional descriptions in the fib-o-mat library."""
    def __init__(self, description: Optional[str] = None):
        """
        Args:
            description (str, optional): description
        """
        self._description = str(description) if description else None

    @property
    def description(self) -> Optional[str]:
        """Description str.

        Access:
            get

        Returns:
            Optional[str]
        """
        return self._description

