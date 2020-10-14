# stats calculation
def stats(portfolio, trading_signals, stdate, eddate, capital0=10000):
    """Given a portfolio_details object, signals object, start date, end date, and initial capital size,
    compute overall strategy stats."""

    stats = pd.DataFrame([0])

    # get the min and max of return
    maximum = np.max(portfolio["return"])
    minimum = np.min(portfolio["return"])

    # growth_rate denotes the average growth rate of portfolio
    # use geometric average instead of arithmetic average for percentage growth
    growth_rate = (float(portfolio["total asset"].iloc[-1] / capital0)) ** (
        1 / len(trading_signals)
    ) - 1

    # calculating the standard deviation
    std = float(
        np.sqrt(
            (((portfolio["return"] - growth_rate) ** 2).sum()) / len(trading_signals)
        )
    )

    # use S&P500 as benchmark
    benchmark = yf.download("^GSPC", start=stdate, end=eddate)

    # return of benchmark
    return_of_benchmark = float(
        benchmark["Close"].iloc[-1] / benchmark["Open"].iloc[0] - 1
    )

    # rate_of_benchmark denotes the average growth rate of benchmark
    # use geometric average instead of arithmetic average for percentage growth
    rate_of_benchmark = (return_of_benchmark + 1) ** (1 / len(trading_signals)) - 1

    del benchmark

    # backtesting stats
    # CAGR stands for cumulated average growth rate
    stats["CAGR"] = stats["portfolio return"] = float(0)
    stats.loc[:, ("CAGR", 0)] = growth_rate
    # stats['CAGR'][0]=growth_rate
    stats["portfolio return"][0] = portfolio["total asset"].iloc[-1] / capital0 - 1
    stats["benchmark return"] = return_of_benchmark
    stats["sharpe ratio"] = (growth_rate - rate_of_benchmark) / std
    stats["maximum drawdown"] = mdd(portfolio["total asset"])

    # calmar ratio is sorta like sharpe ratio
    # the standard deviation is replaced by maximum drawdown
    # it is the measurement of return after worse scenario adjustment
    # check wikipedia for more details
    # https://en.wikipedia.org/wiki/Calmar_ratio
    stats["calmar ratio"] = growth_rate / stats["maximum drawdown"]
    stats["omega ratio"] = omega(
        rate_of_benchmark, len(trading_signals), maximum, minimum
    )
    stats["sortino ratio"] = sortino(
        rate_of_benchmark, len(trading_signals), growth_rate, minimum
    )

    # note that i use stop loss limit to limit the numbers of longs
    # and when clearing positions, we clear all the positions at once
    # so every long is always one, and short cannot be larger than the stop loss limit
    stats["numbers of longs"] = (
        trading_signals["signals1"].loc[trading_signals["signals1"] == 1].count()
        + trading_signals["signals2"].loc[trading_signals["signals2"] == 1].count()
    )
    stats["numbers of shorts"] = (
        trading_signals["signals1"].loc[trading_signals["signals1"] < 0].count()
        + trading_signals["signals2"].loc[trading_signals["signals2"] < 0].count()
    )

    stats["numbers of trades"] = stats["numbers of shorts"] + stats["numbers of longs"]

    # to get the total length of trades
    # given that cumsum indicates the holding of positions
    # we can get all the possible outcomes when cumsum doesnt equal zero
    # then we count how many non-zero positions there are
    # we get the estimation of total length of trades
    stats["total length of trades"] = (
        trading_signals["signals1"].loc[trading_signals["cumsum1"] != 0].count()
        + trading_signals["signals2"].loc[trading_signals["cumsum2"] != 0].count()
    )
    stats["average length of trades"] = (
        stats["total length of trades"] / stats["numbers of trades"]
    )
    stats["profit per trade"] = float(0)
    stats["profit per trade"].iloc[0] = (
        portfolio["total asset"].iloc[-1] - capital0
    ) / stats["numbers of trades"].iloc[0]

    del stats[0]
    print(stats)
