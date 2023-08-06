from pylinlin.householder import Householder
from pylinlin.matrix import Matrix
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
