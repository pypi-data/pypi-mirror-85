from pylinlin.matrix import Matrix
from pylinlin.matrix_view import MatrixView
from pylinlin.householder import Householder


def compute_qr_factorization(mat: Matrix) -> (Matrix, Matrix):
    # Do not overwrite original matrix
    mat = mat.copy()
    householders = []  # store householder transformations
    iterations = min(mat.num_rows(), mat.num_cols())
    for iteration in range(iterations):
        col = mat.get_col(iteration)
        # Zero out the entries below the diagonal
        hh = Householder(col[iteration:])
        householders.append((iteration, hh))
        mat = hh.multiply_left(mat, pad_top=iteration)
    # Accumulate the householder transformations
    q_mat = Matrix.identity(mat.num_rows())
    for iteration, hh in householders[::-1]:
        q_mat = hh.multiply_left(q_mat, pad_top=iteration)
    return (q_mat, mat)
