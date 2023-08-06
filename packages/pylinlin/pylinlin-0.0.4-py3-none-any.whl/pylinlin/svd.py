from pylinlin.matrix import Matrix
from pylinlin.matrix_view import MatrixView
from pylinlin.householder import Householder
from pylinlin.qr_factorization import compute_qr_factorization
from pylinlin.givens import Givens
import pylinlin.matrix_utils as utils
from typing import List


def reduce_to_bidiagonal(mat: Matrix) -> (Matrix, List[Householder], List[Householder]):
    mat = mat.copy()
    if mat.num_rows() != mat.num_cols():
        raise ValueError("Matrix should be square")
    iterations = mat.num_rows() - 1
    acc_left = []
    acc_right = []
    for iteration in range(iterations):
        # clear zeroes below diagonal
        col = mat.get_col(iteration)[iteration:]
        householder_left = Householder(col)
        mat = householder_left.multiply_left(mat, pad_top=iteration)
        acc_left.append(householder_left)
        if iteration != iterations - 1:
            # clear zeroes above superdiagonal
            row = mat.get_row(iteration)[iteration + 1:]
            householder_right = Householder(row)
            mat = householder_right.multiply_right(mat, pad_top=iteration + 1)
            acc_right.append(householder_right)
    return mat, acc_left, acc_right


def compute_svd_bidiagonal(mat: Matrix) -> (Matrix, Matrix, Matrix):
    mat.print()
    dims = mat.num_cols()
    u = Matrix.identity(dims)
    v = Matrix.identity(dims)
    for _ in range(50):
        # while not converged

        # introduce the bulge
        givens = Givens(mat.get(0, 0) ** 2 - mat.get(dims - 1, dims - 1) ** 2 - mat.get(dims - 2, dims - 1) ** 2,
                        mat.get(0, 1) * mat.get(0, 0)).transpose()
        mat = givens.multiply_right(mat)
        v = givens.transpose().multiply_left(v)

        # chase the bulge
        for iteration in range(0, dims - 1):
            # zero subdiagonal
            givens_lower = Givens(
                mat.get(iteration, iteration),
                mat.get(iteration + 1, iteration))
            mat = givens_lower.multiply_left(
                mat, pad_top=iteration)
            u = givens_lower.transpose().multiply_right(
                u, pad_top=iteration)
            # zero above superdiagonal
            if iteration != dims - 2:
                givens_upper = Givens(
                    mat.get(iteration, iteration + 1),
                    mat.get(iteration, iteration + 2)).transpose()
                mat = givens_upper.multiply_right(
                    mat, pad_top=iteration + 1)
                v = givens_upper.transpose().multiply_left(
                    v, pad_top=iteration + 1)
    mat.print()
    # reorder column
    v = v.transpose()
    return u, mat, v


def compute_svd(mat: Matrix) -> (Matrix, Matrix, Matrix):
    if mat.num_cols() > mat.num_rows():
        u, s, v = compute_svd(mat.transpose())
        return v, s.transpose(), u
    elif mat.num_rows() > mat.num_cols():
        # mat is m x n, m > n
        # q should be m x m, r should be m x n
        q, r = compute_qr_factorization(mat)
        # truncate r to be n x n, truncate q to be m x n
        r_truncated = MatrixView.with_size(
            r, (0, 0), (mat.num_cols(), mat.num_cols())).to_matrix()
        r_truncated.print()
        u, s, v = compute_svd(r_truncated)
        u_padded = Matrix.identity(mat.num_rows())
        MatrixView.with_size(
            u_padded, (0, 0), (mat.num_cols(), mat.num_cols())
        ).set(MatrixView.whole(u))
        u = q.multiply(u_padded)
        s_padded = Matrix.zeroes(mat.num_rows(), mat.num_cols())
        MatrixView.with_size(
            s_padded, (0, 0), (mat.num_cols(), mat.num_cols())
        ).set(MatrixView.whole(s))
        s = s_padded
        return u, s, v
    else:
        # matrix is square
        b, left, right = reduce_to_bidiagonal(mat)
        u, s, v = compute_svd_bidiagonal(b)
        for index, hh in list(enumerate(left))[::-1]:
            u = hh.multiply_left(u, index)
        v_transpose = v.transpose()
        for index, hh in list(enumerate(right))[::-1]:
            v_transpose = hh.multiply_right(v_transpose, index + 1)
        return u, s, v_transpose.transpose()
