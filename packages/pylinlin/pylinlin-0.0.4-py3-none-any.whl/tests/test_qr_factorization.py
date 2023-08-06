from pylinlin.qr_factorization import compute_qr_factorization
from pylinlin.matrix import Matrix
import pytest
import pylinlin.matrix_utils as utils


class TestQRFactorization:

    def check_qr_factorization(self, mat: Matrix):
        q, r = compute_qr_factorization(mat)
        print(r.all_cols())
        utils.assert_orthonormal(q)
        utils.assert_upper_triangular(r)
        product = q.multiply(r)
        for col1, col2 in zip(product.all_cols(), mat.all_cols()):
            assert col1 == pytest.approx(col2)

    def test_qr_factorization(self):
        mat = Matrix.from_cols([[1, 2, 3], [4, 5, 6], [7, 8, 10]])
        self.check_qr_factorization(mat)

    def test_qr_factorization_more_rows(self):
        mat = Matrix.from_cols([[1, 2, 3, 5], [4, 5, 6, 8], [7, 8, 10, 1]])
        self.check_qr_factorization(mat)

    def test_qr_factorization_more_cols(self):
        mat = Matrix.from_cols([[1, 2, 3], [4, 5, 6], [7, 8, 10], [-1, 0, 0]])
        self.check_qr_factorization(mat)
