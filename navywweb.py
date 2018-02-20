from datetime import date
from urllib import request

BASE_URL = 'http://lpo.dt.navy.mil/data/DM'

def get_data_for_date(date):
    ''' Returns a generator of dicts of weather data for specified date'''
    if date.year < 2007:
        return _get_data_pre2007(date)
    else:
        return _get_data_post2006(date)

def _get_data_pre2007(date):
    '''Returns a generator of dicts of weather data for each year. For years from 2002 to 2006,
    the data is contained in one file for each year'''

    
