# -*- coding: utf-8 -*-
from typing import NamedTuple, Tuple

__all__ = ['Size']


class Size(NamedTuple):
    w: int
    h: int

    @staticmethod
    def from_tuple(tp: Tuple[int, int]):
        return Size(w=tp[0], h=tp[1])
