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
        self.db.execute("""CREATE TABLE IF NOT EXIST {} (Date TEXT, time TEXT, status Text, Air_Temp FLOAT,
                            Barometric Press FLOAT, Wind_Speed FLOAT""".format(self.table))
