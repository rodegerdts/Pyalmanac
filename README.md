# Pyalmanac (Python 3 version)

Pyalmanac is a **Python 3** script that creates the daily pages of the Nautical Almanac. These are tables that are needed for celestial navigation with a sextant. Although you are strongly advised to purchase the official Nautical Almanac, this program will reproduce the tables with no warranty or guarantee of accuracy.

This version of Pyalmanac was developed by Andrew Bauer based on the original Pyalmanac by Enno Rodegerdts. Various improvements, enhancements and bugfixes have been included. 
Pyalmanac contains its own star database (similar to the database in PyEphem 3.7.6), however the accuracy was poor. It is updated with data from the Hipparcos Catalogue and the GHA/Dec data now matches a sample page from a Nautical Almanac typically within 0°0.1'.

NOTE: two scripts are included (both can be run): 'pyalmanac.py' and 'increments.py'  
NOTE: Pyalmanac contains its own star database - it does not use the version supplied with PyEphem, hence updating from 3.7.6 to 3.7.7 is harmless. Star names are chosen to comply with Nautical Almanacs.  
NOTE: if required, a Python 2.7 script with identical functionality can be found at: https://github.com/aendie/Pyalmanac-Py2  

**ACKNOWLEDGEMENTS**

I, Andrew Bauer, wish to thank Enno Rodegerdts for permission to update his GitHub site. Without Enno's pioneering work on the original Pyalmanac I would never have started (or known how to start) on this journey. I also thank the experts who have helped me... especially Brandon Rhodes, author of PyEphem and Skyfield, for fixing minor issues I identified.  

**AVAILABLE VERSIONS**

Two versions (other than Pyalmanac) are available here: https://github.com/aendie

* **Pyalmanac** is the fastest with "somewhat limited" accuracy that is sufficient for nautical navigation.  
* **SFalmanac** is the slowest and most accurate; almost entirely based on *Skyfield*. *PyEphem* is only used for planet magnitudes (because these are not in *Skyfield*).  
* **Skyalmanac** is a hybrid version that is significantly faster than SFalmanac. *PyEphem* is used for planet magnitudes and for all planet transits, sunrise and sunset calculations as well as moonrise and moonset.  

PyEphem  website: https://rhodesmill.org/pyephem/  
Skyfield website: https://rhodesmill.org/skyfield/

## Requirements

&nbsp;&nbsp;&nbsp;&nbsp;Most of the computation is done by the free Pyephem library.  
&nbsp;&nbsp;&nbsp;&nbsp;Typesetting is done by TeX/LaTeX so you first need to install:

* Python v3.4 or higher (the latest version is recommended)
* PyEphem
* TeX/LaTeX&nbsp;&nbsp;or&nbsp;&nbsp;MiKTeX


### INSTALLATION GUIDELINES on Windows 10:

&nbsp;&nbsp;&nbsp;&nbsp;Install Python 3.8 (add python.exe to path)  
&nbsp;&nbsp;&nbsp;&nbsp;Install MiKTeX 2.9 from https://miktex.org/  
&nbsp;&nbsp;&nbsp;&nbsp;Run Command Prompt as Administrator, go to your Python folder and execute, e.g.:

&nbsp;&nbsp;&nbsp;&nbsp;**cd C:\\Python38-32**  
&nbsp;&nbsp;&nbsp;&nbsp;**pip install --upgrade pip**  
&nbsp;&nbsp;&nbsp;&nbsp;... for a first install:  
&nbsp;&nbsp;&nbsp;&nbsp;**pip install pyephem**  
&nbsp;&nbsp;&nbsp;&nbsp;... if already installed, check for upgrade explicitly:  
&nbsp;&nbsp;&nbsp;&nbsp;**pip install --upgrade pyephem**  

&nbsp;&nbsp;&nbsp;&nbsp;Put the Pyalmanac files in a new folder, run Command Prompt and start with:  
&nbsp;&nbsp;&nbsp;&nbsp;**py -3 pyalmanac.py**


### INSTALLATION GUIDELINES on Linux:

&nbsp;&nbsp;&nbsp;&nbsp;Install your platform's Python- and LaTeX distribution.  
&nbsp;&nbsp;&nbsp;&nbsp;Remember to choose python 3.4 or higher and install all develpment header files.  
&nbsp;&nbsp;&nbsp;&nbsp;Run at the command line:

&nbsp;&nbsp;&nbsp;&nbsp;**pip install pyephem**

&nbsp;&nbsp;&nbsp;&nbsp;Put the Pyalmanac files in any directory and start with:  
&nbsp;&nbsp;&nbsp;&nbsp;**python pyalmanac**  
&nbsp;&nbsp;&nbsp;&nbsp;or  
&nbsp;&nbsp;&nbsp;&nbsp;**./pyalmanac**


### INSTALLATION GUIDELINES on MAC:

&nbsp;&nbsp;&nbsp;&nbsp;Every Mac comes with python preinstalled.  
&nbsp;&nbsp;&nbsp;&nbsp;(Please choose this version of Pyalmanac if Python 3.* is installed.)  
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