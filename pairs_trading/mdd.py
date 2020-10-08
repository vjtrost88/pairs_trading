#i use a function to calculate maximum drawdown
#the idea is simple
#for every day, we take the current asset value marked to market
#to compare with the previous highest asset value
#we get our daily drawdown
#it is supposed to be negative if the current one is not the highest
#we implement a temporary variable to store the minimum negative value
#which is called maximum drawdown
#for each daily drawdown that is smaller than our temporary value
#we update the temp until we finish our traversal
#in the end we return the maximum drawdown
def mdd(series):
    '''Idea here: for every day, we take the current asset value market to market
    to compare with the previous highest asset value. We get our daily drawdown -- 
    it is supposed to be negative if the current one is not the highest. We implement a
    temporary variable to store the minimum negative value whidh is called Maximum
    Drawdown. For each daily drawdown that is smaller than our temporary value,
    we update the temp until we finish our traversal. In the end we return max drawdown''' 

    minimum=0
    for i in range(1,len(series)):
        if minimum>(series[i]/max(series[:i])-1):
            minimum=(series[i]/max(series[:i])-1)

    return minimum
