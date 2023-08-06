from pylinlin.matrix import Matrix
import pytest


class TestMatrix:

    def test_identity(self):
        identity = Matrix.identity(3)
        assert identity.all_cols() == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    def test_create_fail(self):
        with pytest.raises(ValueError):
            Matrix.from_cols([[1, 2], [3], [5, 6]])
        with pytest.raises(ValueError):
            Matrix.from_rows([[1, 2], [3, 4], [6]])

    def test_create_from_rows(self):
        matrix = Matrix.from_rows([[1, 2], [3, 4], [5, 6]])
        assert matrix.size() == (3, 2)
        assert matrix.get_row(0) == [1, 2]
        assert matrix.get_row(1) == [3, 4]
        assert matrix.get_row(2) == [5, 6]
        assert matrix.get_col(0) == [1, 3, 5]
        assert matrix.get_col(1) == [2, 4, 6]

    def test_create_from_cols(self):
        matrix = Matrix.from_cols([[1, 2], [3, 4], [5, 6]])
        assert matrix.size() == (2, 3)
        assert matrix.get_col(0) == [1, 2]
        assert matrix.get_col(1) == [3, 4]
        assert matrix.get_col(2) == [5, 6]
        assert matrix.get_row(0) == [1, 3, 5]
        assert matrix.get_row(1) == [2, 4, 6]

    def test_matrix_transpose(self):
        matrix = Matrix.from_cols([[1, 2], [3, 4], [5, 6]])
        mat_transpose = matrix.transpose()
        assert matrix.num_rows() == mat_transpose.num_cols()
        assert matrix.num_cols() == mat_transpose.num_rows()
        for i in range(matrix.num_rows()):
            assert matrix.get_row(i) == mat_transpose.get_col(i)
        for i in range(matrix.num_cols()):
            assert matrix.get_col(i) == mat_transpose.get_row(i)

    def test_matrix_multiply(self):
        matrix1 = Matrix.from_cols([[1, 2], [3, 4], [5, 6]])
        matrix2 = Matrix.from_cols([[1, 2, 3], [4, 5, 6]])
        product = matrix1.multiply(matrix2)
        assert product.size() == (2, 2)
        assert product.all_cols() == [[22, 28], [49, 64]]
        product = matrix2.multiply(matrix1)
        assert product.size() == (3, 3)
        assert product.all_cols() == [[9, 12, 15], [19, 26, 33], [29, 40, 51]]

    def test_matrix_multiply_fail(self):
        matrix1 = Matrix.from_cols([[1, 2], [3, 4], [5, 6]])
        with pytest.raises(ValueError):
            matrix1.multiply(matrix1)
