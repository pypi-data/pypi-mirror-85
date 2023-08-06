from __future__ import annotations
from typing import List
from .matrix import Matrix
from .matrix_view import MatrixView


class Householder:
    def __init__(self: Householder, vec: List[float]):
        # Reflects vec to e0 * ||vec||
        e0 = Matrix.zeroes(len(vec), 1)
        MatrixView(e0, (0, 0), (0, 0)).set_element(0, 0, 1)
        mat = Matrix.from_cols([vec[:]])
        norm = mat.frobenius_norm()
        MatrixView.to_end(mat, (0, 0)).scale_add(e0, -norm)
        norm2 = mat.frobenius_norm()
        MatrixView.to_end(mat, (0, 0)).scale(1 / norm2)
        self.base = mat

    def multiply_left(self: Householder, mat: Matrix, pad_top: int = 0) -> Matrix:
        cols = []
        all_cols = mat.all_cols()
        for col in all_cols[:pad_top]:
            cols.append(col[:])
        for col in all_cols[pad_top:]:
            cols.append(self.multiply_left_column(col, pad_top))
        return Matrix.from_cols(cols)

    def multiply_left_column(self: Householder, vec: List[float], pad_top: int = 0) -> List[float]:
        # (Ix - 2uuTx)
        full_x = Matrix.from_cols([vec[:]])
        x = Matrix.from_cols([vec[pad_top:]])
        factor = self.base.transpose().multiply(x)
        factor = factor.get(0, 0)
        MatrixView.to_end(full_x, (pad_top, 0)).scale_add(
            MatrixView.to_end(self.base, (0, 0)),
            -2 * factor
        )
        return full_x.get_col(0)

    def multiply_right(self: Householder, mat: Matrix) -> Matrix:
        pass

    def to_matrix(self: Householder) -> Matrix:
        householder_mat = Matrix.identity(self.base.num_rows())
        update = self.base.multiply(self.base.transpose())
        MatrixView.to_end(householder_mat, (0, 0)).scale_add(update, -2)
        return householder_mat
