# -*- coding: utf-8 -*-
import enum


class Cardinality(enum.Enum):
    UNARY_UNARY = 1
    UNARY_STREAM = 2
    STREAM_UNARY = 3
    STREAM_STREAM = 4
