from .matrix import Matrix
from .matrix_view import MatrixView


def compute_lu_factorization(mat: Matrix) -> (Matrix, Matrix):
    # do not overwrite original matrix
    mat = mat.copy()
    mat_l = Matrix.identity(mat.num_rows())
    mat_u = Matrix.zeroes(mat.num_rows(), mat.num_cols())

    iterations = min(mat.num_rows(), mat.num_cols())

    for iteration in range(iterations):

        pivot = mat.get(iteration, iteration)

        # u11 = a11
        MatrixView.with_size(
            mat_u, (iteration, iteration), (1, 1)
        ).set_element(0, 0, pivot)

        # u12 = a12
        if iteration != mat_u.num_cols() - 1:
            MatrixView(
                mat_u,
                (iteration, iteration + 1),
                (iteration, mat_u.num_cols() - 1)
            ).set(MatrixView(
                mat,
                (iteration, iteration + 1),
                (iteration, mat.num_cols() - 1)))

        # l11 = 1
        MatrixView.with_size(
            mat_l, (iteration, iteration),
            (1, 1)
        ).set_element(0, 0, 1)

        # l21 = a21 / pivot
        if iteration != mat_l.num_rows() - 1:
            if pivot == 0:
                raise ValueError(
                    "Pivoting required for computing LU for this matrix")
            MatrixView(
                mat_l,
                (iteration + 1, iteration),
                (mat_l.num_rows() - 1, iteration)
            ).scale_add(MatrixView(
                mat,
                (iteration + 1, iteration),
                (mat.num_rows() - 1, iteration)), 1 / pivot)

        if iteration != mat_l.num_rows() - 1 and iteration != mat_u.num_cols() - 1:
            # Extract as matrix to perform multiplication
            l21 = MatrixView(
                mat_l,
                (iteration + 1, iteration),
                (mat_l.num_rows() - 1, iteration)
            ).to_matrix()
            u12 = MatrixView(
                mat_u,
                (iteration, iteration + 1),
                (iteration, mat_u.num_cols() - 1)
            ).to_matrix()
            update = l21.multiply(u12)
            # Rank-one update: A22 - l21 * u12
            MatrixView.to_end(
                mat, (iteration + 1, iteration + 1)
            ).scale_add(
                MatrixView.to_end(update, (0, 0)),
                -1
            )

    return mat_l, mat_u
