import pylinlin.matrix_utils as utils
from pylinlin.matrix import Matrix
import pytest


class TestMatrixUtils:

    def test_lower_triangular(self):
        mat = Matrix.from_cols([[1, 2, 3], [0, 4, 5], [0, 0, 6]])
        utils.assert_lower_triangular(mat)
        with pytest.raises(AssertionError):
            utils.assert_lower_triangular(mat.transpose())

    def test_upper_triangular(self):
        mat = Matrix.from_cols([[1, 0, 0], [2, 3, 0], [4, 5, 6]])
        utils.assert_upper_triangular(mat)
        with pytest.raises(AssertionError):
            utils.assert_upper_triangular(mat.transpose())

    def test_identity_triangular(self):
        identity = Matrix.identity(3)
        utils.assert_upper_triangular(identity)
        utils.assert_lower_triangular(identity)

    def test_rectangular_triangular(self):
        utils.assert_upper_triangular(
            Matrix.from_cols([[4, 0], [1, 2], [3, 4]]))
