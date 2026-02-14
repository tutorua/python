import numpy as np
from numpy.polynomial import Polynomial

# 3
# 1 5.5 -9.75
# 4
# 1.5 3.25 -9.05005 -1.0
np.set_printoptions(precision = 5, floatmode='fixed')
# read the polynom order
ord = int(input("Enter the polynom order: "))
print(ord)
roots = [float(i) for i in input("Enter the polynom roots (separated by spaces): ").split()]
print(roots)
points = int(input("Enter the number of points: "))
print(points)
arguments = [float(i) for i in input("Enter the arguments to calculate the polynom values (separated by spaces): ").split()]

# Create a polynomial object from roots
polynom = Polynomial.fromroots(roots)
print("Polynom: ", polynom)
coeffs = polynom.coef[::-1]
print("Polynomial coefficients: ", coeffs)

# Calculate the polynom values for the given points
values = polynom(np.array(arguments))
print("Values in the given points: ", values)

# Calculate the drivative values for the given points
derivative = polynom.deriv()
der_values = derivative(np.array(arguments))
print("Derivative values in the given points: ", der_values)
