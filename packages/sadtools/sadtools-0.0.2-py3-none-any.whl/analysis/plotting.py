import matplotlib.pyplot as plt
import numpy as np
import .plotHelper as pH


try:
  plt.style.use('scientific_grid_no_space')
except:
  pass


# -------------------------------------------------------------------------
# Modular plotting functions
# -------------------------------------------------------------------------
def plot_data(ax, x_data, y_data, x_error_data=None, y_error_data=None,
    color='k', ls='-',
    xlabel=None, ylabel=None,
    xscale='linear', yscale='linear'):
  # Plot 'x_' and 'y_data' on specified axis 'ax', including errors if
  # present
  fig = None
  if ax == None:
    fig, ax = plt.subplots()

  # Plot data
  if x_error_data or y_error_data:
    ax.errorbar(x_data, y_data, xerr=x_error_data, yerr=y_error_data,
       color=color, ls=ls)
  else:
    ax.plot(x_data, y_data, color=color, ls=ls)

  # Labels
  if xlabel:
    ax.set_xlabel(xlabel)
  
  if ylabel:
    ax.set_ylabel(ylabel)

  # Set scales
  ax.set_xscale(xscale)
  ax.set_yscale(yscale)

  return fig, ax  # 'fig' will be None if 'ax' was provided

def plot_histogram(ax, data, color='gray', bins=None,
                       xlabel=None, ylabel=None, xscale="linear", yscale="linear"):
  # Plot a histogram of the specified DataFrame column 'df[key]'
  fig = None
  if ax == None:
    fig, ax = plt.subplots()

  mean, median, std_dev = np.mean(data), np.nanmedian(data), np.std(data)

  ax.hist(data, bins=bins, density=True, color=color)

  # Vertical lines for mean, median
  ax.axvline(mean, c='r', ls='--')
  ax.axvline(median, c='b', ls='--')

  # Set scales
  ax.set_xscale(xscale)
  ax.set_yscale(yscale)

  if xlabel:
    ax.set_xlabel(xlabel)

  if ylabel:
    ax.set_ylabel(ylabel)

  return fig, ax  # 'fig' will be None if 'ax' was provided


def plot_data_correlations(ax, correlations_array, 
    cmap='jet', add_text=True, xlabels=[], ylabels=[]):
  # Plot correlations between parameters as a heatmap
  fig = None
  if ax == None:
    fig, ax = plt.subplots()

  # Plot heatmap
  ax.imshow(correlations_array, cmap=cmap)
  
  # Axes ticks
  ticks = np.arange(len(correlations_array))
  ax.set_xticks(ticks)
  ax.set_yticks(ticks)
  
  # Axes tick labels
  ax.set_xticklabels(xlabels)
  ax.set_yticklabels(ylabels)

  # Rotate the tick labels and set their alignment.
  plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
          rotation_mode="anchor")

  # Add text annotations of correlation coefficients to heatmap
  if add_text:
    for i in range(len(correlations_array)):
      for j in range(len(correlations_array)):
        ax.text(j, i, f"{correlations_array[i, j]:.3f}", ha="center", va="center", color="w")

  return fig, ax  # 'fig' will be None if 'ax' was provided


# -------------------------------------------------------------------------
# Dataframe plotting functions
# -------------------------------------------------------------------------
def plot_df_key(ax, df, x_key, y_key, x_error_key=None, y_error_key=None, 
    color='k', ls='-',
    xlabel=None, ylabel=None, 
    xscale="linear", yscale="linear"):
  # Plot DataFrame columns 'df[x_key]' vs 'df[y_key]'
  fig = None
  if ax == None:
    fig, ax = plt.subplots()

  # Copy DF for plotting so it is not changed outside of this scope
  plot_df = df.copy()

  # Get data from DF
  x_data = plot_df[x_key]
  y_data = plot_df[y_key]

  x_error_data = None
  y_error_data = None

  # Get error data from DF
  if x_error_key:
    x_error_data = plot_df[x_error_key]
  
  if y_error_key:
    y_error_data = plot_df[y_error_key]

  # Plot data
  fig, ax = plot_data(ax, x_data, y_data, x_error_data=x_error_data, y_error_data=y_error_data,
    color=color, ls=ls, xlabel=xlabel, ylabel=ylabel, xscale=xscale, yscale=yscale)

  return fig, ax  # 'fig' will be None if 'ax' was provided


def plot_df_key_histogram(ax, df, key, color='gray', bins=None,
                       xlabel=None, ylabel=None, xscale="linear", yscale="linear"):
  # Plot a histogram of the specified DataFrame column 'df[key]'
  fig = None
  if ax == None:
    fig, ax = plt.subplots()

  # Copy DF for plotting so it is not changed outside of this scope
  plot_df = df.copy()

  data = plot_df[key]

  fig, ax = plot_histogram(ax, data, color=color, bins=bins, 
    xlabel=xlabel, ylabel=ylabel, xscale=xscale, yscale=yscale)

  return fig, ax  # 'fig' will be None if 'ax' was provided


def plot_df_correlations(ax, df, keys, cmap='jet', add_text=True):
  # Calculate and plot correlations between 'keys' in DataFrame 'df'
  import utilities.dataframeUtilities as dfut

  fig = None
  if ax == None:
    fig, ax = plt.subplots()

  plot_df = df.copy()
  correlations = dfut.get_correlation(plot_df, columns=keys)

  fig, ax = plot_data_correlations(ax, correlations, 
    cmap=cmap, add_text=add_text, xlabels=keys, ylabels=keys)

  return fig, ax  # 'fig' will be None if 'ax' was provided
