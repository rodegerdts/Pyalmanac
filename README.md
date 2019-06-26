# Pyalmanac

Pyalmanac is a Python 2.7 script that creates the daily pages of the Nautical Almanac. These are tables that are needed for celestial navigation with a sextant. Although you are strongly advised to purchase the official Nautical Almanac, this program will reproduce the tables with no warranty or guarantee of accuracy.  

NOTE: two scripts are included (both can be run): 'pyalmanac.py' and 'increments.py'  
NOTE: a Python 3.7 script with identical functionality can be found at: https://github.com/aendie/Py3almanac  
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

&nbsp;&nbsp;&nbsp;&nbsp;Most of the computation is done by the free Pyephem library.  
&nbsp;&nbsp;&nbsp;&nbsp;Typesetting is done by TeX/LaTeX so you first need to install:

* Python v2.x (2.6 or later )
* PyEphem
* TeX/LaTeX&nbsp;&nbsp;or&nbsp;&nbsp;MiKTeX
  

### INSTALLATION on Windows 10:

&nbsp;&nbsp;&nbsp;&nbsp;Install Python 2.7 and MiKTeX from https://miktex.org/  
&nbsp;&nbsp;&nbsp;&nbsp;Run at the command line:

&nbsp;&nbsp;&nbsp;&nbsp;**pip install pyephem**

&nbsp;&nbsp;&nbsp;&nbsp;Put the Pyalmanac files in any directory and start with:  
&nbsp;&nbsp;&nbsp;&nbsp;**python.exe pyalmanac.py**

&nbsp;&nbsp;&nbsp;&nbsp;However, if Python 3 is also installed, start with:  
&nbsp;&nbsp;&nbsp;&nbsp;**py -2 pyalmanac.py**


### INSTALLATION on Linux:

&nbsp;&nbsp;&nbsp;&nbsp;Install your platform#'s Python- and LaTeX distribution.  
&nbsp;&nbsp;&nbsp;&nbsp;Remember to choose python 2.7 minimum and install all development header files.  
&nbsp;&nbsp;&nbsp;&nbsp;Run at the command line:

&nbsp;&nbsp;&nbsp;&nbsp;**pip install pyephem**

&nbsp;&nbsp;&nbsp;&nbsp;Put the Pyalmanac files in any directory and start with:  
&nbsp;&nbsp;&nbsp;&nbsp;**python pyalmanac**  
&nbsp;&nbsp;&nbsp;&nbsp;or  
&nbsp;&nbsp;&nbsp;&nbsp;**./pyalmanac**


### INSTALLATION on MAC:

&nbsp;&nbsp;&nbsp;&nbsp;Every Mac comes with python preinstalled.  
&nbsp;&nbsp;&nbsp;&nbsp;(Please choose the Python 3.7 version of Pyalmanac if Python 3.* is installed.)  
&nbsp;&nbsp;&nbsp;&nbsp;You need to install the PyEphem library to use Pyalmanac.  
&nbsp;&nbsp;&nbsp;&nbsp;Type the following commands at the commandline (terminal app):

&nbsp;&nbsp;&nbsp;&nbsp;**sudo easy_install pip**  
&nbsp;&nbsp;&nbsp;&nbsp;**pip install pyephem**

&nbsp;&nbsp;&nbsp;&nbsp;If this command fails, your Mac asks you if you would like to install the header files.  
&nbsp;&nbsp;&nbsp;&nbsp;Do so - you do not need to install the full IDE - and try again.

&nbsp;&nbsp;&nbsp;&nbsp;Install TeX/LaTeX from http://www.tug.org/mactex/

&nbsp;&nbsp;&nbsp;&nbsp;Now you are almost ready. Put the Pyalmanac files in any directory and start with:  
&nbsp;&nbsp;&nbsp;&nbsp;**python pyalmanac**  
&nbsp;&nbsp;&nbsp;&nbsp;or  
&nbsp;&nbsp;&nbsp;&nbsp;**./pyalmanac**
