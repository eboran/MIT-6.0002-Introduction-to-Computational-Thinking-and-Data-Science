# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re
import random

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model
            
    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # TODO
    res = []
    for d in degs:
#        fit = pylab.polyfit(x,y,d) 
#        res.append(pylab.array(fit))
        res.append(pylab.polyfit(x,y,d) )
    return res
    
def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    y_bar = y.sum() / len(y)
    nume = ((y - estimated)**2).sum()
    deno = ((y - y_bar)**2).sum()
    return 1 - float(nume / deno)

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    rSq = []
    for f in models:
        yVals = pylab.polyval(f, x)
        rSq.append(r_squared(y,yVals))
    best = models[rSq.index(max(rSq))]
    yVals = pylab.polyval(best, x)
    pylab.plot(x,y,'.b')
    pylab.plot(x,yVals,'-r')
    if len(best)==2:
        se = str(round(se_over_slope(x, y, yVals, best),4))
        pylab.title('Degree: ' + str(len(best) -1) + ', ' +'R-squared: '\
                    + str(round(max(rSq),4)) +'\n'+'standard error of slope / slope: ' +se\
                    +'\n' + 'coeff of X: ' + str(round(best[0],4)))
    else:
        pylab.title('Degree: ' + str(len(best) -1) + ', ' +'R-squared: '\
                    + str(round(max(rSq),4)) +'\n')
    pylab.xlabel('Years')
    pylab.ylabel('Stadard Deviations')

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    # TODO
    res = []
    for year in years:
        av = []
        for city in multi_cities:
            a = climate.get_yearly_temp(city,year)
            av.append(a.sum() / len(a))
        res.append(sum(av) / len(av))
    return pylab.array(res)

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    # TODO
    ans = []
    for i in range(len(y)):
        if i < window_length-1:
            ans.append(float((sum([y[i-m] for m in range(i+1)])) / (i + 1)))
        else:    
            ans.append(float((sum([y[i-m] for m in range(window_length)])) / window_length))
    return pylab.array(ans)
    
def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    # TODO
    return (((y - estimated)**2).sum() / len(y))**0.5

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    # TODO
    sDs = []
    for year in years:
        complete_year_temps = []
        for month in range(1,13):
            for day in range(1,32):
                days = []
                for city in multi_cities:
                    try:
                        days.append(climate.get_daily_temp(city, month, day, year))   
                    except:
                        continue
                try:
                    avgDay = sum(days) / len(days)
                    complete_year_temps.append(avgDay)
                except:
                    continue
        sDs.append(pylab.std(complete_year_temps))
    return pylab.array(sDs)

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    RMSE = []
    for f in models:
        pylab.figure()
        yVals = pylab.polyval(f, x)
        RMSE = rmse(y,yVals)
        pylab.plot(x,y,'.b')
        pylab.plot(x,yVals,'-r')
        pylab.title('Degree: ' + str(len(f)-1) + '\n' +'RMSE: '\
                    + str(round(RMSE,4)))
        pylab.xlabel('Years')
        pylab.ylabel('Temperatures')


if __name__ == '__main__':


    # Part A.4
    data = Climate('data.csv')
    temps = []
    for year in TRAINING_INTERVAL:
        temps.append(data.get_daily_temp('NEW YORK', 1, 10, year))
    tra = pylab.array(TRAINING_INTERVAL)
    temps = pylab.array(temps)
    model = generate_models(tra, temps,[1])
    evaluate_models_on_training(tra,temps,model)
    
    tmpAv = []
    for year in TRAINING_INTERVAL:
        temps2 = []
        for m in range(1,13):
            for d in range(1,32):
                try:
                    temps2.append(data.get_daily_temp('NEW YORK', m, d, year))
                except:
                    continue
        tmpAv.append(sum(temps2)/len(temps2))

    tA = pylab.array(tmpAv)
    x = pylab.array(TRAINING_INTERVAL)
    pylab.figure()
    model = generate_models(x, tA, [1])
    evaluate_models_on_training(x,tA, model)
    
    # Part B
    climate = Climate('data.csv')
    citiesAvg = gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)
    pylab.figure()
    tra = pylab.array(TRAINING_INTERVAL)
    model = generate_models(tra,citiesAvg , [1])
    evaluate_models_on_training(tra,citiesAvg, model)

    # Part C
    pylab.figure()
#    tA = pylab.array(tmpAv)
    mov = moving_average(citiesAvg,5) #five year moving averages of the national yearly temps btw 1961-2009
    model = generate_models(x, mov, [1])
    evaluate_models_on_training(x, mov, model)
    
    # Part D.2
    pylab.figure()
    models = generate_models(TRAINING_INTERVAL,mov,[1])
    evaluate_models_on_training(x, mov, models)
    
    pylab.figure()
    models = generate_models(TRAINING_INTERVAL,mov,[2])
    evaluate_models_on_training(x, mov, models)
    
    pylab.figure()
    models = generate_models(TRAINING_INTERVAL,mov,[20])
    evaluate_models_on_training(x, mov, models)
    
    
    
    pylab.figure()
    citiesAvg_test = gen_cities_avg(climate, CITIES, TESTING_INTERVAL)
    mov_test = moving_average(citiesAvg_test,5)
    evaluate_models_on_testing(TESTING_INTERVAL,mov_test,models)
    
    # Part E
    pylab.figure()
    sDs = gen_std_devs(climate, CITIES, TRAINING_INTERVAL)
    mov_sd = moving_average(sDs,5)
    model = generate_models(TRAINING_INTERVAL ,sDs, [1])
    evaluate_models_on_training(tra,sDs, model)

