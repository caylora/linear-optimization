"""Main entrypoint for the program."""

import linearoptimization as lo
import numpy as np
import csv

MAX_N, MAX_M = 1001, 1001
variables, constraints = 0, 0
A = np.empty((MAX_M, MAX_N))  # Matrix of coefficients of constraints
b = np.empty(MAX_M)  # Vector of constraint values
c = np.empty(MAX_N)  # Vector of objective function variables
v = 0  # Constant
N = np.empty(MAX_N, np.intc)  # Nonbasic variables
B = np.empty(MAX_M, np.intc)  # Basic variables
file_name = input("Enter file location: ")
with open(file_name, newline="") as csvfile:
    csv_reader = csv.reader(csvfile)
    # Read the first line for no. variables and constraints
    variables, constraints = tuple(map(int, next(csv_reader)))
    for i in range(variables):
        # Iterate over each row of the constraint coefficients
        row = list(map(float, next(csv_reader)))
        for j in range(constraints):
            # Populate the constraint coefficient array
            A[i, j] = row[j]
    # Read the line containing
    row = list(map(float, next(csv_reader)))
    for i in range(constraints):
        b[i] = row[i]
    row = list(map(float, next(csv_reader)))
    for i in range(variables):
        c[i] = row[i]
with open('input/pvwatts_hourly.csv', newline="") as e_data:
    csv_reader = csv.reader(e_data)
    for i in range(18):
        next(csv_reader)
    solar_data = []
    for row in csv_reader:
        solar_data.append(np.longdouble(row[-1]))
    total = solar_data.pop()
    sum_total = sum(solar_data)
    print(total, sum_total)
    
# Define the parameters of the problem:
# variables, constraints = 3, 3  # Number of variables, constraints
# A[0, 0], A[0, 1], A[0, 2] = -2, -3, -1
# A[1, 0], A[1, 1], A[1, 2] = -4, -1, -2
# A[2, 0], A[2, 1], A[2, 2] = -3, -4, -2
# b[0], b[1], b[2] = 5, 11, 8
# c[0], c[1], c[2] = 5, 4, 3

# infeasible example
# A[0][0], A[0][1] = -1, -1
# A[1][0], A[1][1] = 2, 2
# b[0], b[1] = 2, -10
# c[0], c[1] = 3, -2

# sample house
# A[0, 0], A[0, 1] = -1100, 0
# A[1, 0], A[1, 1] = -1 / 0.193, -1 / 0.193
# b[0], b[1] = 5760, 30
# c[0], c[1] = -2000 + 0.1 * 1100 * 20, -2000 + 0.04 * 1100 * 20

# Pass the parameters to the solving algorithm
lo.run(variables, constraints, A, b, c, v, N, B)
