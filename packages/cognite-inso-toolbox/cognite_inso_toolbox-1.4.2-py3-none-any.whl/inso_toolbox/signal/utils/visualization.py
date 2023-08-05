"""
Functions used to visualize data from Oscillations Data Quality Metrics
"""
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec


def plot_lpc_roots(
    threshold: float,
    time: np.ndarray,
    data: np.ndarray,
    predicted: np.ndarray,
    f: np.ndarray,
    pxx: np.ndarray,
    roots: np.ndarray,
    distances: np.ndarray,
    figsize: Tuple = (9, 6),
) -> Tuple[plt.Figure, list]:
    """

    Args:
        threshold (float):  Threshold Radius of the circle to determine if a signal has oscillatory components
        time (np.ndarray): Time vector of the signal
        data (np.ndarray): Raw data vector
        predicted (np.ndarray): Predicted polynomial obtained form the LPC analysis
        f (np.ndarray): Frequency vector from the power spectral density analysis
        pxx (np.ndarray): Power spectral density of the signal
        roots (np.ndarray): Roots of the LPC coefficient
        distances (np.ndarray): Distance to the unit circle for each root
        figsize (Tuple): Size of figure

    Returns:

        Tuple[plt.Figure, list]
    """

    fig = plt.figure(constrained_layout=True, figsize=figsize)

    gs = GridSpec(2, 3, figure=fig)
    ax1 = fig.add_subplot(gs[0, :])
    ax2 = fig.add_subplot(gs[1, :-1])
    ax3 = fig.add_subplot(gs[1, 2])

    ax1.plot(time, data, marker=".", label="Raw")
    ax1.plot(time, predicted, "-", label="LPC prediction")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Amplitude")
    ax1.set_title("Signal")
    ax1.legend()

    ax2.loglog(f, pxx)
    ax2.set_xlabel("Frequency")
    ax2.set_ylabel("Amplitude")
    ax2.set_title("Power Spectral Density")

    # Unit circle and oscillation threshold
    # If there are roots inside the threshold the signal present signal
    # A root with a distance to unit circle less than 0.2 is label as data with signal
    ang = np.linspace(0, np.pi * 2, 100)
    x_unit = np.cos(ang)
    y_unit = np.sin(ang)
    x_threshold = threshold * np.cos(ang)
    y_threshold = threshold * np.sin(ang)
    # For filling area in plot
    xf = np.concatenate((x_unit, x_threshold[::-1]))
    yf = np.concatenate((y_unit, y_threshold[::-1]))
    ax3.plot(x_unit, y_unit, linewidth=1, color="r")
    ax3.plot(x_threshold, y_threshold, linewidth=1, color="r")
    ax3.axvline(x=0, color="k", linewidth=0.5)
    ax3.axhline(y=0, color="k", linewidth=0.5)
    # Plot roots
    for root, distance in zip(roots, distances):
        if distance > (1 - threshold):
            ax3.plot(root.real, root.imag, "ro", markersize=7)
        else:
            ax3.plot(root.real, root.imag, "go", markersize=7)

    ax3.set_xlabel("Real Part")
    ax3.set_ylabel("Imaginary Part")
    ax3.set_title("LPC Roots in z-plane")

    ax3.fill_between(xf, yf, color="r", alpha=0.05)
    ax3.set_aspect("equal", adjustable="box")

    return fig, [ax1, ax2, ax3]


def plot_peaks(
    lags: np.ndarray,
    xcoef: np.ndarray,
    freqs: np.ndarray,
    power_norm: np.ndarray,
    peak_freqs: np.ndarray,
    peak_power_norm: np.ndarray,
    figsize: Tuple = (9, 4),
) -> Tuple[plt.Figure, plt.Axes]:
    """

    Plots lags and correlation coefficients and peak frequencies.

    Args:
        lags (np.ndarray): Lags from cross correlation computations
        xcoef (np.ndarray): Correlation coefficients corresponding to the lags
        freqs (np.ndarray): Frequencies
        power_norm (np.ndarray): Normalized power coresponding to frequencies in freqs
        peak_freqs (np.ndarray): Detected peak prequencies
        peak_power_norm (np.ndarray): Normalized power of peak frequencies
        figsize (Tuple): size of figure

    Returns:
        Tuple[plt.Figure, plt.Axes]

    """
    fig, ax = plt.subplots(1, 2, figsize=figsize)
    ax[0].plot(lags, xcoef)
    ax[0].set_title("Correlation coefficient with positive lags")
    ax[0].set_xlabel("Lags")
    ax[0].set_ylabel("Correlation coefficients")
    ax[1].plot(freqs, power_norm)
    ax[1].axhline(y=0.3, color="r", linestyle="--")
    ax[1].set_title("Normalized FFT magnitude spectrum")
    ax[1].plot(peak_freqs, peak_power_norm, "go", markersize=8, alpha=0.5)
    ax[1].set_xlabel("Frequency")
    fig.tight_layout()

    return fig, ax
