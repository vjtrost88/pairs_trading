import pandas as pd
import matplotlib.pyplot as plt

# visualize overall portfolio performance
def portfolio(df1):
    """Visualize overall portfolio performance given a _signals_ object"""

    # initial capital to calculate the actual pnl
    capital0 = 2000

    # shares to buy of each position
    positions1 = capital0 // df1["asset1"].iloc[0]
    positions2 = capital0 // df1["asset2"].iloc[0]

    # cumsum1 column is created to check the holding of the position
    df1["cumsum1"] = df1["positions1"].cumsum()

    # since there are two assets, we calculate each asset separately
    # in the end we aggregate them into one portfolio
    portfolio = pd.DataFrame()
    portfolio["asset1"] = df1["asset1"]
    portfolio["holdings1"] = df1["cumsum1"] * df1["asset1"] * positions1
    portfolio["cash1"] = (
        capital0 - (df1["positions1"] * df1["asset1"] * positions1).cumsum()
    )
    portfolio["total asset1"] = portfolio["holdings1"] + portfolio["cash1"]
    portfolio["return1"] = portfolio["total asset1"].pct_change()
    portfolio["positions1"] = df1["positions1"]
    portfolio["signals1"] = df1["signals1"]

    df1["cumsum2"] = df1["positions2"].cumsum()
    portfolio["asset2"] = df1["asset2"]
    portfolio["holdings2"] = df1["cumsum2"] * df1["asset2"] * positions2
    portfolio["cash2"] = (
        capital0 - (df1["positions2"] * df1["asset2"] * positions2).cumsum()
    )
    portfolio["total asset2"] = portfolio["holdings2"] + portfolio["cash2"]
    portfolio["return2"] = portfolio["total asset2"].pct_change()
    portfolio["positions2"] = df1["positions2"]
    portfolio["signals2"] = df1["signals2"]

    portfolio["z"] = df1["z"]
    portfolio["total asset"] = portfolio["total asset1"] + portfolio["total asset2"]
    portfolio["return"] = portfolio["total asset"].pct_change()
    portfolio["z upper limit"] = df1["z upper limit"]
    portfolio["z lower limit"] = df1["z lower limit"]

    # plotting the asset value change of the portfolio
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()

    (l1,) = ax.plot(portfolio["total asset"], c="#46344e")
    (l2,) = ax2.plot(portfolio["z"], c="#4f4a41", alpha=0.2)

    b = ax2.fill_between(
        portfolio.index,
        portfolio["z upper limit"],
        portfolio["z lower limit"],
        alpha=0.2,
        color="#ffb48f",
    )

    # due to the opposite direction of trade for 2 assets
    # we will not plot positions on asset performance

    ax.set_ylabel("Asset Value")
    ax2.set_ylabel("Z Statistics", rotation=270)
    ax.yaxis.labelpad = 15
    ax2.yaxis.labelpad = 15
    ax.set_xlabel("Date")
    ax.xaxis.labelpad = 15

    plt.legend(
        [l2, b, l1],
        ["Z Statistics", "Z Statistics +-1 Sigma", "Total Asset Performance"],
        loc="best",
    )

    plt.grid(True)
    plt.title("Total Asset")
    plt.show()

    return portfolio
