import operator
from abc import ABC, abstractmethod
from collections.abc import Callable

import polars as pl


class Filter(ABC):
    @abstractmethod
    def __call__(self) -> pl.Expr: ...

    def __and__(self, other: "Filter") -> "Filter":
        return _BinaryFilter(self, other, operator.and_)

    def __or__(self, other: "Filter") -> "Filter":
        return _BinaryFilter(self, other, operator.or_)

    def __invert__(self) -> "Filter":
        return _UnaryFilter(self, operator.invert)

    @property
    def name(self) -> str:
        return type(self).__name__


class _BinaryFilter(Filter):
    def __init__(self, left: Filter, right: Filter, op: Callable):
        self.left, self.right, self.op = left, right, op

    def __call__(self) -> pl.Expr:
        return self.op(self.left(), self.right())

    @property
    def name(self) -> str:
        return f"({self.left.name}_{self.op.__name__}{self.right.name})"


class _UnaryFilter(Filter):
    def __init__(self, operand: Filter, op: Callable):
        self.operand, self.op = operand, op

    def __call__(self) -> pl.Expr:
        return self.op(self.operand())

    @property
    def name(self) -> str:
        return f"({self.op.__name__}_{self.operand.name})"
