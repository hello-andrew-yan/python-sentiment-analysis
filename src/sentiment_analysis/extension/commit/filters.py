import polars as pl

from sentiment_analysis.core.filter import Filter


class Length(Filter):
    def __init__(self, column: str, min_len: int, max_len: int):
        self.column = column
        self.min_len = min_len
        self.max_len = max_len

    def __call__(self):
        return (
            pl.col(self.column).str.len_chars().is_between(self.min_len, self.max_len)
        )


class Matches(Filter):
    def __init__(self, column: str, pattern: str):
        self.column = column
        self.pattern = pattern

    def __call__(self) -> pl.Expr:
        return pl.col(self.column).str.contains(self.pattern, literal=False)
