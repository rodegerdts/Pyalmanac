# Pyalmanac 

Pyalmanac is a Python 2.7 script that creates the daily pages of the Nautical Almanac. These are tabels that are needed for celestial navigation with a sextant. Although you are strongly advised to purchase the official Nautical Almanac, this program will reproduce the tables with no warranty or guarantee of accuracy.  

NOTE: two scripts are included (both can be run): 'pyalmanac.py' and 'increments.py'  
NOTE: a Python 3.7 script with identical functionality can be found at: (...)  
NOTE: a Skyfield version of Pyalmanac is under development.

This fork of the original code, which can be found at https://github.com/rodegerdts/Pyalmanac in general includes:

* **various bugfixes** (in accordance with USNO data), e.g. ...  
     a declination of 20°60.0 now prints as 21°00.0;  
     the same applies to times ('03:60' now prints as '04:00');  
     incorrect date display in the **SHA and Mer.pass** section;  
     some incorrect/missing dates for sunrise/sunset or moonrise/moonset;  
     a few incorrect dates for Moon (upper) Transit or Antitransit (lower);  
     incorrect times (by 1 minute) for Moon (upper) Transit or Antitransit (lower) due to truncation instead of rounding (506 such cases in 2019);  
     a Mer. Pass. of '6:15:' now prints correctly as '06:15';  
     an event occuring within 30 seconds before midnight now lists as 00:00 the next day.

* **enhanced functionality**, e.g. ...  
     user input checks are performed when entering the requested data;  
     a brief version of the tables can be created instead of the whole year;  
     a '**modern**' table format in addition to the 'traditional' format layout;  
     **three Moonrise/Moonset** events per day can be shown (e.g. on 7th July 2019 at 70°N);  
     temporary files are deleted after running 'increments.py'.

* **cosmetic improvements**, e.g. ...  
     Declinations/Latitudes are N/S instead of positive and negative;  
     Declinations are always printed with two digits for degrees;  
     line spacing (row padding) within the tables has been improved;  
     table header improvements;  
     addition of the minutes symbol on the Moon’s v, d and HP data rows.

* **a few typo corrections**

and the results have been crosschecked with USNO data to some extent.  
(Constructive feedback is always appreciated.)
  

## Requirements

Most of the heavy computing is done by the free Pyephem library. Typesetting is done by TeX/LaTeX So before you can use this program you need to install:

* Python v2.x (2.6 or later ) python 3 will not work out of the box
* PyEphem
* TeX/LaTeX
  

### INSTALLATION on Linux:

    Install your platforms Python- and LaTeX distribution. Remember to chose python 2.7 minimum and install all develpment header files. Run at the command line:

    pip install pyephem

    Put the Pyalmanac files in any directory and start with:

    python pyalmanac  
    or  
    ./pyalmanac


### INSTALLATION on MAC:

    Every Mac comes with python preinstalled. (Please choose the Python 3.7 version of Pyalmanac if Python 3.* is installed.) You need to install the PyEphem library to use Pyalmanac. Type the following commands at the commandline (terminal app):

    sudo easy_install pip
    pip install pyephem

    If this command fails your mac asks you if you would like to install the header files. Do so, you do not need to install the full IDE. Try again.

    Install TeX/LaTeX from http://www.tug.org/mactex/

    Now you are almost ready. Put the Pyalmanac files in any directory and start with 

    python pyalmanac  
    or  
    ./pyalmanac
