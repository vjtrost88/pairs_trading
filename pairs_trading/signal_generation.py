#the signal generation process is very straight forward
#if the normalized residual gets above or below threshold
#we long the bearish one and short the bullish one, vice versa
#i only need to generate trading signal of one asset
#the other one should be the opposite direction
def signal_generation(df1,df2,method):
    '''
    Given two pricing data frames for separate assets and a signal generation method
    (like cointegration), it will return the long/short signals for each day.
    '''
    
    
    signals=method(df1,df2)

    signals['signals1']=0
    
    #as z statistics cannot exceed both upper and lower bounds at the same time
    #this line holds
    signals['signals1']=np.select([signals['z']>signals['z upper limit'], \
                                   signals['z']<signals['z lower limit']], \
                                   [-1,1],default=0)
    
    #signals only imply holding
    #we take the first order difference to obtain the execution signal
    signals['positions1']=signals['signals1'].diff()
    signals['signals2']=-signals['signals1']
    signals['positions2']=signals['signals2'].diff()
    
    #fix initial positions issue
    if signals['signals1'].iloc[0]!=0:
        signals['positions1'].iloc[0]=signals['signals1'].iloc[0]
        signals['positions2'].iloc[0]=signals['signals2'].iloc[0]        
    
    return signals

