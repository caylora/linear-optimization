"""Main entrypoint for the program."""

import linearoptimization as lo

import numpy as np

variables, contraints = 3, 3  # Number of variables, constraints
A = np.zeros(
    (contraints, variables), np.double
)  # Matrix of coefficients of constraints
b = np.zeros(contraints, np.double)  # Vector of constraint values
c = np.zeros(variables, np.double)  # Vector of objective function variables
v = 0  # Constant

# Define the parameters of the problem:
A[0, 0], A[0, 1], A[0, 2] = -2, -3, -1
A[1, 0], A[1, 1], A[1, 2] = -4, -1, -2
A[2, 0], A[2, 1], A[2, 2] = -3, -4, -2
b[0], b[1], b[2] = 5, 11, 8
c[0], c[1], c[2] = 5, 4, 3

# Pass the parameters to the solving algorithm
lo.run(variables, contraints, A, b, c, v)
