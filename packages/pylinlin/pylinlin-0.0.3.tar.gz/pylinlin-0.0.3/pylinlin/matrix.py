from __future__ import annotations
from typing import List
import math


class Matrix:

    @staticmethod
    def from_rows(rows: List[List[float]]):
        num_rows = len(rows)
        num_cols = len(rows[0])
        for row in rows:
            if len(row) != num_cols:
                raise ValueError("Rows must have equal length")
        cols = [[0] * num_rows for _ in range(num_cols)]
        for row_index, row in enumerate(rows):
            for col_index, elem in enumerate(row):
                cols[col_index][row_index] = elem
        return Matrix(cols)

    @staticmethod
    def from_cols(cols: List[List[float]]):
        return Matrix(cols)

    @staticmethod
    def zeroes(num_rows: int, num_cols: int) -> Matrix:
        return Matrix.from_cols([[0] * num_rows for _ in range(num_cols)])

    @staticmethod
    def identity(dims: int) -> Matrix:
        cols = [[0] * dims for _ in range(dims)]
        for i in range(dims):
            cols[i][i] = 1
        return Matrix.from_cols(cols)

    @staticmethod
    def column_scale(col: List[float], scale: float) -> List[float]:
        return [elem * scale for elem in col]

    @staticmethod
    def column_add(col1: List[float], col2: List[float]) -> List[float]:
        if len(col1) != len(col2):
            raise ValueError("Columns must have same dimension to be added")
        return [a + b for a, b in zip(col1, col2)]

    def __init__(self: Matrix, columns: List[List[float]]):
        self._num_cols = len(columns)
        self._num_rows = len(columns[0])
        for col in columns:
            if len(col) != self.num_rows():
                raise ValueError("Columns must have equal length")
        self.columns = columns

    def copy(self: Matrix) -> Matrix:
        cols = [col[:] for col in self.columns]
        return Matrix.from_cols(cols)

    def size(self: Matrix) -> (int, int):
        return (self._num_rows, self._num_cols)

    def num_rows(self: Matrix) -> int:
        return self._num_rows

    def num_cols(self: Matrix) -> int:
        return self._num_cols

    def get_row(self: Matrix, index: int) -> List[float]:
        if index < 0 or index >= self.num_rows():
            raise ValueError("Index out of bounds")
        return [col[index] for col in self.columns]

    def get_col(self: Matrix, index: int) -> List[float]:
        if index < 0 or index >= self.num_cols():
            raise ValueError("Index out of bounds")
        return self.columns[index]

    def get(self: Matrix, row: int, col: int) -> float:
        if row < 0 or row >= self.num_rows():
            raise ValueError("Index out of bounds")
        if col < 0 or col >= self.num_cols():
            raise ValueError("Index out of bounds")
        return self.columns[col][row]

    def all_cols(self: Matrix) -> List[List[float]]:
        return self.columns

    def transpose(self: Matrix) -> Matrix:
        return Matrix.from_rows(self.columns)

    def multiply_column(self: Matrix, vector: List[float]) -> List[float]:
        if self.num_cols() != len(vector):
            raise ValueError(
                f"Incompatible sizes for multiplication: {self.size()} and {len(vector)}")
        result = [0] * self.num_rows()
        for col, multiplier in zip(self.all_cols(), vector):
            result = Matrix.column_add(
                result, Matrix.column_scale(col, multiplier))
        return result

    def multiply(self: Matrix, other: Matrix) -> Matrix:
        if self.num_cols() != other.num_rows():
            raise ValueError(
                f"Incompatible matrix sizes for multiplication: {self.size()} and {other.size()}")
        result = [self.multiply_column(col) for col in other.all_cols()]
        return Matrix.from_cols(result)

    def frobenius_norm(self: Matrix) -> float:
        sum_sq = 0
        for col in self.columns:
            for elem in col:
                sum_sq += elem * elem
        return math.sqrt(sum_sq)
