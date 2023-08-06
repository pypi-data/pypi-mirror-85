import pytest
from pylinlin.givens import Givens
from pylinlin.matrix import Matrix
import pylinlin.matrix_utils as utils
import math


class TestGivens:

    def test_givens_rotation(self):
        givens = Givens(1, 1)
        product = givens.multiply_left(Matrix.from_cols([[1, 1]]))
        assert product.size() == (2, 1)
        assert product.get_col(0) == pytest.approx([math.sqrt(2), 0])
        product = givens.multiply_left_column([1, 1])
        assert product.size() == (2, 1)
        assert product.get_col(0) == pytest.approx([math.sqrt(2), 0])

    def test_givens_padded(self):
        givens = Givens(-0.8, 0.6)
        product = givens.multiply_left(
            Matrix.from_cols([[1, 2, -0.8, 0.6]]), 2)
        assert product.size() == (4, 1)
        assert product.get_col(0) == pytest.approx([1, 2, 1, 0])

    def test_givens_matrix(self):
        givens = Givens(1, 1).to_matrix()
        product = givens.multiply(Matrix.from_cols([[1, 1]]))
        assert product.size() == (2, 1)
        assert product.get_col(0) == pytest.approx([math.sqrt(2), 0])

    def test_givens_inverse(self):
        givens = Givens(1, 1).to_matrix()
        product = givens.transpose().multiply(givens)
        utils.assert_matrix_equal(product, Matrix.identity(2))
