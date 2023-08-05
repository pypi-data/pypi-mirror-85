# -------------------------------------------------------------------------
# Dictionary utility functions
# -------------------------------------------------------------------------
def convert_log_dict_to_linear(log_dict):
  linear_dict = {}

  for key, value in log_dict.items():
    linear_dict[key] = 10**value
  
  return linear_dict


def add_unit_to_dict_items(dictionary, unit):
  unit_dict = {}

  for key, value in dictionary.items():
    unit_dict[key] = value * unit

  return unit_dict
