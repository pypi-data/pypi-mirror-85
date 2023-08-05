"""
Implements the PathSearchMethods enumeration.

Copyright 2019, 2020 William W. Kimball, Jr. MBA MSIS
"""
from enum import Enum, auto
from typing import List


class PathSearchMethods(Enum):
    """
    Supported selfs for searching YAML Path segments.

    These include:

    `CONTAINS`
        Matches when the haystack contains the needle.

    `ENDS_WITH`
        Matches when the haystack ends with the needle.

    `EQUALS`
        Matches when the haystack and needle are identical.

    `STARTS_WITH`
        Matches when the haystack starts with the needle.

    `GREATER_THAN`
        Matches when the needle is greater than the haystack.

    `LESS_THAN`
        Matches when the needle is less than the haystack.

    `GREATER_THAN_OR_EQUAL`
        Matches when the needle is greater than or equal to the haystack.

    `LESS_THAN_OR_EQUAL`
        Matches when the needle is less than or equal to the haystack.

    `REGEX`
        Matches when the needle Regular Expression matches the haystack.
    """

    CONTAINS = auto()
    ENDS_WITH = auto()
    EQUALS = auto()
    STARTS_WITH = auto()
    GREATER_THAN = auto()
    LESS_THAN = auto()
    GREATER_THAN_OR_EQUAL = auto()
    LESS_THAN_OR_EQUAL = auto()
    REGEX = auto()

    def __str__(self) -> str:
        """Get a String representation of an employed value of this enum."""
        operator = ''
        if self is PathSearchMethods.EQUALS:
            operator = '='
        elif self is PathSearchMethods.STARTS_WITH:
            operator = '^'
        elif self is PathSearchMethods.ENDS_WITH:
            operator = '$'
        elif self is PathSearchMethods.CONTAINS:
            operator = '%'
        elif self is PathSearchMethods.LESS_THAN:
            operator = '<'
        elif self is PathSearchMethods.GREATER_THAN:
            operator = '>'
        elif self is PathSearchMethods.LESS_THAN_OR_EQUAL:
            operator = '<='
        elif self is PathSearchMethods.GREATER_THAN_OR_EQUAL:
            operator = '>='
        elif self is PathSearchMethods.REGEX:
            operator = '=~'

        return operator

    @staticmethod
    def get_operators() -> List[str]:
        """Return the full list of suppoerted symbolic search operators."""
        return [str(o) for o in PathSearchMethods]

    @staticmethod
    def is_operator(symbol: str) -> bool:
        """Indicate whether symbol is a known search method operator."""
        return symbol in PathSearchMethods.get_operators()
