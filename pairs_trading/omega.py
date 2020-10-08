#omega ratio is a variation of sharpe ratio
#the risk free return is replaced by a given threshold
#in this case, the return of benchmark
#integral is needed to calculate the return above and below the threshold
#you can use summation to do approximation as well
#it is a more reasonable ratio to measure the risk adjusted return
#normal distribution doesnt explain the fat tail of returns
#so i use student T cumulated distribution function instead 
#to make our life easier, i do not use empirical distribution
#the cdf of empirical distribution is much more complex
#check wikipedia for more details
# https://en.wikipedia.org/wiki/Omega_ratio
def omega(risk_free,degree_of_freedom,maximum,minimum):

    y=scipy.integrate.quad(lambda g:1-scipy.stats.t.cdf(g,degree_of_freedom),risk_free,maximum)
    x=scipy.integrate.quad(lambda g:scipy.stats.t.cdf(g,degree_of_freedom),minimum,risk_free)

    z=(y[0])/(x[0])

    return z
