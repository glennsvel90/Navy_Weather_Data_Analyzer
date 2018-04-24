from tkinter import *
from tkinter import ttk, messagebox
from statistics import mean, median
from datetime import date
import NavyWDB


class NavyWAPP:
    """
    This is a GUI module for the Navy Weather Data Application. The module retrieves data for
    requested date ranges from the NavyWDB module
    """

    def __init__(self, master):

        #store the tkinter top level window object as an internal variable called master
        self.master = master

        #
        self._makeGUI()

        #create and store a database object from the NavyWDB module
        self.database = NavyWDB.NavyWDB()

        #configures master to closing application event to safely close database before closing master window of gui
        self.master.protocol("WM_DELETE_WINDOW", self._safe_close)

    def _makeGUI(self):
        """
        Initiates the graphical user interface that displays date input parameters
        """

        self.master.title('Navy Weather Data Analyzer')
        self.master.resizable(False, False)
        self.master.configure(background = '#CAC9FB')

        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#CAC9FB')
        self.style.configure('TButton', font=('Helvetica',11, 'bold'))
        self.style.configure('TLabel', background = '#CAC9FB', font=('Helvetica',12, 'bold'))


        #creates gui header
        self.frameheader = ttk.Frame(self.master)
        self.frameheader.pack()

        self.logo = PhotoImage(file ='/home/userlin/Dropbox/dropubun/Navy_Weather_Data_Analyzer/lpo_logo.gif')

        ttk.Label(self.frameheader, image = self.logo).grid(row = 0, column= 0, columnspan = 2)

        #creates gui body where input controls and date boxes are placed
        self.framebody = ttk.Frame(self.master)
        self.framebody.pack()

        ttk.Label(self.framebody, text= 'Start Date:').grid(row=0, column=0,
                                                            columnspan= 3, padx= (15, 0), sticky='sw')


        self.months = ('Jan', 'Feb', 'Mar', 'Apr', 'May',
                      'Jun', 'Jul', 'Aug,', 'Sep', 'Oct','Nov', 'Dec')

        #store starting date month input values as string variables
        self.smonth = StringVar()
        self.smspinbox = Spinbox(self.framebody, textvariable = self.smonth, width = 4,
                                 font = 'Helvetica 11')
        self.smspinbox.grid(row = 1, column = 0, padx=(15, 0))
        self.smspinbox.config(values = (self.months))
        self.smonth.set(self.months[date.today().month-1])


        #store starting date day imput values as string variables
        self.sdaynum = StringVar()
        self.sdspinbox = Spinbox(self.framebody, from_= 1, to = 31,
                                 textvariable = self.sdaynum, width= 2,
                                 font = 'Helvetica 11')
        self.sdspinbox.grid(row = 1, column = 1)
        self.sdaynum.set(date.today().day)

        #store starting date year input values as string variables
        self.syear = StringVar()
        self.sylimit = date.today().year
        self.syspinbox = Spinbox(self.framebody, from_= 2001, to = self.sylimit,
                                 textvariable = self.syear, width= 4, font = 'Helvetica 11')
        self.syspinbox.grid(row = 1, column = 2)
        self.syear.set(date.today().year)


        #store ending date month input values as string variables
        self.emonth = StringVar()
        self.emspinbox = Spinbox(self.framebody, textvariable = self.emonth, width= 4,
                                 font = 'Helvetica 11')
        self.emspinbox.grid(row = 1, column = 4, padx=(30, 0))
        self.emspinbox.config(values = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                        'Jul', 'Aug,' 'Sep', 'Oct', 'Dec'))
        self.emonth.set(self.months[date.today().month-1])

        #store ending date day input values as string variables
        self.edaynum = StringVar()
        self.edspinbox = Spinbox(self.framebody, from_= 1, to = 31, textvariable = self.edaynum,
                                 width= 2, font = 'Helvetica 11')
        self.edspinbox.grid(row = 1, column = 5)
        self.edaynum.set(date.today().day)

        #store ending date year input values as string variables
        self.eyear = StringVar()
        self.eylimit = date.today().year
        self.espinbox = Spinbox(self.framebody, from_= 2001, to = self.eylimit,
                                textvariable = self.eyear, width= 4, font = 'Helvetica 11')
        self.espinbox.grid(row = 1, column = 6, padx= (0, 15))

        self.eyear.set(date.today().year)


        ttk.Label(self.framebody, text= 'End Date:').grid(row=0, column=4, columnspan= 3, padx= (30, 0), sticky='sw')

        #create the submit button to call the submit function
        ttk.Button(self.master, text = "Submit", command = self.submit).pack(pady = (5,5))

        self.frameresults = ttk.Frame(self.master, width=70, height=70)
        self.frameresults.pack(padx=(10, 10), pady=(10,10))

        #create a frame to populate the resulting mean, median, mode weather data
        fat = Frame(self.frameresults,width=66,height=50)
        fat.grid(row=0,column=1,padx=(5,5),sticky="s")
        fat.grid_propagate(0)
        fat.update()
        lat = Label(fat,text="Wind\nSpeed",font = 'Helvetica 12 bold')
        lat.place(x=30, y=25, anchor="center")

        fws = Frame(self.frameresults,width=115,height=50)
        fws.grid(row=0,column=2,padx=(5,5), sticky="s")
        fws.grid_propagate(0)
        fws.update()
        lws = Label(fws,text="Air\nTemperature", font = 'Helvetica 12 bold')
        lws.place(x=55, y=25, anchor="center")

        fbp = Frame(self.frameresults,width=100,height=50)
        fbp.grid(row=0,column=3,padx=(5,5), sticky="s")
        fbp.grid_propagate(0)
        fbp.update()
        lbp = Label(fbp,text="Barometric\nPressure", font = 'Helvetica 12 bold')
        lbp.place(x=50, y=25, anchor="center")



        ttk.Label(self.frameresults, text='Mean:').grid(row=1, column=0, sticky='e')
        ttk.Label(self.frameresults, text='Median:').grid(row=2, column=0, sticky='e')

        self.air_temp_mean = StringVar()
        self.air_temp_median = StringVar()
        self.barometric_press_mean = StringVar()
        self.barometric_press_median = StringVar()
        self.wind_speed_mean = StringVar()
        self.wind_speed_median = StringVar()

        ttk.Label(self.frameresults, textvariable = self.air_temp_mean).grid(row = 1, column =2)
        ttk.Label(self.frameresults, textvariable = self.air_temp_median).grid(row = 2 , column =2)
        ttk.Label(self.frameresults, textvariable = self.barometric_press_mean).grid(row = 1, column =3)
        ttk.Label(self.frameresults, textvariable = self.barometric_press_median).grid(row = 2 , column =3)
        ttk.Label(self.frameresults, textvariable = self.wind_speed_mean).grid(row = 1 , column =1)
        ttk.Label(self.frameresults, textvariable = self.wind_speed_median).grid(row = 2 , column =1)



    def submit(self):
        """
        Obtain the mean and median weather data parameters for the specified date range
        """
        #try to get the day, month, and year, converting those into a datetime object.
        #throw and error if actual real dates are not used as inputs, and reset the date values to
        #day of today
        try:
            start = date(int(self.syear.get()),
                         self.months.index(self.smonth.get()) + 1,
                                           int(self.sdaynum.get()))
            end = date(int(self.eyear.get()),
                       self.months.index(self.emonth.get())+1,
                       int(self.edaynum.get()))

        except ValueError as e:
            messagebox.showerror(title='ValueError',
                                 message=('Invalid Date:\n'
                                          'Correct format is "month DD YYYY" '))
            self.sdaynum.set(date.today().day)
            self.smonth.set(self.months[date.today().month-1])
            self.syear.set(date.today().year)
            self.edaynum.set(date.today().day)
            self.emonth.set(self.months[date.today().month-1])
            self.eyear.set(date.today().year)
            return


        #check that date range is correct
        if (start < date(2001, 1, 12)) or (end > date.today()) or (start > end):
            messagebox.showerror(title = 'ValueError', message = ('INVALID DATE RANGE\nStart Date: {}\nEnd Date: {}\n'
                                                                  'Dates must be between 2001-1-12 and {}.\n'
                                                                  'Start Date must be <= End Date.').format(start, end, date.today()))
            return
        #retrieve weather data to calculate statistics, all by calling a method to return a generator object with a dictionary
        #containing each of the 3 types of weather data for requested range of dates. The generator object of dicts is converted
        #into a list of dicts
        data = list(self.database.get_data_for_range(start, end))

        #check if data was retrieved from the cached database
        if data != []:

            #processing data
            dict_of_lists = dict(Air_Temp = [], Barometric_Press = [], Wind_Speed = [])


            # for each dictionary entry in list "Data", concerning the key for the list of dicts, append to the right list according
            #to the corresponding key, the value of the dictionary entry using the same spelt key names in the list "Data"
            for entry in data:
                for key in dict_of_lists.keys():
                    dict_of_lists[key].append(entry[key])

            result = {}

            # for --value of the results[key]--(value of a certain key in the results dictionary) make the value equal to the
            # dictionary containing: 1)the mean equal to the mean calculated from the corresponding key's values(list of specific type
            # of weather data results with each row a new date's data result for the corresponding key, 2) the median equal to the
            # median calculated from the corresponding key's values (list of specific type of weather data results with each row a
            # new date's data result for the corresponding key,
            for key in dict_of_lists.keys():
                result[key] = dict(mean = mean(dict_of_lists[key]),
                                   median = median(dict_of_lists[key]))

            self.air_temp_mean.set('{0:.2f}'.format(result['Air_Temp']['mean']))
            self.air_temp_median.set('{0:.2f}'.format(result['Air_Temp']['median']))
            self.barometric_press_mean.set('{0:.2f}'.format(result['Barometric_Press']['mean']))
            self.barometric_press_median.set('{0:.2f}'.format(result['Barometric_Press']['median']))
            self.wind_speed_mean.set('{0:.2f}'.format(result['Wind_Speed']['mean']))
            self.wind_speed_median.set('{0:.2f}'.format(result['Wind_Speed']['median']))

            self.frameresults.pack(side = TOP)

        # hide the the resulting frame if data is not retreived yet, this prevents user from seeing left over results
        # from a previous query and misinterpret them as valid results when actually no data was retreived
        else:
            self.frameresults.forget()



    def _safe_close(self):
        """When the GUI is closed, this is run to properly shut down the database before closing the GUI"""

        self.database.close()
        self.master.destory()

#CAC9FB
def main():

    root = Tk()

    app = NavyWApp(root)

    root.mainloop()



if __name__ == "__main__": main()
