from .matrix import Matrix
from typing import List


def is_upper_triangular(mat: Matrix) -> bool:
    for index, col in enumerate(mat.all_cols()):
        for elem in col[index + 1:]:
            if elem != 0:
                return False
    return True


def is_lower_triangular(mat: Matrix) -> bool:
    for index, col in enumerate(mat.all_cols()):
        for elem in col[:index]:
            if elem != 0:
                return False
    return True


def extract_diagonal(mat: Matrix) -> List[float]:
    result = [0] * min(mat.num_rows(), mat.num_cols())
    for i in range(min(mat.num_rows(), mat.num_cols())):
        result[i] = mat.get(i, i)
    return result
