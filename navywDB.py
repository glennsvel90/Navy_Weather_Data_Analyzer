from datetime import date, datetime, timedelta
from tkinter import messagebox
import sqlite3
import NavyWWeb


class NavyWDB():
    """
    A database that stores weather data, such as Wind Speed, Barometric Pressure,
    and Air Temperature
    """

    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename', 'navyw.db')
        self.table = kwargs.get('table', 'weather')
        self.db = sqlite3.connect(self.filename)
        self.db.row_factory = sqlite3.Row
        self.db.execute("""CREATE TABLE IF NOT EXIST {} (Date TEXT, Time TEXT, Status Text, Air_Temp FLOAT,
                            Barometric Press FLOAT, Wind_Speed FLOAT""".format(self.table))

    def get_data_for_range(self, start, end):
        """
        Using the start and end dates, returns a generator of dictionaries that have all weather data, such as Wind Speed,
        Barometric Pressure, and Wind Speed in those dates
        """

        dates_to_update = []

        #find pre-2007 dates to update and add to list

        for year in range(start.year, 2007):
            if list(self._get_status_for_range(date(year,1,12), date(year,1,12))) == []:
                dates_to_update.append(date(year,1,12))

        #find post-2006 dates to update and add to list

        if (end.year > 2006) and (start >= date(2007,1,1)):
            temp_start = start
        elif (end.year > 2006) and (start < date(2007,1,1)):
            temp_start = date(2007,1,1)
        else:
            temp_start = end

        #obtains a list of dates between temp_start and end

        delta = end - temp_start
        for d in range(delta.days +1):
            dates_to_update.append(temp_start + timedelta(days=d))

        statuses = list(self._get_status_for_range(temp_start, end))

        for entry in statuses:
            if entry['Status'] == 'COMPLETE':
                dates_to_update.remove(datetime.strptime(str(entry['Date']), '%Y%m%d').date())
            elif entry['Status'] == 'PARTIAL':
                try:
                    self._update_data_for_date(datetime.strptime(str(entry['Date']), '%Y%m%d').date(), True)
                except:
                    raise
                dates_to_update.remove(datetime.strptime(str(entry['Date']), '%Y%m%d').date())

        error_dates = []
        for day in dates_to_update:
            try:
                self._update_data_for_date(day, False)
            except ValueError as e:
                error_dates.append(e)

        if error_dates != []:
            error_message = "There were problems accessing data for the following dates. They were not included in the results.\n"
            for day in error_dates:
                error_message += '\n{}'.format(day)
                messagebox.showwarning(title='Warning', message=error_message)

        cursor = self.db.execute('''SELECT Air_Temp, Barometric_Press, Wind_Speed FROM {} WHERE Date BETWEEN {} AND {}'''.format(self.table,
                                                                                                                                 start.strftime(%Y%m%d),
                                                                                                                                end.strftime(%Y%m%d)))
        for row in cursor:
            yield dict(row)

    def get_status_for_range(self, start, end):
        """
        Given a start and end date, return a generator of dicts containing the dates and their corresponding status value which
        is entered as either COMPLETE or PARTIAL
        """

        cursor = self.db.execute('''SELECT DISTINCT Date, Status FROM {} WHERE Date BETWEEN {} AND {}'''.format(self.table,
                                                                                                                start.strftime(%Y%m%d),
                                                                                                                end.strftime(%Y%m%d)))

        for row in cursor:
            yield dict(row)
