from .matrix import Matrix
from typing import List
import pytest


def assert_square(mat: Matrix):
    assert mat.num_rows() == mat.num_cols()


def assert_upper_triangular(mat: Matrix) -> bool:
    for index, col in enumerate(mat.all_cols()):
        for elem in col[index + 1:]:
            assert elem == pytest.approx(0)
    return True


def assert_lower_triangular(mat: Matrix) -> bool:
    for index, col in enumerate(mat.all_cols()):
        for elem in col[:index]:
            assert elem == pytest.approx(0)
    return True


def extract_diagonal(mat: Matrix) -> List[float]:
    result = [0] * min(mat.num_rows(), mat.num_cols())
    for i in range(min(mat.num_rows(), mat.num_cols())):
        result[i] = mat.get(i, i)
    return result
