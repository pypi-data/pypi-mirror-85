import numpy as np

from sparse_uls.util import linear_subspace, least_p, glpk_linprog


def solve(A: np.ndarray, b: np.ndarray, p: float = 1.0) -> np.ndarray:
    '''
    Minimizer of ||x||_p^p
    Given Ax=b
    '''
    if len(A.shape) != 2 or len(b.shape) != 1:
        raise Exception("A must be 2D, b must be 1D")

    if p == 1:
        return solve_1(A, b)

    x_, Q2 = linear_subspace(A, b)
    z = least_p(Q2, x_, p)
    x = Q2.__matmul__(z).__add__(x_)
    return x


def solve_1(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    '''
    Minimizer of ||Ax+b||_1 using linear programming
    '''
    if len(A.shape) != 2 or len(b.shape) != 1:
        raise Exception("A must be 2D, b must be 1D")

    m, n = A.shape

    A_ = np.empty(shape=(2 * n, 2 * n))
    A_[0:n, 0:n] = +np.identity(n)
    A_[n:2 * n, 0:n] = -np.identity(n)
    A_[0:n, n:2 * n] = -np.identity(n)
    A_[n:2 * n, n:2 * n] = -np.identity(n)
    b_ub = np.zeros(shape=(2 * n))

    c = np.empty(shape=(2 * n))
    c[0:n] = 0
    c[n:2 * n] = 1

    A_eq = np.empty(shape=(m, 2 * n))
    A_eq[:, 0:n] = A
    A_eq[:, n:2 * n] = 0
    b_eq = b

    x1 = glpk_linprog(
        c=c,
        A=A_,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
    )
    return x1[0:n]
