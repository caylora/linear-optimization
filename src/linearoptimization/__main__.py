"""Main entrypoint for the program."""

import linearoptimization as lo

import numpy as np

MAX_N, MAX_M = 1001, 1001
A = np.empty((MAX_M, MAX_N))  # Matrix of coefficients of constraints
b = np.empty(MAX_M)  # Vector of constraint values
c = np.empty(MAX_N, np.double)  # Vector of objective function variables
v = 0  # Constant
N = np.empty(MAX_N, np.intc)  # Nonbasic variables
B = np.empty(MAX_M, np.intc)  # Basic variables

# Define the parameters of the problem:
variables, contraints = 2, 2  # Number of variables, constraints
# A[0, 0], A[0, 1], A[0, 2] = -2, -3, -1
# A[1, 0], A[1, 1], A[1, 2] = -4, -1, -2
# A[2, 0], A[2, 1], A[2, 2] = -3, -4, -2
# b[0], b[1], b[2] = 5, 11, 8
# c[0], c[1], c[2] = 5, 4, 3

# infeasible example
A[0][0], A[0][1] = -1, -1
A[1][0], A[1][1] = 2, 2
b[0], b[1] = 2, -10
c[0], c[1] = 3, -2

# Pass the parameters to the solving algorithm
lo.run(variables, contraints, A, b, c, v, N, B)
