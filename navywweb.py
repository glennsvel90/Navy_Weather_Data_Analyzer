from datetime import date
from urllib import request

BASE_URL = 'http://lpo.dt.navy.mil/data/DM'

def get_data_for_date(date):
    ''' Return a generator of dicts of weather data for specified date '''
    
    if date.year < 2007:
        return _get_data_pre2007(date)
    else:
        return _get_data_post2006(date)

def _get_data_pre2007(date):
    """ Return a generator of dicts of weather data scraped for each year from 2002 to 2006. """
    #the data is obtained from one file for each year.

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

def _get_data_post2006(date):
    ''' Return a generator of dicts of weather data scraped for each year after 2006. ''' 
    # Data is contained in sub-directories of years and then days.'''

#for the following line, the datetime string rendered form has hypens between number
#thus I convert those to underscores to process for the url
    url = '{}/{}/{}'.format(BASE_URL, date.year, str(date).replace('-','_'))
    data = dict(Air_Temp = [], Barometric_Press = [], Wind_Speed = [])

    print('Fetching online data for {}'.format(date))
    for key in data.keys():
        try:
            data[key] = request.urlopen('{}{}'.format(url,key)).read().decode(encoding='utf_8').split('\n')
        except:
            raise ValueError(date)
        else:
            data[key].pop()

    for i in range(len(data['Air_Temp'])):
        timestamps = []
        for k in data.keys():
            timestamps.append(data[k][i].split()[1])
        if timestamps[1:] != timestamps[:1]:
            raise ValueError(date)

        yield dict (Date = data['Air_Temp'][i].split()[0],
                    Time = data['Air_Temp'][i].split()[1],
                    Status = 'PARTIAL' if data == date.today() else 'COMPLETE',
                    Air_Temp = data['Air_Temp'][i].split()[2],
                    Barometric_Press = data['Barometric_Press'][i].split()[2],
                    Wind_Speed = data['Wind_Speed'][i].split()[2])
