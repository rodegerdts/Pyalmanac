# Pyalmanac-Py2

Pyalmanac is a Python 2.7 script that creates the daily pages of the Nautical Almanac. These are tables that are needed for celestial navigation with a sextant. Although you are strongly advised to purchase the official Nautical Almanac, this program will reproduce the tables with no warranty or guarantee of accuracy.

Pyalmanac-Py2 was developed based on the original Pyalmanac by Enno Rodegerdts. Various improvements, enhancements and bugfixes (listed below) are implemented. Pyalmanac contains its own star database (similar to the database in PyEphem 3.7.6), however the accuracy was poor. It is updated with data from the Hipparcos Catalogue and the GHA/Dec data now matches a sample page from a Nautical Almanac exactly or at the most is within 0°0.1', which is very good.

NOTE: two scripts are included (both can be run): 'pyalmanac.py' and 'increments.py'  
NOTE: Pyalmanac contains it's own star database - it does not use the version supplied with PyEphem, hence updating from 3.7.6 to 3.7.7 is harmless. Star names are chosen to comply with Nautical Almanacs.  
NOTE: a Python 3 script with identical functionality can be found at: https://github.com/aendie/Pyalmanac-Py3  
NOTE: a [Skyfield](https://rhodesmill.org/skyfield/) version of Pyalmanac is available here: https://github.com/aendie/SFalmanac-Py2

This fork of the original code, which can be found at https://github.com/rodegerdts/Pyalmanac, in general includes:

* **various bugfixes** (in accordance with USNO data), e.g. ...  
     - a declination of 20°60.0 now prints as 21°00.0;  
     - the same applies to times ('03:60' now prints as '04:00');  
     - incorrect date display in the **SHA and Mer.pass** section;  
     - some incorrect/missing dates for sunrise/sunset or moonrise/moonset;  
     - a few incorrect dates for Moon (upper) Transit or Antitransit (lower);  
     - incorrect times (by 1 minute) for Moon (upper) Transit or Antitransit (lower) due to truncation instead of rounding (506 such cases in 2019);  
     - a Mer. Pass. of '6:15:' now prints correctly as '06:15';  
     - an event occuring within 30 seconds before midnight now lists as 00:00 the next day.

* **enhanced functionality**, e.g. ...  
     - more accurate star database (based on the Hipparcos Catalogue);  
     - user input checks are performed when entering the requested data;  
     - a brief version of the tables can be created instead of the whole year;  
     - a '**modern**' table format in addition to the 'traditional' format layout;  
     - **three Moonrise/Moonset** events per day can be shown (e.g. on 7th July 2019 at 70°N);  
     - temporary files are deleted after running 'increments.py'.

* **cosmetic improvements**, e.g. ...  
     - Declinations/Latitudes are N/S instead of positive and negative;  
     - Declinations are always printed with two digits for degrees;  
     - line spacing (row padding) within the tables has been improved;  
     - minor table header improvements;  
     - addition of the minutes symbol on the Moon’s v, d and HP data rows.

* **a few typo corrections**

and the results have been crosschecked with USNO data to some extent.  
(Constructive feedback is always appreciated.)

**UPDATE: Aug 2019**

This includes a minor bugfix, improved and standardised output formatting, and cosmetic enhancements to the code. The idea is to have the same output formatting for both the PyEphem-based and Skyfield-based versions. If both are opened in a PDF reader, then simply by switching between tabs will highlight the data that has changed. Also one can now generate multiple years of almanacs with a single run. And output messages can be sent to the console or written to a log file if the log file has been opened.

**UPDATE: Nov 2019**

Declination formatting has been changed to the standard used in Nautical Almanacs. In each 6-hour block of declinations, the degrees value is only printed on the first line if it doesn't change. It is printed whenever the degrees value changes. The fourth line has two dots indicating "ditto". This applies to all planet declinations and for the sun's declination, but not to the moon's declination as this is continuously changing.

This also includes some very minor changes and an improved title page for the full almanac with a star chart that indicates the northern navigational stars.

## Requirements

&nbsp;&nbsp;&nbsp;&nbsp;Most of the computation is done by the free Pyephem library.  
&nbsp;&nbsp;&nbsp;&nbsp;Typesetting is done by LaTeX or MiKTeX so you first need to install:

* Python v2.x (2.6 or later)
* PyEphem
* TeX/LaTeX&nbsp;&nbsp;or&nbsp;&nbsp;MiKTeX

&nbsp;&nbsp;&nbsp;&nbsp;**DEPRECATION:** Python 2.7 will reach the end of its life on January 1st, 2020.  
&nbsp;&nbsp;&nbsp;&nbsp;Please upgrade your Python as Python 2.7 won't be maintained after that date.  
&nbsp;&nbsp;&nbsp;&nbsp;A future version of pip will drop support for Python 2.7.

### INSTALLATION GUIDELINES on Windows 10:

&nbsp;&nbsp;&nbsp;&nbsp;Install Python 2.7 and MiKTeX from https://miktex.org/  
&nbsp;&nbsp;&nbsp;&nbsp;Run Command Prompt as Administrator, go to your Python Scripts folder and execute, e.g.:

&nbsp;&nbsp;&nbsp;&nbsp;**cd C:\\Python27\\Scripts**  
&nbsp;&nbsp;&nbsp;&nbsp;**pip install pyephem**

&nbsp;&nbsp;&nbsp;&nbsp;NOTE: if Python 3 is already installed, you need to be in the Scripts folder - otherwise the Py3 version of pip will execute.

&nbsp;&nbsp;&nbsp;&nbsp;Put the Pyalmanac files in any folder, go there and start with:  
&nbsp;&nbsp;&nbsp;&nbsp;**python.exe pyalmanac.py**

&nbsp;&nbsp;&nbsp;&nbsp;However, if Python 3 is also installed, start with:  
&nbsp;&nbsp;&nbsp;&nbsp;**py -2 pyalmanac.py**


### INSTALLATION GUIDELINES on Linux:

&nbsp;&nbsp;&nbsp;&nbsp;Install your platform's Python- and LaTeX distribution.  
&nbsp;&nbsp;&nbsp;&nbsp;Remember to choose python 2.7 minimum and install all development header files.  
&nbsp;&nbsp;&nbsp;&nbsp;Run at the command line:

&nbsp;&nbsp;&nbsp;&nbsp;**pip install pyephem**

&nbsp;&nbsp;&nbsp;&nbsp;Put the Pyalmanac files in any directory and start with:  
&nbsp;&nbsp;&nbsp;&nbsp;**python pyalmanac**  
&nbsp;&nbsp;&nbsp;&nbsp;or  
&nbsp;&nbsp;&nbsp;&nbsp;**./pyalmanac**


### INSTALLATION GUIDELINES on MAC:

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
