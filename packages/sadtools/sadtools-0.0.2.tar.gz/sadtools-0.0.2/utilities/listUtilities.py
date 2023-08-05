import operator as opt
import functools as ft

# -------------------------------------------------------------------------
# List utility functions
# -------------------------------------------------------------------------
def list_instances_to_dict(list_):
  # Takes in 'reactants' or 'products' list which may have duplicate keys
  # and creates the dictionary expected by Reaction()
  output_dict = {}
  for element in [sublist for i, sublist in enumerate(list_, 1) if sublist not in list_[i:]]:
    output_dict[element] = list_.count(element)

  return output_dict


def reduce_list(list_, operator=opt.mul):
  # Reduce a list to a single value based on the operator provided
  return ft.reduce(lambda a, b: operator(a, b), list_)


def chunk_list(list, n):
  # Subdivide and return list in chunks based on sample 'n'
  chunks = []
  step = len(list) // n - 1

  for i in range(0, len(list), step):
      chunks.append(list[i: i + step])

  return chunks
