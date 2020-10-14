from pairs_trading.EG_method import EG_method
import pandas as pd
import numpy as np
import statsmodels.api as sm

# first we verify the status of cointegration by checking historical datasets
# bandwidth determines the number of data points for consideration
# bandwidth is 250 by default, around one year's data points
# if the status is valid, we check the signals
# when z stat gets above the upper bound
# we long the bearish one and short the bullish one, vice versa
def signal_generation(asset1, asset2, method, bandwidth=250):

    signals = pd.DataFrame()
    signals["asset1"] = asset1["Close"]
    signals["asset2"] = asset2["Close"]

    # signals only imply holding
    signals["signals1"] = 0
    signals["signals2"] = 0

    # initialize
    prev_status = False
    signals["z"] = np.nan
    signals["z upper limit"] = np.nan
    signals["z lower limit"] = np.nan
    signals["fitted"] = np.nan
    signals["residual"] = np.nan

    # signal processing
    for i in range(bandwidth, len(signals)):

        # cointegration test
        coint_status, model = method(
            signals["asset1"].iloc[i - bandwidth : i],
            signals["asset2"].iloc[i - bandwidth : i],
        )

        # cointegration breaks
        # clear existing positions
        if prev_status and not coint_status:
            if signals.at[signals.index[i - 1], "signals1"] != 0:
                signals.at[signals.index[i], "signals1"] = 0
                signals.at[signals.index[i], "signals2"] = 0
                signals["z"].iloc[i:] = np.nan
                signals["z upper limit"].iloc[i:] = np.nan
                signals["z lower limit"].iloc[i:] = np.nan
                signals["fitted"].iloc[i:] = np.nan
                signals["residual"].iloc[i:] = np.nan

        # cointegration starts
        # set the trigger conditions
        # this is no forward bias
        # just to minimize the calculation done in pandas
        if not prev_status and coint_status:

            # predict the price to compute the residual
            signals["fitted"].iloc[i:] = model.predict(
                sm.add_constant(signals["asset1"].iloc[i:])
            )
            signals["residual"].iloc[i:] = (
                signals["asset2"].iloc[i:] - signals["fitted"].iloc[i:]
            )

            # normalize the residual to get z stat
            # z should be a white noise following N(0,1)
            signals["z"].iloc[i:] = (
                signals["residual"].iloc[i:] - np.mean(model.resid)
            ) / np.std(model.resid)

            # create thresholds
            # conventionally one sigma is the threshold
            # two sigma reaches 95% which is relatively difficult to trigger
            signals["z upper limit"].iloc[i:] = signals["z"].iloc[i] + np.std(
                model.resid
            )
            signals["z lower limit"].iloc[i:] = signals["z"].iloc[i] - np.std(
                model.resid
            )

        # as z stat cannot exceed both upper and lower bounds at the same time
        # the lines below hold
        if coint_status and signals["z"].iloc[i] > signals["z upper limit"].iloc[i]:
            signals.at[signals.index[i], "signals1"] = 1
        if coint_status and signals["z"].iloc[i] < signals["z lower limit"].iloc[i]:
            signals.at[signals.index[i], "signals1"] = -1

        prev_status = coint_status

    # signals only imply holding
    # we take the first order difference to obtain the execution signal
    signals["positions1"] = signals["signals1"].diff()

    # only need to generate trading signal of one asset
    # the other one should be the opposite direction
    signals["signals2"] = -signals["signals1"]
    signals["positions2"] = signals["signals2"].diff()

    return signals
