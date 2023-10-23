# Navy_Weather_Data_Analyzer

**Note:** Navy Weather Base Data Server (http://lpo.dt.navy.mil/data/DM) has gone offline, thus application is unable to run to completion. Check the github repository for sample data downloaded for experimentation. Snapshots of data are also provided for understanding data layout.

The U.S. Navy uses weather data to make informed decisions about submarine training protocols. This application helps solves the problem of Navy researchers' need for key information about the weather's air temperature, barometric pressure, and wind speed for a range of dates at a navy base research area, Lake Pend Oreille. This web application calculates and presents the mean and median of Navy weather data collected. It presents a graphical user interface to input date ranges. A sqlite3 database is initiated and data is downloaded, cached, and managed for dates requested.

## Getting Started

### Prerequisites

* Python 3.4 or later  (Statistics Module is included in this version)


### Installing

Clone the repository and unzip the contents. Open your computer terminal and change directory to be located inside the repository.

### Running

Type in the terminal:
```
python NavyWApp.py
```

## GUI Preview  

![alt text](https://github.com/glennsvel90/Navy_Weather_Data_Analyzer/blob/master/GUI_preview.PNG "GUI Preview")

## Methodology

The application consists of three modules: NavyWAPP, NavyWDB, and NavyWWEB

1. NavyWAPP module creates the GUI to input request. The module creates and stores a database object
2. The module validates requested dates to make sure they exist in correct limits
3. The module makes calls to the database module(NavyWDB), which manages the database,
4. The NavyWDB module determines which dates have complete/incomplete data available in the database. For dates with complete or partial  data, module
will use the NavyWWEB module to download the weather data for that date from the navy website
5. The NavyWDB module will cache the downloaded data into the database for future use
6. The module will then return all of the data for the requested range of dates to the NavyWAPP module
7. The NavyWAPP module calculates the mean and median of the requested dataset
8. The module finally displays the results to the user interface.


## Limitations

The are some varying data for the same dates. When errors did occur for the downloading of certain dates, a warning message is shown with the specific dates that
had problems being downloaded. These dates let the user know dates that was not incorporated in the database and thus, not included in the final result.
