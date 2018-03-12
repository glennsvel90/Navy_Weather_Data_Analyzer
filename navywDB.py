from datetime import date, datetime, timedelta
from tkinter import messagebox
import sqlite3
import NavyWWeb


class NavyWDB():
    """
    Creates and manages a database that stores local cache of all weather data that's been downloaded from the internet
    """

    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename', 'navyw.db')
        self.table = kwargs.get('table', 'weather')

        #open a database, or create a new one if none is found.Store the reference to the database in the class db variable
        self.db = sqlite3.connect(self.filename)
        self.db.row_factory = sqlite3.Row

        # if table does not exist, will create a new table with the following columns
        self.db.execute("""CREATE TABLE IF NOT EXIST {} (Date TEXT, Time TEXT, Status Text, Air_Temp FLOAT,
                            Barometric Press FLOAT, Wind_Speed FLOAT""".format(self.table))

    def get_data_for_range(self, start, end):
        """
        Using the start and end dates, returns a generator of dictionaries that have all weather data, such as Wind Speed,
        Barometric Pressure, and Wind Speed in those dates. This funtion is called by the NavyWApp module
        """

        # aim to obtain a list of dates that need updating in the database
        dates_to_update = []

        #find pre-2007 dates to update and add to list to be dates to be updated by if a year's data should be updated by
        # checking if there is no data for a Jan 12 date in the given year in the database
        #

        for year in range(start.year, 2007):
            if list(self._get_status_for_range(date(year,1,12), date(year,1,12))) == []:
                dates_to_update.append(date(year,1,12))

        #find post-2006 dates to update and add to list to be the dates to be updated by if

        if (end.year > 2006) and (start >= date(2007,1,1)):
            temp_start = start
        elif (end.year > 2006) and (start < date(2007,1,1)):
            temp_start = date(2007,1,1)
        else:
            temp_start = end

        #obtains a list of dates between -temp_start and end for dates post 2006

        delta = end - temp_start
        for d in range(delta.days +1):
            dates_to_update.append(temp_start + timedelta(days=d))

        # convert the dictionary of dictionaries that comes out from using the "get status for range" function
        # into a list of dictionaries of containing the key date and its value, and the
        # key status and it's value
        statuses = list(self._get_status_for_range(temp_start, end))

        # for each dictionary in statuses list, if the key of status is 'complete', remove the datetime object from the list. From the
        # the reading of the database the statuses list created has a string form of the date. Convert that string form date into a datetime
        # in order to specify the removal of the date time from "dates to update list"
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

        # from the multiple records of different timestamps for redunant dates between the start and end date, get one date results.
        # Turn the dates python start and end datetime objects into string text form to be able to be added and be compatible with the database
        cursor = self.db.execute('''SELECT DISTINCT Date, Status FROM {} WHERE Date BETWEEN {} AND {}'''.format(self.table,
                                                                                                                start.strftime(%Y%m%d),
                                                                                                                end.strftime(%Y%m%d)))

        for row in cursor:
            yield dict(row)

    def _update_data_for_date(self, date, partial):
        """
        Uses NavyWWeb module to download data for dates not already in the DB. If partial data exists, then it is deleted and re-downloaded
        completely
        """
        if partial:
            self.db.execute('DELETE FROM {} WHERE DATE = {}'.format(self.table, date.strftime('%Y%m%d')))
            self.db.commit()

        try:
            data = navywweb.get_data_for_date(date)
            except
                raise

        for entry in data:
            self.db.execute('''INSERT INTO {} (Date, Time, Status, Air_Temp, Barometric_Press, Wind_Speed) VALUES (?,?,?,?,?,?)'''.format(self.table),
                                                                                                                                    (entry['Date'].replace("_", ""),
                                                                                                                                    entry['Time'],
                                                                                                                                    entry['Status'],
                                                                                                                                    entry['Air_Temp']
                                                                                                                                    entry['Barometric_Press'],
                                                                                                                                    entry['Wind_Speed']))
        self.db.commit()


    def clear(self):
        """Clears the database by dropping the current table"""
        self.db.execute('DROP TABLE IF EXISTS {}'.format(self.table))


    def close(self):
        """
        closes the database in a safe way and delete the filename reference to it
        """
        self.db.close()
        del self.filename
