from __future__ import annotations
from .matrix import Matrix


class MatrixView:
    def __init__(self: MatrixView, mat: Matrix, start: (int, int), end: (int, int)):
        self.mat = mat
        if start[0] < 0 or start[0] >= mat.num_rows():
            raise ValueError("Row index out of bounds")
        if start[1] < 0 or start[1] >= mat.num_cols():
            raise ValueError("Col index out of bounds")
        self.start = start
        if end[0] < 0 or end[0] >= mat.num_rows() or end[0] < start[0]:
            raise ValueError("Row index out of bounds")
        if end[1] < 0 or end[1] >= mat.num_cols() or end[1] < start[1]:
            raise ValueError("Col index out of bounds")
        self.end = end  # inclusive
        self._size = (self.end[0] - self.start[0] + 1,
                      self.end[1] - self.start[1] + 1)

    @staticmethod
    def with_size(mat: Matrix, start: (int, int), size: (int, int)):
        return MatrixView(mat, start, (start[0] + size[0] - 1, start[1] + size[1] - 1))

    @staticmethod
    def to_end(mat: Matrix, start: (int, int)):
        sz = mat.size()
        return MatrixView(mat, start, (sz[0] - 1, sz[1] - 1))

    def size(self: MatrixView) -> (int, int):
        return self._size

    def to_matrix(self: MatrixView) -> Matrix:
        sz = self.size()
        cols = [[0] * sz[0] for _ in range(sz[1])]
        for col_index in range(sz[1]):
            for row_index in range(sz[0]):
                cols[col_index][row_index] = self.get(row_index, col_index)
        return Matrix.from_cols(cols)

    def set(self: MatrixView, other: MatrixView):
        if self.size() != other.size():
            raise ValueError("Sizes must match to set values")
        sz = self.size()
        for col_index in range(sz[1]):
            for row_index in range(sz[0]):
                self.set_element(row_index, col_index,
                                 other.get(row_index, col_index))

    def scale_add(self: MatrixView, other: MatrixView, factor: int = 1):
        if self.size() != other.size():
            raise ValueError("Sizes must match to set values")
        sz = self.size()
        for col_index in range(sz[1]):
            for row_index in range(sz[0]):
                self.set_element(
                    row_index, col_index,
                    self.get(row_index, col_index) + factor * other.get(row_index, col_index))

    def scale(self: MatrixView, scale: float):
        sz = self.size()
        for col_index in range(sz[1]):
            for row_index in range(sz[0]):
                self.set_element(
                    row_index, col_index,
                    float * self.get(row_index, col_index))

    def set_element(self: MatrixView, row: int, col: int, value: float):
        sz = self.size()
        if row < 0 or row >= sz[0]:
            raise ValueError("Index out of bounds")
        if col < 0 or col >= sz[1]:
            raise ValueError("Index out of bounds")
        self.mat.columns[col + self.start[1]][row + self.start[0]] = value

    def get(self: MatrixView, row: int, col: int):
        sz = self.size()
        if row < 0 or row >= sz[0]:
            raise ValueError("Index out of bounds")
        if col < 0 or col >= sz[1]:
            raise ValueError("Index out of bounds")
        return self.mat.columns[col + self.start[1]][row + self.start[0]]
