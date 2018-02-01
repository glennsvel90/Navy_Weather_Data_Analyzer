from tkinter import *
from tkinter import ttk, messagebox
from statistics import mean, median
from datetime import date

#import IpoDB


class NavyWApp:

    def __init__(self, master):

        master.title('Navy Weather Data Analyzer')
        master.resizable(False, False)
        master.configure(background = '#CAC9FB')

        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#CAC9FB')
        self.style.configure('TButton', font=('Helvetica',11, 'bold'))
        self.style.configure('TLabel', background = '#CAC9FB', font=('Helvetica',12, 'bold'))



        self.frameheader = ttk.Frame(master)
        self.frameheader.pack()

        self.logo = PhotoImage(file ='/home/userlin/Dropbox/dropubun/Navy_Weather_Data_Analyzer/lpo_logo.gif')

        ttk.Label(self.frameheader, image = self.logo).grid(row = 0, column= 0, columnspan = 2)


        self.framebody = ttk.Frame(master)
        self.framebody.pack()

        ttk.Label(self.framebody, text= 'Start Date:').grid(row=0, column=0,
                                                            columnspan= 3, padx= (15, 0), sticky='sw')
        # self.cmonths= cycle(Jan, Feb, Mar, Apr, May,
        #              Jun, Jul, Aug, Sep, Oct,Nov, Dec)

        self.months= ('Jan', 'Feb', 'Mar', 'Apr', 'May',
                      'Jun', 'Jul', 'Aug,', 'Sep', 'Oct','Nov', 'Dec')

        # self.months= ('Jan', 'Feb', 'Mar', 'Apr', 'May',
        #                    'Jun', 'Jul', 'Aug,', 'Sep', 'Oct','Nov', 'Dec')

        self.smonth = StringVar()
        self.smspinbox = Spinbox(self.framebody, textvariable = self.smonth, width = 4,
                                 font = 'Helvetica 11')
        self.smspinbox.grid(row = 1, column = 0, padx=(15, 0))


        self.smspinbox.config(values = (self.months))
        # self.smspinbox.config(values = self.months)
        self.smonth.set(self.months[date.today().month-1])




        self.sdaynum = StringVar()
        self.sdspinbox = Spinbox(self.framebody, from_= 1, to = 31,
                                 textvariable = self.sdaynum, width= 2,
                                 font = 'Helvetica 11')
        self.sdspinbox.grid(row = 1, column = 1)
        self.sdaynum.set(date.today().day)


        self.syear = StringVar()
        self.sylimit = date.today().year
        self.syspinbox = Spinbox(self.framebody, from_= 2001, to = self.sylimit,
                                 textvariable = self.syear, width= 4, font = 'Helvetica 11')
        self.syspinbox.grid(row = 1, column = 2)
        self.syear.set(date.today().year)



        self.emonth = StringVar()
        self.emspinbox = Spinbox(self.framebody, textvariable = self.emonth, width= 4,
                                 font = 'Helvetica 11')
        self.emspinbox.grid(row = 1, column = 4, padx=(30, 0))
        self.emspinbox.config(values = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                        'Jul', 'Aug,' 'Sep', 'Oct', 'Dec'))

        self.emonth.set(self.months[date.today().month-1])


        self.edaynum = StringVar()
        self.edspinbox = Spinbox(self.framebody, from_= 1, to = 31, textvariable = self.edaynum,
                                 width= 2, font = 'Helvetica 11')
        self.edspinbox.grid(row = 1, column = 5)
        self.edaynum.set(date.today().day)


        self.eyear = StringVar()
        self.eylimit = date.today().year
        self.espinbox = Spinbox(self.framebody, from_= 2001, to = self.eylimit,
                                textvariable = self.eyear, width= 4, font = 'Helvetica 11')
        self.espinbox.grid(row = 1, column = 6, padx= (0, 15))

        self.eyear.set(date.today().year)


        ttk.Label(self.framebody, text= 'End Date:').grid(row=0, column=4, columnspan= 3, padx= (30, 0), sticky='sw')


        ttk.Button(master, text = "Submit", command = self.submit).pack(pady = (5,5))

        self.frameresults = ttk.Frame(master, width=70, height=70)
        self.frameresults.pack(padx=(10, 10), pady=(10,10))


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


        #
        # ttk.Label(self.frameresults, text='Air\nTemperature', justify= CENTER, borderwidth=2, width=12,
        #           relief="groove").grid(row=0, column=1, sticky='s',padx=(0, 15))
        # ttk.Label(self.frameresults, text='Wind\nSpeed', justify= CENTER, borderwidth=2, relief="groove").grid(row=0, column=2, sticky='s', padx=(0, 15))
        # ttk.Label(self.frameresults, text='Barometric\nPressure',justify= CENTER, borderwidth=2, relief="groove").grid(row=0, column=3,
        #                                                                                padx=(0, 15), sticky='s')
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

        data = list(self.database.get_data_for_range(start, end))

        if data != []:


            dict_of_lists = dict(Air_Temp = [], Barometric_Press = [], Wind_Speed = [])

            for entry in data:
                for key in dict_of_lists.keys():
                    dict_of_lists[key].append(entry[key])

            result = {}
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

        else:
            self.frameresults.forget()



    def _safe_close(self):
        """When the GUI is closed

#CAC9FB
def main():

    root = Tk()

    app = NavyWApp(root)

    root.mainloop()



if __name__ == "__main__": main()
