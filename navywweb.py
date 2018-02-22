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

    url = '{}/Environmental_Data_{}/'.format(BASE_URL, date.year)
    print('Fetching online data for {} (full year)'.format(date.year))

    try:
        year_data = request.urlopen(url).read().decode(encoding='utf_8').split('\n')
    except:
        raise ValueError(date)
    else:
        year_data.pop(0)

    for line in year_data:
        elements = line.split()
        yield dict(Date = elements[0],
                   Time = elements[1],
                   Status = 'COMPLETE',
                   Air_Temp = elements[5],
                   Barometric_Press = elements[7],
                   Wind_Speed = elements[2])
