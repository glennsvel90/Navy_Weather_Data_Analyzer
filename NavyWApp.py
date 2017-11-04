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
        self.smspinbox = Spinbox(self.framebody, textvariable = self.smonth, width = 3,
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
        self.emspinbox = Spinbox(self.framebody, textvariable = self.emonth, width= 3,
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

        self.frameresults = ttk.Frame(master)




    def submit(self):
        pass

#CAC9FB
def main():

    root = Tk()

    app = NavyWApp(root)

    root.mainloop()



if __name__ == "__main__": main()
