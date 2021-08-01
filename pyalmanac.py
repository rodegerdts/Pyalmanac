#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#   Copyright (C) 2014  Enno Rodegerdts
#   Copyright (C) 2021  Andrew Bauer

#  This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.
# 
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License along
#     with this program; if not, write to the Free Software Foundation, Inc.,
#     51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# Standard library imports
import os
import sys
import time
import datetime

# Local application imports
import tables
import suntables
import eventtables
import config
import increments


def makePDF(args, fn, msg = ""):
    command = 'pdflatex {}'.format(args + fn + ".tex")
    if args == "":
        os.system(command)
        print("finished" + msg)
    else:
        returned_value = os.system(command)
        if returned_value != 0:
            if msg != "":
                print("ERROR detected while" + msg)
            else:
                print("!!   ERROR detected while creating PDF file   !!")
                print("!! Append '-v' or '-log' for more information !!")
        else:
            if msg != "":
                print("finished" + msg)
            else:
                print("finished creating PDF")
    return

def tidy_up(fn):
    if not keeptex: os.remove(fn + ".tex")
    if not keeplog:
        if os.path.isfile(fn + ".log"):
            os.remove(fn + ".log")
    if os.path.isfile(fn + ".aux"):
        os.remove(fn + ".aux")
    return


##Main##
if sys.version_info[0] < 3:
    raise Exception("This runs with Python 3")

try:
    arg = sys.argv[1]
except IndexError:
    arg = ""
if len(sys.argv) > 2 or not (arg == "" or arg == "-v" or arg == "-log" or arg == "-tex"):
    print("One optional command line parameter is permitted:")
    print(" python pyalmanac.py -v")
    print(" ... to send pdfTeX output to the terminal")
    print(" python pyalmanac.py -log")
    print(" ... to keep the log file")
    print(" python pyalmanac.py -tex")
    print(" ... to keep the tex file")
    sys.exit(0)

args = "" if arg == "-v" else "-interaction=batchmode -halt-on-error "
keeplog = True if arg == "-log" else False
keeptex = True if arg == "-tex" else False

d = datetime.datetime.utcnow().date()
first_day = datetime.date(d.year, d.month, d.day)

# if this code runs locally (not in Docker), the settings in config.py are used.
# if this code runs in Docker without use of an environment file, the settings in config.py apply.
# if this code runs in Docker with an environment file ("--env-file ./.env"), then its values apply.
if config.dockerized:
    docker_main = os.getcwd()
    config.pgsz = os.getenv('PGSZ', config.pgsz)
    config.search_next_rising_sun = os.getenv('SNRS', str(config.search_next_rising_sun))
    stdt = os.getenv('SDATE', 'None')
    if stdt != 'None':      # for testing a specific date
        try:
            first_day = datetime.date(int(stdt[0:4]), int(stdt[5:7]), int(stdt[8:10]))
        except:
            print("Invalid date format for SDATE in .env: {}".format(stdt))
            sys.exit(0)
        d = first_day
    err1 = " the Docker .env file"
    err2 = "for SNRS in the Docker .env file"
else:
    #first_day = datetime.date(2023, 6, 24)	# for testing a specific date
    #d = first_day							# for testing a specific date
    config.search_next_rising_sun = str(config.search_next_rising_sun)
    err1 = "config.py"
    err2 = "for search_next_rising_sun in config.py"

sday = "{:02d}".format(d.day)       # sday = "%02d" % d.day
smth = "{:02d}".format(d.month)     # smth = "%02d" % d.month
syr  = "{}".format(d.year)          # syr  = "%s" % d.year
symd = syr + smth + sday
sdmy = sday + "." + smth + "." + syr
#print('Today is {}'.format(symd))

if config.pgsz not in set(['A4', 'Letter']):
    print("Please choose a valid paper size in {}".format(err1))
    sys.exit(0)

if config.search_next_rising_sun.lower() not in set(['true', 'false']):
    print("Please choose a boolean value {}".format(err2))
    sys.exit(0)

config.search_next_rising_sun = (config.search_next_rising_sun.lower() == 'true')   # to boolean
f_prefix = config.docker_prefix
f_postfix = config.docker_postfix

s = input("""\nWhat do you want to create?:\n
    1   Nautical Almanac   (for a year)
    2   Sun tables only    (for a year)
    3   Event Time tables  (for a year)
    4   Nautical almanac   -  6 days from today
    5   Sun tables only    - 30 days from today
    6   Event Time tables  -  6 days from today
    7   "Increments and Corrections" tables (static data)
""")

if s in set(['1', '2', '3', '4', '5', '6', '7']):
    if int(s) < 4:
        print("Please enter the desired year")
        years = input("  as yyyy ... or the FIRST and LAST year as yyyy-yyyy\n")
        if len(years)== 4:
            yearfr = years
            yearto = years
        elif len(years) == 9 and years[4] == '-':
            yearfr = years[0:4]
            yearto = years[5:9]
        else:
            print("Error! Invalid format")
            sys.exit(0)
        
        if str(yearfr).isnumeric():
            if 1000 <= int(yearfr) <= 3000:
                first_day = datetime.date(int(yearfr), 1, 1)
            else:
                print("Error! Please pick a year between 1000 and 3000")
                sys.exit(0)
        else:
            print("Error! First year is not numeric")
            sys.exit(0)

        if str(yearto).isnumeric():
            if 1000 <= int(yearto) <= 3000:
                first_day_to = datetime.date(int(yearto), 1, 1)
            else:
                print("Error! Please pick a year between 1000 and 3000")
                sys.exit(0)
            if int(yearto) < int(yearfr):
                print("Error! The LAST year must be later than the FIRST year")
                sys.exit(0)
        else:
            print("Error! Last year is not numeric")
            sys.exit(0)

    if s != '3' and int(s) <= 5:
        tsin = input("""What table style is required?:\n
        t   Traditional
        m   Modern
""")
        ff = '_'
        DecFmt = ''
        config.tbls = tsin[0:1]	# table style
        config.decf = tsin[1:2]	# Declination format
        if config.tbls != 'm':
            config.tbls = ''		# anything other than 'm' is traditional
            ff = ''
        if config.decf != '+':		# Positive/Negative Declinations
            config.decf = ''		# USNO format for Declination
        else:
            DecFmt = '[old]'

    if s == '1':        # Nautical Almanac (for a year)
        print("Please wait - this can take a while.")
        for yearint in range(int(yearfr),int(yearto)+1):
            start = time.time()
            year = "{:4d}".format(yearint)  # year = "%4d" %yearint
            msg = "\nCreating the nautical almanac for the year {}\n".format(year)
            print(msg)
            first_day = datetime.date(yearint, 1, 1)
            ff = "tradna_" if config.tbls != 'm' else "modna_"
            fn = "{}{}".format(ff,year+DecFmt)
            outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
            outfile.write(tables.almanac(first_day,122))
            outfile.close()
            stop = time.time()
            msg = "execution time = {:0.2f} seconds".format(stop-start) # msg = "execution time = %0.2f seconds" %(stop-start)
            print(msg)
            print()
            if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
            makePDF(args, fn, " creating nautical almanac for {}".format(year))
            tidy_up(fn)
            if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

    elif s == '2':      # Sun Tables (for a year)
        for yearint in range(int(yearfr),int(yearto)+1):
            year = "{:4d}".format(yearint)  # year = "%4d" %yearint
            msg = "\nCreating the sun tables for the year {}\n".format(year)
            print(msg)
            first_day = datetime.date(yearint, 1, 1)
            ff = "tradst_" if config.tbls != 'm' else "modst_"
            fn = "{}{}".format(ff,year+DecFmt)
            outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
            outfile.write(suntables.almanac(first_day,25))
            outfile.close()
            if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
            makePDF(args, fn, " creating sun tables for {}".format(year))
            tidy_up(fn)
            if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

    elif s == '3':      # Event Time tables  (for a year)
        print("Please wait - this can take a while.")
        for yearint in range(int(yearfr),int(yearto)+1):
            start = time.time()
            year = "{:4d}".format(yearint)  # year = "%4d" %yearint
            msg = "\nCreating the event time tables for the year {}\n".format(year)
            print(msg)
            first_day = datetime.date(yearint, 1, 1)
            fn = "event-times_{}".format(year)
            outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
            outfile.write(eventtables.maketables(first_day,183))
            outfile.close()
            stop = time.time()
            msg = "execution time = {:0.2f} seconds".format(stop-start) # msg = "execution time = %0.2f seconds" %(stop-start)
            print(msg)
            print()
            if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
            makePDF(args, fn, " creating event time tables for {}".format(year))
            tidy_up(fn)
            if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

    elif s == '4':      # Nautical almanac   -  6 days from today
##        config.initLOG()		# initialize log file
        msg = "\nCreating nautical almanac tables - from {}\n".format(sdmy)
        print(msg)
        ff = "tradna_" if config.tbls != 'm' else "modna_"
        fn = "{}{}".format(ff,symd+DecFmt)
        outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
        outfile.write(tables.almanac(first_day,2))
        outfile.close()
##        msg = 'Count of incorrect values: {}'.format(config.errors)
##        config.writeLOG('\n' + msg + '\n')
##        config.closeLOG()
        if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
        makePDF(args, fn)
        tidy_up(fn)

    elif s == '5':      # Sun tables only    - 30 days from today
        msg = "\nCreating the sun tables - from {}\n".format(sdmy)
        print(msg)
        ff = "tradst_" if config.tbls != 'm' else "modst_"
        fn = "{}{}".format(ff,symd+DecFmt)
        outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
        outfile.write(suntables.almanac(first_day,2))
        outfile.close()
        if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
        makePDF(args, fn)
        tidy_up(fn)

    elif s == '6':      # Event Time tables  -  6 days from today
        msg = "\nCreating event time tables - from {}\n".format(sdmy)
        print(msg)
        fn = "event-times_{}".format(symd)
        outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
        outfile.write(eventtables.maketables(first_day,3))
        outfile.close()
        if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
        makePDF(args, fn)
        tidy_up(fn)

    elif s == '7':
        msg = "\nCreating the Increments and Corrections tables\n"
        print(msg)
        fn = "inc"
        outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
        outfile.write(increments.makelatex())
        outfile.close()
        if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
        makePDF(args, fn)
        tidy_up(fn)

else:
    print("Error! Choose 1, 2, 3, 4, 5, 6 or 7")
