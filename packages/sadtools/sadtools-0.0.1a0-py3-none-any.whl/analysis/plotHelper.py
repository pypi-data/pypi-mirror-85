def determine_rows_cols_for_subplots(num_subplots):
  # Determine the optimal number of rows and columns for a 'plt.subplots'
  # call based on the number of subplots in the figure, preferring a 
  # square layout. The routine favours the number closest to the 
  # number of subplots, with a minimum of 'num_subplots'
  from itertools import product
  import numpy as np

  # Determine min and max rows to optimise matrix size
  root = np.sqrt(num_subplots)

  # Min and max size for the matrix indices
  max_size = int(np.ceil(root) + 1)
  min_size = int(np.floor(root) - 1)
  matrix_size = max_size - min_size

  matrix = np.zeros(shape=(matrix_size, matrix_size))
  r = range(min_size, max_size)

  for ((indx, x), (indy, y)) in product(enumerate(r), enumerate(r)):
    matrix[indx, indy] = x * y

  # Set elements less than 'num_subplots' to infinity to filter them out
  matrix[np.where(matrix < num_subplots)] = np.inf
  nrows, ncols = np.unravel_index(np.argmin(matrix), matrix.shape)

  # Add 'min_size' back to indices to scale it to normal 'matrix'
  nrows += min_size
  ncols += min_size

  return nrows, ncols
