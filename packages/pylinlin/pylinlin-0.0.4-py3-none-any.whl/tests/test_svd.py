import pytest
from pylinlin.matrix import Matrix
from pylinlin.matrix_view import MatrixView
import pylinlin.matrix_utils as utils
from pylinlin.svd import \
    compute_svd, \
    reduce_to_bidiagonal, \
    compute_svd_bidiagonal


class TestSVD:

    def test_reduce_to_bidiagonal(self):
        mat = Matrix.from_cols([[1, 2, 3], [4, 5, 6], [7, 8, 10]])
        b, _, _ = reduce_to_bidiagonal(mat)
        utils.assert_upper_triangular(b)
        truncated = MatrixView.with_size(
            b, (0, 1), (mat.num_rows() - 1, mat.num_cols() - 1)
        ).to_matrix()
        utils.assert_lower_triangular(truncated)

    def test_bidiagonal_recreate(self):
        mat = Matrix.from_cols([[1, 2, 3], [4, 5, 6], [7, 8, 10]])
        b, left, right = reduce_to_bidiagonal(mat)
        for index, hh in list(enumerate(left))[::-1]:
            b = hh.multiply_left(b, index)
        for index, hh in list(enumerate(right))[::-1]:
            b = hh.multiply_right(b, index + 1)
        utils.assert_matrix_equal(mat, b)

    def test_bidiagonal_recreate_2(self):
        mat = Matrix.from_cols([[1, 2, 3], [2, 5, 1], [-1, 3, -2]])
        b, left, right = reduce_to_bidiagonal(mat)
        for index, hh in list(enumerate(left))[::-1]:
            b = hh.multiply_left(b, index)
        for index, hh in list(enumerate(right))[::-1]:
            b = hh.multiply_right(b, index + 1)
        utils.assert_matrix_equal(mat, b)

    def test_svd_bidiagonal(self):
        mat = Matrix.from_cols([[1, 0, 0], [2, 3, 0], [0, 4, 5]])
        u, s, v = compute_svd_bidiagonal(mat)
        utils.assert_orthonormal(u)
        utils.assert_orthonormal(v)
        product = u.multiply(s)
        product = product.multiply(v.transpose())
        product.print()
        utils.assert_matrix_equal(mat, product)

    def test_svd_bidiagonal_2(self):
        mat = Matrix.from_cols(
            [[3.742, 0, 0], [4.018, 3.511, 0], [0, -3.408, -1.979]])
        u, s, v = compute_svd_bidiagonal(mat)
        utils.assert_orthonormal(u)
        utils.assert_orthonormal(v)
        product = u.multiply(s)
        product = product.multiply(v.transpose())
        product.print()
        utils.assert_matrix_equal(mat, product)

    def test_svd_square(self):
        mat = Matrix.from_cols([[1, 2, 3], [2, 5, 1], [-1, 3, -2]])
        u, s, v = compute_svd(mat)
        u.transpose().multiply(u).print()
        utils.assert_orthonormal(u)
        utils.assert_orthonormal(v)
        product = u.multiply(s)
        product = product.multiply(v.transpose())
        mat.print()
        product.print()
        utils.assert_matrix_equal(mat, product)

    def test_svd_more_rows(self):
        mat = Matrix.from_cols([[1, 2, 3, 1], [2, 5, 1, 0], [-1, 3, -2, -2]])
        u, s, v = compute_svd(mat)
        u.transpose().multiply(u).print()
        utils.assert_orthonormal(u)
        utils.assert_orthonormal(v)
        product = u.multiply(s)
        product = product.multiply(v.transpose())
        mat.print()
        product.print()
        utils.assert_matrix_equal(mat, product)

    def test_svd_more_cols(self):
        mat = Matrix.from_cols([[1, 2, 3], [2, 5, 1], [-1, 3, -2], [3, 2, 1]])
        u, s, v = compute_svd(mat)
        u.transpose().multiply(u).print()
        utils.assert_orthonormal(u)
        utils.assert_orthonormal(v)
        product = u.multiply(s)
        product = product.multiply(v.transpose())
        mat.print()
        product.print()
        utils.assert_matrix_equal(mat, product)
