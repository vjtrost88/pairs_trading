# check cointegration status
from sklearn.model_selection import train_test_split
import pandas as pd
import statsmodels.api as sm
import numpy as np


# use Engle-Granger two-step method to test cointegration
# the underlying method is straight forward and easy to implement
# a more important thing is the method is invented by the mentor of my mentor!!!
# the latest statsmodels package should ve included johansen test which is more common
# check sm.tsa.var.vecm.coint_johansen
# the malaise of two-step is the order of the cointegration
# unlike johansen test, two-step method can only detect the first order
# check the following material for further details
# https://warwick.ac.uk/fac/soc/economics/staff/gboero/personal/hand2_cointeg.pdf
def EG_method(X, Y, show_summary=False):

    # step 1
    # estimate long run equilibrium
    model1 = sm.OLS(Y, sm.add_constant(X)).fit()
    epsilon = model1.resid

    if show_summary:
        print("\nStep 1\n")
        print(model1.summary())

    # check p value of augmented dickey fuller test
    # if p value is no larger than 5%, stationary test is passed
    if sm.tsa.stattools.adfuller(epsilon)[1] > 0.05:
        return False, model1

    # take first order difference of X and Y plus the lagged residual from step 1
    X_dif = sm.add_constant(pd.concat([X.diff(), epsilon.shift(1)], axis=1).dropna())
    Y_dif = Y.diff().dropna()

    # step 2
    # estimate error correction model
    model2 = sm.OLS(Y_dif, X_dif).fit()

    if show_summary:
        print("\nStep 2\n")
        print(model2.summary())

    # adjustment coefficient must be negative
    if list(model2.params)[-1] > 0:
        return False, model1
    else:
        return True, model1
