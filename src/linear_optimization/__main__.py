"""Main entrypoint for the program."""

import linear_optimization as lo
import solar_input as si
import numpy as np

MAX_N, MAX_M = 10001, 10001

ARRAY_COST = 3000  # $/kW
TAX_MODIFIER = 0.74
BATTERY_COST = 150  # $/kWh
P_RETAIL_COST = si.calculate_future_power_costs(
    0.134,  # current $/kWh
    1.018,  # avg. growth factor/yr
    20,  # yrs
)
P_WHOLESALE_COST = 0.0646  # $/kWh
ROOF_AREA = 30
AREA_USAGE = 5.181  # m^2/kW
PRODUCTION_DATA, ANNUAL_PRODUCTION = si.read_pvwatts(
    "input/pvwatts_hourly.csv"
)  # kWh/yr
BATTERY_STORAGE_TARGET = 24  # hrs
USAGE_DATA, TOTAL_USAGE = si.read_usage("input/usage.csv")
USAGE_CONSTRAINTS = si.generate_constraints(
    USAGE_DATA,
    BATTERY_STORAGE_TARGET,
)
PRODUCTION_CONSTRAINTS = si.generate_constraints(
    PRODUCTION_DATA,
    BATTERY_STORAGE_TARGET,
)

variables, constraints = 0, 0
A = np.empty((MAX_M, MAX_N))  # Matrix of coefficients of constraints
b = np.empty(MAX_M)  # Vector of constraint values
c = np.empty(MAX_N)  # Vector of objective function variables
v = 0  # Constant
N = np.empty(MAX_N, np.intc)  # Nonbasic variables
B = np.empty(MAX_M, np.intc)  # Basic variables

# Process data to fit solar equation
# Define the parameters of the problem:
A[0, 0], A[0, 1], A[0, 2] = -ANNUAL_PRODUCTION, 0, 0
A[1, 0], A[1, 1], A[1, 2] = -AREA_USAGE, -AREA_USAGE, 0
b[0], b[1] = TOTAL_USAGE, ROOF_AREA
c[0], c[1], c[2] = (
    (-TAX_MODIFIER * ARRAY_COST + P_RETAIL_COST * ANNUAL_PRODUCTION),
    (-TAX_MODIFIER * ARRAY_COST + P_WHOLESALE_COST * ANNUAL_PRODUCTION),
    -BATTERY_COST,
)

# Find the constraint with the largest difference between usage and production
diff = np.subtract(USAGE_CONSTRAINTS, PRODUCTION_CONSTRAINTS)
loc = np.argmax(diff)

A[2, 0], A[2, 1], A[2, 2] = PRODUCTION_CONSTRAINTS[loc], PRODUCTION_CONSTRAINTS[loc], 1
b[2] = -USAGE_CONSTRAINTS[loc]
variables, constraints = 3, 3

# C_A = cost of array                   $/kW
# x_A1 = solar cap. retail              kW
# x_A2 = solar cap. wholesale           kW
# P_R = retail price of E               $/kWh
# P_W = wholesale price of E            $/kWh
# K = annual production                 kWh/yr
# C_B = cost of battery                 $/kWh
# x_B = battery capacity                kWh
# D = solar area usage                  m^2/kW
# U_tot = energy usage                  kWh/yr
# U_max = usage at max difference       kWh
# Pr_max = production at max difference kWh
# A_roof = area of roof                 m^2
# T = tax credit multiplier

# maximize
#   (-T * C_A + P_R * K) * x_A1 + (-T * C_A + P_W * K) * x_A2 - C_B * x_B
# subj. to
#   -K * x_A1 + U_tot = w_1
#   -D * x_A1 - D * x_A2 + A_roof = w_2
#   Pr_max * x_A1 + Pr_max * x_A2 + x_B - U_max = w_3

#   x_A1, x_A2, x_B, w_1, w_2, w_3 >= 0

# Pass the parameters to the solving algorithm
lo.run(variables, constraints, A, b, c, v, N, B)
