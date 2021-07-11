# Linear Optimization Using the Simplex Method

The purpose of this project is to create an implementation of the simplex method for solving linear programming problems.

To run, open command line in the src directory with Python version 3.8 or greater installed and type:

```cmd
pip install poetry;
poetry install;
poetry run python linearoptimization;
```

The current version of the program accepts values for the optimization problem via a `.CSV` file. This file should be structured such that the first line contains the number of variables and the number of constraints, the next section should contain the coefficients of the constraints, and the final two lines should contain the constraint values and objective function coefficients.
