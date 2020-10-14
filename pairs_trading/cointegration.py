# check cointegration status
from sklearn.model_selection import train_test_split
import pandas as pd
import statsmodels.api as sm
import numpy as np


def cointegration(data1, data2, override=False):
    """
    Given two data frames with a \"close\" column, return cointegration status.
    Override will return signals table even if the pair is not cointegrated.
    """

    # train test split
    # this is the reason the results here are different than the stattools.coint fcn
    df1, test1, df2, test2 = train_test_split(
        data1, data2, test_size=0.7, shuffle=False
    )

    train = pd.DataFrame()
    train["asset1"] = df1["close"]
    train["asset2"] = df2["close"]

    # this is the part where we test the cointegration
    # in this case, i use Engle-Granger two-step method
    # which is invented by the mentor of my mentor!!!
    # generally people use Johanssen test to check the cointegration status
    # the first step for EG is to run a linear regression on both variables
    # next, we do OLS and obtain the residual
    # after that we run unit root test to check the existence of cointegration
    # if it is stationary, we can determine its a drunk man with a dog
    # the first step would be adding a constant vector to asset1

    x = sm.add_constant(train["asset1"])
    y = train["asset2"]
    model = sm.OLS(y, x).fit()
    resid = model.resid

    print(model.summary())
    pval = sm.tsa.stattools.adfuller(resid)[1]
    print("\nCointegration P-value: ", pval)
    if pval > 0.05:
        print("Pair is not cointegrated!")
        if override:
            pass
        else:
            return

    # this phrase is how we set the trigger conditions
    # first we normalize the residual
    # we would get a vector that follows standard normal distribution
    # generally speaking, most tests use one sigma level as the threshold
    # two sigma level reaches 95% which is relatively difficult to trigger
    # after normalization, we should obtain a white noise follows N(0,1)
    # we set +-1 as the threshold
    # eventually we visualize the result

    signals = pd.DataFrame()
    signals["asset1"] = test1["close"]
    signals["asset2"] = test2["close"]

    signals["fitted"] = np.mat(sm.add_constant(signals["asset2"])) * np.mat(
        model.params
    ).reshape(2, 1)

    signals["residual"] = signals["asset1"] - signals["fitted"]

    signals["z"] = (signals["residual"] - np.mean(signals["residual"])) / np.std(
        signals["residual"]
    )

    # use z*0 to get panda series instead of an integer result
    signals["z upper limit"] = (
        signals["z"] * 0 + np.mean(signals["z"]) + np.std(signals["z"])
    )
    signals["z lower limit"] = (
        signals["z"] * 0 + np.mean(signals["z"]) - np.std(signals["z"])
    )

    return signals
