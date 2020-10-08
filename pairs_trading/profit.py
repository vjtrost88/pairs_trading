#plotting the asset value change of the portfolio
def profit(portfolio):
        
    fig=plt.figure()
    bx=fig.add_subplot(111)
    
    portfolio['total asset'].plot(label='Total Asset')
    
    #long/short position markers related to the portfolio
    #the same mechanism as the previous one
    #replace close price with total asset value
    bx.plot(portfolio['signals1'].loc[portfolio['signals1']==1].index,portfolio['total asset'][portfolio['signals1']==1],lw=0,marker='^',c='g',label='long')
    bx.plot(portfolio['signals2'].loc[portfolio['signals2']==1].index,portfolio['total asset'][portfolio['signals2']==1],lw=0,marker='^',c='g',label='long')

    bx.plot(portfolio['signals1'].loc[portfolio['signals1']<0].index,portfolio['total asset'][portfolio['signals1']<0],lw=0,marker='v',c='r',label='short')
    bx.plot(portfolio['signals2'].loc[portfolio['signals2']<0].index,portfolio['total asset'][portfolio['signals2']<0],lw=0,marker='v',c='r',label='short')

    plt.legend(loc='best')
    plt.grid(True)
    plt.xlabel('Date')
    plt.ylabel('Asset Value')
    plt.title('Total Asset')
    plt.show()
