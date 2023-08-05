import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def steady_state(
    data: pd.DataFrame, ratio_lim: float = 2.5, avg_filter: float = 0.2, var_filter: float = 0.1, debug: bool = False
):
    """
    Steady state detector for a time series signal.

    Args:
        data (pd.DataFrame): Data to detect steady state on.
        ratio_lim (float, optional): Specifies the variance ratio threshold if it is in steady state or not.
            A variance greather than ``ratio_lim`` means it is in transient state.
        avg_filter (float, optional): Parameter that determines how many datapoints to use for calculating the
            average value of the time series.
        var_filter (float, optional): Parameter that determines how many datapoints to use for calculating the variance
            ratio.
        debug (bool, optional): Specifies whether to return a dataframe with columns used for intermediate calculations
            and plot analysis diagrams useful for determining the right parameter values.

    Returns:
        pd.DataFrame: Dataframe with a new column ``SS`` which indicates if the time series is steady (1) or transient
        (0).

    Warning:
        The returned dataframe has fewer rows because the initial datapoints are removed to conserve statistical
        indipendence.

    Hint:
        Larger ``avg_filter`` and ``var_filter`` values mean that fewer datapoints are involved in the analysis, which
        has a benefit of reducing the time for the identifier to catch up to a process change, reducing the average run
        length (ARL). Lower values undesirably increase the ARL to detection, but increase precision. With the default
        values only the previous 45 datapoints will be used.

    Example:

        To identify the optimal hyperparameter values for your data, make sure to run the function in a notebook with
        ``debug`` set to ``True`` as this will output a dataframe with intermediate calculations and plot various
        analysis diagrams.

            >>> # This will output a dataframe and plot analysyis diagrams
            >>> ss_data = steady_state(data, debug=True)

    Note:
        The implemented algorithm is taken from this paper: https://bit.ly/3fNfQZO
    """
    assert isinstance(data, pd.DataFrame), "Input data must be pd.DataFrame"
    assert len(data.columns) == 1, "Input data can only have one column."

    assert ratio_lim >= 0.0

    assert avg_filter >= 0.0 and avg_filter <= 1.0
    assert var_filter >= 0.0 and var_filter <= 1.0

    # Copy data
    df = data.copy()

    # df.columns = ["PV"]  # PV = Process Variable
    colname = data.columns[0]

    # Determine number of datapoints to be used to initializa values (set between 10 and 25)
    Ls = int(len(data) * 0.05)
    assert Ls >= 10, "There are too few datapoints to detect steady states."
    if Ls > 50:
        Ls = 50

    # Initialize filter and variance
    filt0 = df[colname].iloc[0:Ls].mean()
    var0 = df[colname].iloc[0:Ls].var()
    initial = df[colname].iloc[Ls - 1]

    # Remove first Ls df points to conserve statistical independence
    df.drop(df.index[0:Ls], inplace=True)

    # Create internal calculation columns
    df["_filt"] = 0
    df["_var1"] = 0
    df["_var2"] = 0

    # Set algorithm alpha values
    alpha1 = avg_filter
    alpha2, alpha3 = var_filter, var_filter

    # Initialize filter
    df.loc[df.index[0], "_filt"] = alpha1 * df[colname][0] + (1 - alpha1) * filt0

    # Initialize variance based on difference between df and filtered df
    df.loc[df.index[0], "_var1"] = alpha2 * (df[colname][0] - filt0) ** 2 + (1 - alpha2) * var0

    # Initialize diltered variance based sequential df differences
    df.loc[df.index[0], "_var2"] = alpha3 * (df[colname][0] - initial) ** 2 + (1 - alpha3) * var0

    # Calculate filter and variance values
    for i in range(1, len(df)):
        df.loc[df.index[i], "_filt"] = alpha1 * df[colname][i] + (1 - alpha1) * df._filt[i - 1]
        df.loc[df.index[i], "_var1"] = alpha2 * (df[colname][i] - df._filt[i - 1]) ** 2 + (1 - alpha2) * df._var1[i - 1]
        df.loc[df.index[i], "_var2"] = (
            alpha3 * (df[colname][i] - df[colname][i - 1]) ** 2 + (1 - alpha3) * df._var2[i - 1]
        )

    # Calcualte Variance ratio
    df["_ratio"] = (2 - alpha1) * df._var1 / df._var2

    # Filter df based on variance ration threshold (Rlim)
    st_colname = "SS"
    df[st_colname] = 1
    df["_steady"] = df[colname]
    df.loc[df._ratio > ratio_lim, st_colname] = 0
    df.loc[df._ratio > ratio_lim, "_steady"] = np.nan

    # Calculate rolling median from steady values
    df["_steady_ravg"] = df._steady.rolling("1h").median()
    df.loc[df._ratio > ratio_lim, "_steady_ravg"] = np.nan

    # Return df with data column and steady state column
    if not debug:
        return df[[colname, "SS"]]

    # If in debugging mode, return entire dataframe and plot output
    fig, [ax1, ax2, ax3] = plt.subplots(3, 1, figsize=(14, 12), tight_layout=True, sharex=True)

    # Plot time series and where steady state has been detected
    ax1.set_title("Steady State Detection Analysis", fontsize=14)
    ax1.plot(df[colname], "-", label=colname)
    ax1.plot(df._steady, "g-", label="steady state")
    ax1.plot(df._steady_ravg, "k-", linewidth=3, label="SS rolling avg")
    ax1.set_ylabel(colname)
    ax1.grid(which="both")
    ax1.legend()

    # Plot variance ratio
    ax2.plot(df._ratio, "k-")
    ax2.set_ylabel("Variance Ratio")
    ax2.grid(which="both")
    ax2.axhline(ratio_lim, color="r", linestyle="-", label=f"ratio_lim = {ratio_lim}")
    ax2.legend()

    # Plot steady state and transient state periods
    ax3.plot(df["SS"], "k-")
    ax3.set_xlabel("Date and Time")
    ax3.set_ylabel("Steady (1) - Transient (0)")
    ax3.grid(which="both")

    return df
