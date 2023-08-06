"""
k3math is a toy math impl
"""


__version__ = "0.1.2"
__name__ = "k3math"

from .mth import Matrix
from .mth import Polynomial
from .mth import Vector

__all__ = [
    "Vector",
    "Matrix",
    "Polynomial",
]
