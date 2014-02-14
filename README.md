Pyalmanac 
=========

Pyalmanac is a Python script that creats the daily pages of the
Nautical Almanac. These are tabels that are needed for selestial
navigation with a Sekstant. Normally these tables must be bought every
year as a Book. This little program is trying to do away with this
inconveniance. Most of the heavy computing is done by the free Pyephem
libraries. Typesetting is done by TeX/LaTeX So before you can use this
program you net to install:

Python v2.x (2.6 or later ) python 3 will not work out of the box

PyEphem

TeX/LaTeX

INSTALLATION Linux:
Install your platforms Python- and LaTeX distribution. Remember to chose python 2.x and install all develpment header files.
Run at the command line:

pip install pyephem

Put the Pyalmanac files in any directory and start with:

python pyalmanac
or 
./pyalmanac 



INSTALLATION MAC:

Every Mac comes with python preinstalled. You need to install the PyEphem library to use Pyalmanac. Type the following commands at the commandline (terminal app):

sudo easy_install pip

pip install pyephem

If this command fails your mac asks you if you would like to install the header files. Do so, you do not need to install the full IDE.
Try again.

Install TeX/LaTeX from http://www.tug.org/mactex/

Now you are almost ready
Put the Pyalmanac files in any directory and start with 
python pyalmanac
or 
./pyalmanac 


