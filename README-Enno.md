# Pyalmanac (Python 3 version)

**Description**

Pyalmanac is a Python 3 script that creates the daily pages of the Nautical Almanac using the UTC timescale,
which is the basis for the worldwide system of civil time. Official Nautical Almanacs employ a UT timescale (equivalent to UT1).

The 'daily pages' are tables that are needed for celestial navigation with a sextant.
Although you are strongly advised to purchase the official Nautical Almanac, this program will reproduce the tables with no warranty or guarantee of accuracy.

Pyalmanac was developed based on the original *Pyalmanac* by Enno Rodegerdts. Various improvements, enhancements and bugfixes have been added since.

**Current state of Pyalmanac**

Pyalmanac is a somewhat dated program.
Pyalmanac is implemented using the [Ephem](https://rhodesmill.org/pyephem/) astronomical library (originally named PyEphem), which has *Mature* development status.
Ephem was based upon XEphem, which is 'end of life' as no further updates to XEphem are planned.
Elwood Charles Downey, the author of XEphem, generously gave permission for their use in (Py)Ephem.  
**Please note the Software Requirements below for Ephem as the latest versions still contain a software error!**

Pyalmanac contains its own star database, now updated with data from the Hipparcos Star Catalogue. 
Star names are chosen to comply with official Nautical Almanacs.
The GHA/Dec star data now matches a sample page from a Nautical Almanac typically to within 0°0.1'.
As of now, (Py)Ephem will continue to receive critical bugfixes and be ported to each new version of Python.
Pyalmanac still has the advantage of speed over other implementations.

One minor limitation of Ephem is in the EOP (Earth Orientation Parameters) (affecting *sidereal time*) which is more accurate in Skyfield-based almanacs as they can employ the IERS (International Earth Rotation Service) EOP published data. This affects *sidereal time*, which minimizes GHA discrepancies in general. (This applies to all celestial objects.)

Slight differences can also be detected in the *Event Times*: sunrise, sunset, moonrise, moonset, civil twilight start/end and nautical twilight start/end, particularly in more Northern latitudes. 

Given the choice, [SFalmanac](https://pypi.org/project/sfalmanac/) is an up-to-date program with almost identical functionality to Pyalmanac, and it uses [Skyfield](https://rhodesmill.org/skyfield/), a modern astronomical library based on the highly accurate algorithms employed in the [NASA JPL HORIZONS System](https://ssd.jpl.nasa.gov/horizons/).
(Pyalmanac and SFalmanac have same formatted pages so differences can easily be spotted by swiching between them in Adobe Acrobat reader.)

**ACKNOWLEDGEMENTS**

I, Andrew Bauer, wish to thank Enno Rodegerdts for permission to update his GitHub site. Without Enno's pioneering work on the original Python 2 version of Pyalmanac I would never have started (or known how to start) on this journey. I also thank the experts who have helped me... especially Brandon Rhodes, author of Ephem/PyEphem and Skyfield, for his assistance.  

**AVAILABLE VERSIONS**

**NOTE: the Python Package Index (PyPI) edition is here:** https://pypi.org/project/pyalmanac/  
**Users are encouraged to install the PyPI edition instead.**  

Two versions (other than Pyalmanac) are available here: https://github.com/aendie

* **Pyalmanac** is the fastest with marginally poorer accuracy.  
* **SFalmanac** is slightly slower and most accurate; based on *Skyfield*. *Ephem* is only used for a few planet magnitudes (because these are not yet in *Skyfield*).  
* **Skyalmanac** is a hybrid version that is no longer recommended now that SFalmanac supports multiprocessing.  

Ephem website: https://rhodesmill.org/pyephem/  
Skyfield website: https://rhodesmill.org/skyfield/

**UPDATE: Mar 2020**

A new parameter in *config.py* enables one to choose between A4 and Letter-sized pages. A [new approach](https://docs.python.org/3/whatsnew/3.0.html#pep-3101-a-new-approach-to-string-formatting) to string formatting has been implemented:
the [old](https://docs.python.org/2/library/stdtypes.html#string-formatting) style Python string formatting syntax has been replaced by the [new](https://docs.python.org/3/library/string.html#format-string-syntax) style string formatting syntax. 

**UPDATE: Jun 2020**

The Equation Of Time is shaded whenever EoT is negative indicating that apparent solar time is slow compared to mean solar time (mean solar time > apparent solar time).

**UPDATE: Feb 2021**

Minor changes are included here to this original (non-PyPI) edition to reflect some of the adaptation that was required (e.g. integrate *increments.py* into *pyalmanac.py* as Option 5) to create a PyPI (Python Package Index) edition making this original (non-PyPI) and the PyPI editions similar. Both editions create identical almanacs and the [PyPI edition](https://pypi.org/project/pyalmanac/) is the preferred choice for users.

**UPDATE: Apr 2021**

A double moonrise or moonset on the same day is now highlighted for better legibility. Event Time tables can now be generated - these are the tables containing data in hours:minutes:seconds, e.g. sunrise, sunset, moonrise, moonset and Meridian Passage.
Accuracy to to the second of time is not required for navigational purposes, but may be used to compare accuracy with other algorithms. Some internal technical enhancements and minor changes to text are also included.

**UPDATE: May 2021**

The indication of objects (Sun or Moon) continuously above or below the horizon has been corrected.

Regarding Moon Data: ".. .." has been added to indicate that the moonrise/moonset event occurs the following day (at the specified latitude). If there is no moonrise/moonset for two or more consecutive days, black boxes indicate "moon below horizon"; white boxes indicate "moon above horizon". This brings it in line with Nautical Almanacs. (Previously they were only displayed when there was no moonrise *and* no moonset on a single day.)

Correction to Sun Data: "Sun continually above/below horizon" now shown if it applies to both Sunrise and Sunset, or *additionally* to both Civil Twilight Start & End; or *additionally* to both Astronomical Twilight Start & End, i.e. as two, four or six events per day and latitude. This brings it in line with Nautical Almanacs.

&emsp;:smiley:&ensp;Pyalmanac is now available on DockerHub [here](https://hub.docker.com/repository/docker/aendie/pyalmanac).&ensp;:smiley:

The DockerHub image contains a Linux-based OS, TeX Live, the application code, and third party Python imports (including the astronomical library). It can be executed "in a container" on Windows 10 Pro, macOS or a Linux-based OS.

**UPDATE: Jul 2021**

The PDF filenames have been revised:

* modna_\<starting date or year\>.pdf: for Nautical Almanacs in modern style
* modst_\<starting date or year\>.pdf: for Sun Tables in modern style
* tradna_\<starting date or year\>.pdf: for Nautical Almanacs in traditional style
* tradst_\<starting date or year\>.pdf: for Sun Tables in traditional style

One command line argument may be appended to the run command:

* -v to invoke verbose mode (send pdfTeX execution steps to the console)
* -log to preserve the log file
* -tex to preserve the tex file

**UPDATE: Nov 2021**

* Enhanced User Interface includes the possibility to generate tables starting at any valid date, or for any month (within -12/+11 months from today).
* Minor cosmetic improvements ('d'-correction in italics; greek 'nu' replaces 'v'-correction; Minutes-symbol added to SD and d)

Increased accuracy due to the following minor improvements:
* Moon phase (percent illumination) is based on midnight (as opposed to midday)
* Star positions are based on midnight (as opposed to midday)
* Moon v and d for hour ‘n’ are based on “hour ‘n+1’ minus hour ‘n’” as opposed to “hour ‘n’ + 30 minutes minus hour ‘n’ – 30 minutes”

The PDF filenames have been revised (again):

* NAmod_\<starting date or month or year\>.pdf: for Nautical Almanacs in modern style
* STmod_\<starting date or month or year\>.pdf: for Sun Tables in modern style
* NAtrad_\<starting date or month or year\>.pdf: for Nautical Almanacs in traditional style
* STtrad_\<starting date or month or year\>.pdf: for Sun Tables in traditional style

**UPDATE: Sep 2022**

* The PDF filenames have been harmonized with those in SFalmanac.
* Better support for Letter-sized pages.
* The LaTeX *fancyhdr* package is employed when MiKTeX (or a TeX Live version >= 2020) is detected.
* Command line options:
    * -v   ... 'verbose': to send pdfTeX output to the terminal
    * -log ... to keep the log file
    * -tex ... to keep the tex file
    * -old ... old formatting without the fancyhdr package
    * -a4  ... A4 papersize
    * -let ... Letter papersize
    * -dpo ... data pages only

## Requirements

&emsp;Astronomical computation is done by the free Ephem library.  
&emsp;Typesetting is typically done by MiKTeX or TeX Live.  
&emsp;Here are the requirements/recommendations:

* Python v3.4 or higher (the latest version is recommended)
* Ephem >= 3.7.6 (4.1 is good; 4.1.1, 4.1.2 or 4.1.3 are faulty)
* MiKTeX&ensp;or&ensp;TeX Live

## Files required in the execution folder:

* &ast;.py
* Ra.jpg
* A4chartNorth_P.pdf

### INSTALLATION GUIDELINES on Windows 10:

&emsp;Install Python 3.10.6 It should be in the system environment variable PATH, e.g.  
&emsp;&ensp;**C:\\Python310\Scripts;C:\\Python310;** .....  
&emsp;Install MiKTeX 22.7 from https://miktex.org/  
&emsp;When MiKTeX first runs it will require installation of additional packages.  
&emsp;Run Command Prompt as Administrator, go to your Python folder and execute, e.g.:

&emsp;**cd C:\\Python310**  
&emsp;**python.exe -m pip install --upgrade pip**  
&emsp;... for a first install:  
&emsp;**pip3 uninstall pyephem ephem**  
&emsp;**pip3 install ephem==4.1**  

&emsp;Put the Pyalmanac files in a new folder, run Command Prompt and start with:  
&emsp;**py -3 pyalmanac.py**

&emsp;If using MiKTeX 21 or higher, executing 'option 7' (Increments and Corrections) will probably fail with  
&emsp;**! TeX capacity exceeded, sorry [main memory size=3000000].**  
&emsp;To resolve this problem (assuming MiKTeX has been installed for all users),  
&emsp;open a Command Prompt as Administrator and enter:  
&emsp;**initexmf --admin --edit-config-file=pdflatex**  
&emsp;This opens **pdflatex.ini** in Notepad. Add the following line:  
&emsp;**extra_mem_top = 1000000**  
&emsp;and save the file. Problem solved. For more details go [here](https://tex.stackexchange.com/questions/438902/how-to-increase-memory-size-for-xelatex-in-miktex/438911#438911)

### INSTALLATION GUIDELINES on Ubuntu 19.10 or 20.04:

&emsp;Ubuntu 19 and higher come with Python 3 preinstalled,  
&emsp;however pip may need to be installed:  
&emsp;**sudo apt install python3-pip**

&emsp;Install the following TeX Live package:  
&emsp;**sudo apt install texlive-latex-extra**

&emsp;Install the required astronomical library:  
&emsp;**pip3 uninstall pyephem ephem**  
&emsp;**pip3 install ephem==4.1**

&emsp;Put the Pyalmanac files in a folder and start with:  
&emsp;**python3 pyalmanac.py**  


### INSTALLATION GUIDELINES on MAC:

&emsp;Every Mac comes with python preinstalled.  
&emsp;(Please choose this version of Pyalmanac if Python 3.* is installed.)  
&emsp;You need to install the Ephem library to use Pyalmanac.  
&emsp;Type the following commands at the commandline (terminal app):

&emsp;**sudo easy_install pip**  
&emsp;**pip uninstall pyephem ephem**  
&emsp;**pip install ephem==4.1**  

&emsp;If this command fails, your Mac asks you if you would like to install the header files.  
&emsp;Do so - you do not need to install the full IDE - and try again.

&emsp;Install TeX/LaTeX from http://www.tug.org/mactex/

&emsp;Now you are almost ready. Put the Pyalmanac files in any directory and start with:  
&emsp;**python pyalmanac**  
&emsp;or  
&emsp;**./pyalmanac**