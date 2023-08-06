from __future__ import annotations
from typing import List
from .matrix import Matrix
from .matrix_view import MatrixView
import math


class Givens:
    def __init__(self: Givens, x1: float, x2: float):
        # G * (x1, x2) = (||x||, 0)
        magnitude = math.sqrt(x1 * x1 + x2 * x2)
        self.x1 = x1 / magnitude
        self.x2 = x2 / magnitude
        self.matrix = Matrix.from_cols(
            [[self.x1, -self.x2], [self.x2, self.x1]])

    def transpose(self: Givens) -> Givens:
        return Givens(self.x1, -self.x2)

    def multiply_left(self: Givens, mat: Matrix, pad_top: int = 0):
        mat = mat.copy()
        affected = MatrixView(
            mat, (pad_top, 0), (pad_top + 1, mat.num_cols() - 1))
        extracted = affected.to_matrix()
        product = self.matrix.multiply(extracted)
        affected.set(MatrixView.whole(product))
        return mat

    def multiply_left_column(self: Givens, vec: List[float], pad_top: int = 0) -> Matrix:
        mat = Matrix.from_cols([vec])
        affected = MatrixView.with_size(mat, (pad_top, 0), (2, 1))
        extracted = affected.to_matrix()
        product = self.matrix.multiply(extracted)
        affected.set(MatrixView.whole(product))
        return mat

    def multiply_right(self: Givens, mat: Matrix, pad_top: int = 0):
        mat = mat.copy()
        affected = MatrixView(
            mat, (0, pad_top), (mat.num_rows() - 1, pad_top + 1))
        extracted = affected.to_matrix()
        product = extracted.multiply(self.matrix)
        affected.set(MatrixView.whole(product))
        return mat

    def to_matrix(self: Givens, pad_top: int = 0, dims: int = 2):
        mat = Matrix.identity(dims)
        MatrixView.with_size(mat, (pad_top, pad_top), (2, 2)).set(
            MatrixView.whole(self.matrix))
        return mat
