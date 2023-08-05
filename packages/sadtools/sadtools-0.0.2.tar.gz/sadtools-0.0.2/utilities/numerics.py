import numpy as np
from scipy.interpolate import splrep, splev
import math


# -------------------------------------------------------------------------
# Grid functions
# -------------------------------------------------------------------------
def create_grid(x_range, y_range, num_x_points=50, num_y_points=50):
  # Utility function for creating a general mesh grid
  x = np.linspace(*x_range, num=num_x_points)
  y = np.linspace(*y_range, num=num_y_points)

  grid = np.meshgrid(x, y)

  return grid


# -------------------------------------------------------------------------
# Interpolation functions
# -------------------------------------------------------------------------
def determine_fits(x_list, data_list):
  # Takes in a single x-variable list and a list of y-variable lists to generate fits for each
    fits = []
    # x_list = sorted(x_list)

    for data in data_list:
        fit = splrep(x_list, data)
        fits.append(fit)

    return fits


def evaluate_fits(x_list, fits_list):
  # Takes in a list of x-value lists and an associated fits list for interpolation
    y_data_list = [[] for _ in range(len(fits_list))]

    for x in x_list:
        for index, fit in enumerate(fits_list):
            y_data_list[index].append(float(splev(x, fit)))

    return y_data_list


# -------------------------------------------------------------------------
# Arithmetic utility functions
# -------------------------------------------------------------------------
def even_to_odd(number, direction='up'):
    """
    Casts an even number to an odd number. Used mainly to centre axis labels for plots by having an odd number of
    rows and columns.
    
    Arguments:
        number {Int} -- Even number to be cast to an odd number.
    
    Keyword Arguments:
        direction {str} -- If 'up', add 1 to the even number. If 'down', subtract 1 from the even number. 
        (default: {'up'})
    
    Returns:
        {int} -- Odd number
    """
    number = int(number)
    if number % 2 == 0:
        if direction is 'up':
            number += 1
        elif direction is 'down':
            number -= 1
        else:
            print("Invalid option {direction}. Valid options are \'up\' or \'down\'. Choosing \'up\'.")
            number += 1
    
    return number


def is_square(number: int) -> bool:
  root = math.isqrt(number)
  return number == root ** 2
