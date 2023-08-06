from pylinlin.matrix import Matrix
from pylinlin.lu_factorization import compute_lu_factorization
import pylinlin.matrix_utils as utils


class TestLUFactorization:

    def vector_all(self, vector, value):
        for elem in vector:
            if elem != value:
                return False
        return True

    def test_lu(self):
        matrix = Matrix.from_cols([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        mat_l, mat_u = compute_lu_factorization(matrix)
        assert utils.is_lower_triangular(mat_l)
        assert utils.is_upper_triangular(mat_u)
        assert self.vector_all(utils.extract_diagonal(mat_l), 1)
        product = mat_l.multiply(mat_u)
        assert product.all_cols() == matrix.all_cols()

    def test_lu_more_cols(self):
        matrix = Matrix.from_cols(
            [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
        mat_l, mat_u = compute_lu_factorization(matrix)
        assert utils.is_lower_triangular(mat_l)
        assert utils.is_upper_triangular(mat_u)
        assert self.vector_all(utils.extract_diagonal(mat_l), 1)
        product = mat_l.multiply(mat_u)
        assert product.all_cols() == matrix.all_cols()

    def test_lu_more_rows(self):
        mat_l = Matrix.from_cols([
            [1, 2, 3, 4, 5],
            [0, 1, 2, 3, 4],
            [0, 0, 1, 2, 3],
            [0, 0, 0, 1, 2],
            [0, 0, 0, 0, 1]])
        mat_u = Matrix.from_cols([
            [5, 1, 2, 3, 4],
            [0, 4, 3, 2, 1],
            [0, 0, 2, 1, 0]])
        matrix = mat_l.multiply(mat_u)
        mat_l, mat_u = compute_lu_factorization(matrix)
        # note LU factorization is not unique therefore we are not comparing L and U
        assert utils.is_lower_triangular(mat_l)
        assert utils.is_upper_triangular(mat_u)
        assert self.vector_all(utils.extract_diagonal(mat_l), 1)
        product = mat_l.multiply(mat_u)
        assert product.all_cols() == matrix.all_cols()
