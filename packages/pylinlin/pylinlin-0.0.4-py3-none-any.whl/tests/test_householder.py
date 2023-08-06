from pylinlin.householder import Householder
from pylinlin.matrix import Matrix
import pylinlin.matrix_utils as utils
import pytest


class TestHouseholder:

    def test_householder(self):
        vec = [5, 4, 3, 2, 1]
        householder = Householder(vec)
        householder_mat = householder.to_matrix()
        vec_as_mat = Matrix.from_cols([vec])
        product = householder_mat.multiply(vec_as_mat)
        assert product.num_cols() == 1
        assert product.get(0, 0) == pytest.approx(vec_as_mat.frobenius_norm())
        for elem in product.get_col(0)[1:]:
            assert elem == pytest.approx(0)

    def test_householder_symmetric(self):
        vec = [5, 4, 3, 2, 1]
        householder = Householder(vec)
        householder_mat = householder.to_matrix()
        utils.assert_matrix_equal(householder_mat, householder_mat.transpose())

    def test_householder_inverse(self):
        vec = [5, 4, 3, 2, 1]
        householder = Householder(vec)
        householder_mat = householder.to_matrix()
        product = householder_mat.multiply(householder_mat)
        utils.assert_matrix_equal(product, Matrix.identity(5))

    def test_householder_col(self):
        vec = [5, 4, 3, 2, 1]
        householder = Householder(vec)
        vec_as_mat = Matrix.from_cols([vec])
        product = householder.multiply_left(vec_as_mat)
        assert product.num_cols() == 1
        assert product.get(0, 0) == pytest.approx(vec_as_mat.frobenius_norm())
        for elem in product.get_col(0)[1:]:
            assert elem == pytest.approx(0)

    def test_householder_row(self):
        vec = [5, 4, 3, 2, 1]
        householder = Householder(vec)
        row_matrix = Matrix.from_rows([vec])
        product = householder.multiply_right(row_matrix)
        assert product.num_rows() == 1
        assert product.get(0, 0) == pytest.approx(row_matrix.frobenius_norm())
        for elem in product.get_row(0)[1:]:
            assert elem == pytest.approx(0)
