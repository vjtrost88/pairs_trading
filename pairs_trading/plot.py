import matplotlib.pyplot as plt

# position visualization
def plot(new, ticker1, ticker2):
    """Visualise a position given a _signals_ object and two ticker names"""

    fig = plt.figure(figsize=(10, 5))
    bx = fig.add_subplot(111)
    bx2 = bx.twinx()

    # plot two different assets
    (l1,) = bx.plot(new.index, new["asset1"], c="#4abdac")
    (l2,) = bx2.plot(new.index, new["asset2"], c="#907163")

    (u1,) = bx.plot(
        new.loc[new["positions1"] == 1].index,
        new["asset1"][new["positions1"] == 1],
        lw=0,
        marker="^",
        markersize=8,
        c="g",
        alpha=0.7,
    )
    (d1,) = bx.plot(
        new.loc[new["positions1"] == -1].index,
        new["asset1"][new["positions1"] == -1],
        lw=0,
        marker="v",
        markersize=8,
        c="r",
        alpha=0.7,
    )
    (u2,) = bx2.plot(
        new.loc[new["positions2"] == 1].index,
        new["asset2"][new["positions2"] == 1],
        lw=0,
        marker=2,
        markersize=9,
        c="g",
        alpha=0.9,
        markeredgewidth=3,
    )
    (d2,) = bx2.plot(
        new.loc[new["positions2"] == -1].index,
        new["asset2"][new["positions2"] == -1],
        lw=0,
        marker=3,
        markersize=9,
        c="r",
        alpha=0.9,
        markeredgewidth=3,
    )

    bx.set_ylabel(
        ticker1,
    )
    bx2.set_ylabel(ticker2, rotation=270)
    bx.yaxis.labelpad = 15
    bx2.yaxis.labelpad = 15
    bx.set_xlabel("Date")
    bx.xaxis.labelpad = 15

    plt.legend(
        [l1, l2, u1, d1, u2, d2],
        [
            ticker1,
            ticker2,
            "LONG {}".format(ticker1),
            "SHORT {}".format(ticker1),
            "LONG {}".format(ticker2),
            "SHORT {}".format(ticker2),
        ],
        loc=8,
    )

    plt.title("Pair Trading")
    plt.xlabel("Date")
    plt.grid(True)
    plt.show()
