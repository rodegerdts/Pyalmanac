# Pyalmanac (Python 3 version)

**'End of Life' ANNOUNCEMENT**

Pyalmanac is nearing the end of its useful days. Almanacs generated after the next few
years should not be used for navigational purposes. SFalmanac (or Skyalmanac with
some restrictions regarding the accuracy of sunset/twilight/sunrise and moonrise/moonset)
are the new norm as these are based on the more accurate algorithms currently employed
in the NASA JPL HORIZONS System (the same algorithms are implemented in Skyfield).

Pyalmanac is implemented using Ephem (originally named PyEphem), which in turn uses XEphem that is based on the
VSOP87D algorithms. XEphem is also 'end of life' as no further updates are planned,
however the major discrepancies are related to the projected speed of Earth's rotation.
The discrepancies in GHA between Ephem and Skyfield 1.31 can be summarized thus:

* in 2020:&nbsp;&nbsp; 00.0 to 00.1 arcMINUTES GHA too high
* in 2030:&nbsp;&nbsp; 04.0 to 04.8 arcMINUTES GHA too high
* in 2050:&nbsp;&nbsp; 13.9 to 14.9 arcMINUTES GHA too high
* in 2100:&nbsp;&nbsp; 38.0 to 40.2 arcMINUTES GHA too high
* in 2200:&nbsp;&nbsp; 90.1 to 94.1 arcMINUTES GHA too high

The GHA discrepancy applies to the sun, moon, the First Point of Aries and to all planets.

**Description**

Pyalmanac is a **Python 3** script that creates the daily pages of the Nautical Almanac. These are tables that are needed for celestial navigation with a sextant. Although you are strongly advised to purchase the official Nautical Almanac, this program will reproduce the tables with no warranty or guarantee of accuracy.

This version of Pyalmanac was developed by Andrew Bauer based on the original Pyalmanac by Enno Rodegerdts. Various improvements, enhancements and bugfixes have been included. 
Pyalmanac contains its own star database (similar to the database in Ephem 3.7.6), however the accuracy was poor. It is updated with data from the Hipparcos Star Catalogue and the GHA/Dec star data now matches a sample page from a Nautical Almanac typically to within 0°0.1'.

NOTE: two scripts are included (both can be run): 'pyalmanac.py' and 'increments.py'  
NOTE: Pyalmanac contains its own star database - it does not use the version supplied with Ephem, hence updating from 3.7.6 to 3.7.7.1 is harmless. Star names are chosen to comply with Nautical Almanacs.  
NOTE: if still required, a Python 2.7 script with identical functionality can be found at: https://github.com/aendie/Pyalmanac-Py2  

**ACKNOWLEDGEMENTS**

I, Andrew Bauer, wish to thank Enno Rodegerdts for permission to update his GitHub site. Without Enno's pioneering work on the original Pyalmanac I would never have started (or known how to start) on this journey. I also thank the experts who have helped me... especially Brandon Rhodes, author of Ephem/PyEphem and Skyfield, for fixing minor issues I identified.  

**AVAILABLE VERSIONS**

Two versions (other than Pyalmanac) are available here: https://github.com/aendie

* **Pyalmanac** is the fastest with "somewhat limited" accuracy that is sufficient for nautical navigation up to 2020 or so.  
* **SFalmanac** is the slowest and most accurate; almost entirely based on *Skyfield*. *Ephem* is only used for planet magnitudes (because these are not yet in *Skyfield*).  
* **Skyalmanac** is a hybrid version that is significantly faster than SFalmanac. *Ephem* is used for planet magnitudes and for all planet transits, sunrise, twilight and sunset calculations as well as for moonrise and moonset.  

Ephem/PyEphem  website: https://rhodesmill.org/pyephem/  
Skyfield website: https://rhodesmill.org/skyfield/

**UPDATE: Mar 2020**

A new parameter in *config.py* enables one to choose between A4 and Letter-sized pages. A [new approach](https://docs.python.org/3/whatsnew/3.0.html#pep-3101-a-new-approach-to-string-formatting) to string formatting has been implemented:
the [old](https://docs.python.org/2/library/stdtypes.html#string-formatting) style Python string formatting syntax has been replaced by the [new](https://docs.python.org/3/library/string.html#format-string-syntax) style string formatting syntax. 

**UPDATE: Jun 2020**

The Equation Of Time is shaded whenever EoT is negative indicating that apparent solar time is slow compared to mean solar time (mean solar time > apparent solar time).

## Requirements

&nbsp;&nbsp;&nbsp;&nbsp;Most of the computation is done by the free Ephem library.  
&nbsp;&nbsp;&nbsp;&nbsp;Typesetting is done by MiKTeX or TeX Live so you first need to install:

* Python v3.4 or higher (the latest version is recommended)
* Ephem
* TeX/LaTeX&nbsp;&nbsp;or&nbsp;&nbsp;MiKTeX&nbsp;&nbsp;or&nbsp;&nbsp;TeX Live

## Files required in the execution folder:

* &ast;.py
* Ra.jpg
* A4chartNorth_P.pdf

### INSTALLATION GUIDELINES on Windows 10:

&nbsp;&nbsp;&nbsp;&nbsp;Install Python 3.9.1 (should be in the system environment variable PATH, e.g. )  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**C:\\Python39\Scripts;C:\\Python39;** .....  
&nbsp;&nbsp;&nbsp;&nbsp;Install MiKTeX 21.1 from https://miktex.org/  
&nbsp;&nbsp;&nbsp;&nbsp;When MiKTeX first runs it will require installation of additional packages.  
&nbsp;&nbsp;&nbsp;&nbsp;Run Command Prompt as Administrator, go to your Python folder and execute, e.g.:

&nbsp;&nbsp;&nbsp;&nbsp;**cd C:\\Python39**  
&nbsp;&nbsp;&nbsp;&nbsp;**python.exe -m pip install --upgrade pip**  
&nbsp;&nbsp;&nbsp;&nbsp;... for a first install:  
&nbsp;&nbsp;&nbsp;&nbsp;**pip3 uninstall pyephem**  
&nbsp;&nbsp;&nbsp;&nbsp;**pip3 install ephem**  
&nbsp;&nbsp;&nbsp;&nbsp;... if already installed, check for upgrade explicitly:  
&nbsp;&nbsp;&nbsp;&nbsp;**pip3 install --upgrade ephem**  

&nbsp;&nbsp;&nbsp;&nbsp;Put the Pyalmanac files in a new folder, run Command Prompt and start with:  
&nbsp;&nbsp;&nbsp;&nbsp;**py -3 pyalmanac.py**

&nbsp;&nbsp;&nbsp;&nbsp;If using MiKTeX 21 or higher, running **py -3 increments.py** will probably fail with  
&nbsp;&nbsp;&nbsp;&nbsp;**! TeX capacity exceeded, sorry [main memory size=3000000].**  
&nbsp;&nbsp;&nbsp;&nbsp;To resolve this problem (assuming MiKTeX has been installed for all users),  
&nbsp;&nbsp;&nbsp;&nbsp;open a Command Prompt as Administrator and enter:  
&nbsp;&nbsp;&nbsp;&nbsp;**initexmf --admin --edit-config-file=pdflatex**  
&nbsp;&nbsp;&nbsp;&nbsp;This opens **pdflatex.ini** in Notepad. Add the following line:  
&nbsp;&nbsp;&nbsp;&nbsp;**extra_mem_top = 1000000**  
&nbsp;&nbsp;&nbsp;&nbsp;and save the file. Problem solved. For more details go [here](https://tex.stackexchange.com/questions/438902/how-to-increase-memory-size-for-xelatex-in-miktex/438911#438911)

### INSTALLATION GUIDELINES on Ubuntu 19.10 or 20.04:

&nbsp;&nbsp;&nbsp;&nbsp;Ubuntu 19 and higher come with Python 3 preinstalled,  
&nbsp;&nbsp;&nbsp;&nbsp;however pip may need to be installed:  
&nbsp;&nbsp;&nbsp;&nbsp;**sudo apt install python3-pip**

&nbsp;&nbsp;&nbsp;&nbsp;Install the following TeX Live package:  
&nbsp;&nbsp;&nbsp;&nbsp;**sudo apt install texlive-latex-extra**

&nbsp;&nbsp;&nbsp;&nbsp;Install the required astronomical library:  
&nbsp;&nbsp;&nbsp;&nbsp;**pip3 uninstall pyephem**  
&nbsp;&nbsp;&nbsp;&nbsp;**pip3 install ephem**

&nbsp;&nbsp;&nbsp;&nbsp;Put the Pyalmanac files in a folder and start with:  
&nbsp;&nbsp;&nbsp;&nbsp;**python3 pyalmanac.py**  


### INSTALLATION GUIDELINES on MAC:

&nbsp;&nbsp;&nbsp;&nbsp;Every Mac comes with python preinstalled.  
&nbsp;&nbsp;&nbsp;&nbsp;(Please choose this version of Pyalmanac if Python 3.* is installed.)  
&nbsp;&nbsp;&nbsp;&nbsp;You need to install the PyEphem library to use Pyalmanac.  
&nbsp;&nbsp;&nbsp;&nbsp;Type the following commands at the commandline (terminal app):

&nbsp;&nbsp;&nbsp;&nbsp;**sudo easy_install pip**  
&nbsp;&nbsp;&nbsp;&nbsp;**pip uninstall pyephem**  
&nbsp;&nbsp;&nbsp;&nbsp;**pip install ephem**  

&nbsp;&nbsp;&nbsp;&nbsp;If this command fails, your Mac asks you if you would like to install the header files.  
&nbsp;&nbsp;&nbsp;&nbsp;Do so - you do not need to install the full IDE - and try again.

&nbsp;&nbsp;&nbsp;&nbsp;Install TeX/LaTeX from http://www.tug.org/mactex/

&nbsp;&nbsp;&nbsp;&nbsp;Now you are almost ready. Put the Pyalmanac files in any directory and start with:  
&nbsp;&nbsp;&nbsp;&nbsp;**python pyalmanac**  
&nbsp;&nbsp;&nbsp;&nbsp;or  
&nbsp;&nbsp;&nbsp;&nbsp;**./pyalmanac**