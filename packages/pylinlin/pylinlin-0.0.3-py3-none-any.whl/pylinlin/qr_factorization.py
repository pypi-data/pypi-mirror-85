from pylinlin.matrix import Matrix
from pylinlin.matrix_view import MatrixView
from pylinlin.householder import Householder


def compute_qr_factorization(mat: Matrix) -> (Matrix, Matrix):
    mat = mat.copy()
    q_mat = Matrix.identity(mat.num_rows())
    iterations = min(mat.num_rows(), mat.num_cols())
    householders = []
    for iteration in range(iterations):
        col = mat.get_col(iteration)
        hh = Householder(col[iteration:])
        householders.append((iteration, hh))
        mat = hh.multiply_left(mat, pad_top=iteration)
    for iteration, hh in householders[::-1]:
        q_mat = hh.multiply_left(q_mat, pad_top=iteration)
    return (q_mat, mat)
