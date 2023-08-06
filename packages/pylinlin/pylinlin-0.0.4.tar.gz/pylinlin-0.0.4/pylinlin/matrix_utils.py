from .matrix import Matrix
from typing import List
import pytest


def assert_orthonormal(mat: Matrix):
    assert_square(mat)
    # qTq should be the identity
    qTq = mat.transpose().multiply(mat)
    for index, col in enumerate(qTq.all_cols()):
        for elem in col[:index]:
            assert elem == pytest.approx(0)
        assert col[index] == pytest.approx(1)
        for elem in col[index+1:]:
            assert elem == pytest.approx(0)


def assert_matrix_equal(mat1: Matrix, mat2: Matrix):
    assert mat1.size() == mat2.size()
    for col1, col2 in zip(mat1.all_cols(), mat2.all_cols()):
        assert col1 == pytest.approx(col2)


def assert_square(mat: Matrix):
    assert mat.num_rows() == mat.num_cols()


def assert_upper_triangular(mat: Matrix):
    for index, col in enumerate(mat.all_cols()):
        for elem in col[index + 1:]:
            assert elem == pytest.approx(0)
    return True


def assert_lower_triangular(mat: Matrix):
    for index, col in enumerate(mat.all_cols()):
        for elem in col[:index]:
            assert elem == pytest.approx(0)
    return True


def extract_diagonal(mat: Matrix) -> List[float]:
    result = [0] * min(mat.num_rows(), mat.num_cols())
    for i in range(min(mat.num_rows(), mat.num_cols())):
        result[i] = mat.get(i, i)
    return result
