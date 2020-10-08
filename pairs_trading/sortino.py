#sortino ratio is another variation of sharpe ratio
#the standard deviation of all returns is substituted with standard deviation of negative returns
#sortino ratio measures the impact of negative return on return
#i am also using student T probability distribution function instead of normal distribution
#check wikipedia for more details
# https://en.wikipedia.org/wiki/Sortino_ratio
def sortino(risk_free,degree_of_freedom,growth_rate,minimum):

    v=np.sqrt(np.abs(scipy.integrate.quad(lambda g:((risk_free-g)**2)*scipy.stats.t.pdf(g,degree_of_freedom),risk_free,minimum)))
    s=(growth_rate-risk_free)/v[0]

    return s
