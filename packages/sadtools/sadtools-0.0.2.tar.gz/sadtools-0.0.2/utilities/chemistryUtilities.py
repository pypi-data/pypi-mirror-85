import numpy as np
import utilities as util
import astropy.units as u


# -------------------------------------------------------------------------
# Derived Units
# -------------------------------------------------------------------------
cm3 = u.cm**3
dm3 = u.dm**3
m3 = u.m**3
g_cm3 = (u.g / cm3)
molar = u.mol / dm3

# -------------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------------
avogadro_constant = 6.0221415E+23 / u.mol  # atoms [mol^-1]
hydrogen_mass_amu = 1.008  # a.m.u., standard atomic weight
hydrogen_mass_cgs = 1.6733E-24 * u.g  # [g]

# -------------------------------------------------------------------------
# Conversion functions for physical quantities
# -------------------------------------------------------------------------
def gas_density_to_hydrogen_number_density(gas_density, percentage_hydrogen=1, log=False):
  # Converts gas density (assumed [g cm^-3]) to a hydrogen number density 
  # based on the percentage of hydrogen (default 100% hydrogen)
  hydrogen_number_density = (gas_density / hydrogen_mass_cgs) * percentage_hydrogen

  if log:
    return np.log10(hydrogen_number_density.value)
  else:
    return hydrogen_number_density

def log_abundance_to_number_density(log_abundance, log_hydrogen_number_density, log_hydrogen_abundance=12):
  # Using the log(hydrogen abundance) (default '12' for solar physics),
  # convert from stellar photospheric abundance to a number density
  log_number_density = log_abundance - log_hydrogen_abundance + log_hydrogen_number_density
  number_density = 10**log_number_density
  
  return number_density

def number_density_to_concentration(number_density):
  # Assumes number density in [cm^-n] & 'avogadro_constant' in [mol^-1]
  # so concentration ~ [mol cm^-n]
  concentration = number_density / avogadro_constant

  return concentration

def concentration_to_number_density(concentration):
  # Assumes concentration ~ [mol cm^-3] & 'avogadro_constant' in [mol^-1]
  # so number density in [cm^-3]
  number_density = concentration * avogadro_constant

  return number_density
  
# -------------------------------------------------------------------------
# Stoichiometry functions
# -------------------------------------------------------------------------
def calculate_stoichiometry(reactants_list, products_list, return_dicts=False):
  reactant_stoichiometry = util.list_instances_to_dict(reactants_list)
  product_stoichiometry = util.list_instances_to_dict(products_list)

  if return_dicts:
    return reactant_stoichiometry, product_stoichiometry
  else:
    return reactant_stoichiometry.values, product_stoichiometry.values

# -------------------------------------------------------------------------
# Reaction rate and timescale functions
# -------------------------------------------------------------------------
def modified_to_arrhenius_prefactor(alpha, beta, temperature):
	# Modified Arrhenius rate prefactor to Arrhenius rate prefactor
	return alpha * (temperature / 300)**beta

def modified_arrhenius_rate(alpha=1, beta=0, gamma=0, temperature=300):
  # rate = alpha * (T/300[K])^beta * EXP(-gamma / T)
	# Equivalent to standard Arrhenius for beta=0
  return alpha * (temperature/300)**beta * np.exp(-gamma / temperature)

def arrhenius_rate(prefactor, activation_energy, temperature):
  return prefactor * np.exp(-activation_energy / temperature)

def calculate_unitless_timescale(forward_rate, reverse_rate=None, reactant_stoichiometry=[1, 1]):
  # Example case: A + B -> C
  # Note that this is only valid if rates are dimensionless. Othwerwise, 
  # the rates need to be related to one another based on the number 
  # densities of the reactants and products
  total_rate = forward_rate.value * np.sum(reactant_stoichiometry)

  if reverse_rate != None:
    total_rate += reverse_rate.value
  
  timescale = 1 / total_rate

  return timescale

# -------------------------------------------------------------------------
# Functions for determining equilibrium quantities
# -------------------------------------------------------------------------
def equilibrium_constant_dimensional(forward_rate_coefficient,
                                    reverse_rate_coefficient):
  # dimensional equilibrium constant K_eq = k_f / k_r
  equilibrium_constant = forward_rate_coefficient / reverse_rate_coefficient

  return equilibrium_constant

# -------------------------------------------------------------------------
# Utility functions for rates and timescales
# -------------------------------------------------------------------------
def scale_timescale_with_number_density(timescale, reactant_number_density):
  # Scale timescale based on number of primary reactants; Wedemeyer-Boehm(2005)
  scaled_timescale = timescale / reactant_number_density
  
  return scaled_timescale

def convert_rate_to_molar(rate, order):
  # Assumes rate is in [cm^-3*n s^-1] where 'n' is order of reaction
  # Convert from cm^3 -> dm^3 & use Avogadro number to change from 
  # volume / atom -> volume / mol
  volume_conversion = cm3.to(dm3)
  conversion_factor = (volume_conversion * avogadro_constant)**order
  molar_rate = rate * conversion_factor  # units of [mol^n dm^-3n s^-1]

  return molar_rate

# -------------------------------------------------------------------------
# Unit conversion functions
# -------------------------------------------------------------------------
def get_rate_unit_from_order(order, unit_system='cgs'):
  # Based on the order of the reaction (n), determine the proper units for 
  # the reaction rate.
  unit = None
  if unit_system == 'cgs':
    # [cm^3*n s^-1]
    unit = (cm3)**order
  elif unit_system == 'molar':
    # [M^(1-n) s^-1]
    unit = (u.M)**(1-order)
  
  unit /= u.s

  return unit