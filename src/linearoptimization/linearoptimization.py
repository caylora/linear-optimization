"""Code to support simplex method optimization."""

import numpy as np


def pivot(x, y):
    """Pivot yth variable around xth constraint"""
    global n, m, A, b, c, v, N, B
    print(f"Pivoting variable {y} around constraint {x}.")
    # Rearrange row x
    for j in range(n):
        if j != y:
            A[x, j] /= -A[x, y]
    b[x] /= -A[x, y]
    A[x, y] = 1.0 / A[x, y]

    # Rearrange other rows
    for i in range(m):
        if i != x:
            for j in range(n):
                if j != y:
                    A[i, j] += A[i, y] * A[x, j]
            b[i] += A[i, y] * b[x]
            A[i, y] *= A[x, y]

    # Rearrange objective function
    for j in range(n):
        if j != y:
            c[j] += c[y] * A[x, j]
    v += c[y] * b[x]
    c[y] *= A[x, y]

    # Swap basic and nonbasic variable
    B[x], N[y] = N[y], B[x]


def iterate_simplex():
    """Run a single iteration of the simplex algorithm,
    Returns 0 if OK, 1 if STOP, -1 if UNBOUNDED."""
    global n, m, A, b, c, v, N, B
    print("--------------------")
    print("State:")
    print("Maximize: ", end="")
    global n
    for j in range(n):
        print(f"{c[j]}x_{N[j]} + ", end="")
    print(f"{v}")
    print("Subject to:")
    for i in range(m):
        for j in range(n):
            print(f"{A[i, j]}x_{N[j]} + ", end="")
        print(f"{b[i]} = x_{B[i]}")
    ind = -1
    best_var = -1
    for j in range(n):
        if c[j] > 0:
            if best_var == -1 or N[j] < ind:
                ind = N[j]
                best_var = j
    if ind == -1:
        return 1
    max_constr = float("inf")
    best_constr = -1
    for i in range(m):
        if A[i, best_var] < 0:
            curr_constr = -b[i] / A[i, best_var]
            if curr_constr < max_constr:
                max_constr = curr_constr
                best_constr = i
    if max_constr == float("inf"):
        return -1
    pivot(best_constr, best_var)
    return 0


def initialize_simplex():
    """Tries to convert the LP into slack form with feasible basic solution,
    Returns 0 if OK, -1 if INFEASIBLE."""
    global n, m, A, b, c, v, N, B
    k = -1
    min_b = -1
    for i in range(m):
        if k == -1 or b[i] < min_b:
            k = i
            min_b = b[i]
    if b[k] >= 0:  # basic solution feasible
        for j in range(n):
            N[j] = j
        for i in range(m):
            B[i] = n + i
        return 0
    # Generate auxiliary LP
    n += 1
    for j in range(n):
        N[j] = j
    for i in range(m):
        B[i] = n + i
    # Store the objective function
    c_old = c
    v_old = v
    # Aux. objective function
    c[n - 1] = -1
    for j in range(n):
        c[j] = 0
    v = 0
    # Aux. coefficients
    for i in range(m):
        A[i, n - 1] = 1
    # Perform initial pivot
    pivot(k, n - 1)
    # Solve aux. LP
    code = 0
    while code == 0:
        code = iterate_simplex()
    assert code == 1  # aux lp cant be unbounded
    if v != 0:
        return -1  # infeasible
    z_basic = -1
    for i in range(m):
        if B[i] == n - 1:
            z_basic = i
            break
    # If x_n basic, perform 1 degen pivot to make it nonbasic
    if z_basic != -1:
        pivot(z_basic, n - 1)
    z_nonbasic = -1
    for j in range(n):
        if N[j] == n - 1:
            z_nonbasic = j
            break
    assert z_nonbasic != -1
    for i in range(m):
        A[i, z_nonbasic] = A[i, n - 1]
    N[z_nonbasic], N[n - 1] = N[n - 1], N[z_nonbasic]
    n -= 1
    for j in range(n):
        if N[j] > n:
            N[j] -= 1
    for i in range(m):
        if B[i] > n:  # should this be m? idk
            B[i] -= 1

    for j in range(n):
        c[j] = 0
    v = v_old

    for j in range(n):
        ok = False
        for jj in range(n):
            if j == N[jj]:
                c[jj] += c_old[j]
                ok = True
                break
        if ok:
            continue
        for i in range(m):
            if j == B[i]:
                for jj in range(n):
                    c[jj] += c_old[j] * A[i, jj]
                v += c_old[j] * b[i]
                break
    return 0


def simplex():
    """Runs the simplex algorithm to optimize the LP,
    Returns vector of -1s if unbounded, -2s if infeasible."""
    global n, m, A, b, c, v, N, B
    if initialize_simplex() == -1:
        return (np.full(n + m, -2), np.inf)
    code = 0
    while code == 0:
        code = iterate_simplex()
    if code == -1:
        return (np.full(n + m, -1), np.inf)
    ret = np.zeros(n + m)
    for j in range(n):
        ret[N[j]] = 0
    for i in range(m):
        ret[B[i]] = b[i]
    return (ret, v)


def run(
    variables,
    constraints,
    constr_coeff_matrix,
    constr_value_vector,
    objfunc_coeff_vector,
    constant,
):
    """Main entrypoint for the code."""
    global n, m, A, b, c, v, N, B

    n, m = variables, constraints  # Number of variables, constraints
    A = constr_coeff_matrix  # Matrix of coefficients of constraints
    b = constr_value_vector  # Vector of constraint values
    c = objfunc_coeff_vector  # Vector of objective function variables
    v = constant  # Constant
    N = np.zeros(n, np.intc)  # Nonbasic variables
    B = np.zeros(m, np.intc)  # Basic variables

    ret = simplex()
    if ret[1] == np.inf:
        if ret[0][0] == -1:
            print("Objective function unbounded!\n")
        elif ret[0][0] == -2:
            print("Linear program infeasible!\n")
    else:
        print("Solution: (", end="")
        for i in range(n + m):
            st = ", " if i < n + m - 1 else ")\n"
            print(f"{ret[0][i]}{st}", end="")
        print(f"Optimal objective value: {ret[1]}\n")
