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


class Contains(Filter):
    def __init__(self, column: str, word: str):
        self.column = column
        self.word = word

    def __call__(self):
        return pl.col(self.column).str.contains(self.word, literal=True, strict=False)
