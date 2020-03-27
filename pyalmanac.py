#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#   Copyright (C) 2014  Enno Rodegerdts
#   Copyright (C) 2019  Andrew Bauer

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

import tables
import suntables 
import os
import sys
import time
import datetime
import config

##Main##
if sys.version_info[0] < 3:
    raise Exception("This runs with Python 3")

d = datetime.datetime.utcnow().date()
first_day = datetime.date(d.year, d.month, d.day)

#first_day = datetime.date(2023, 6, 24)	# for testing a specific date
#d = first_day							# for testing a specific date

sday = "{:02d}".format(d.day)       # sday = "%02d" % d.day
smth = "{:02d}".format(d.month)     # smth = "%02d" % d.month
syr  = "{}".format(d.year)          # syr  = "%s" % d.year
symd = syr + smth + sday
sdmy = sday + "." + smth + "." + syr
#print('Today is {}'.format(symd))

if config.pgsz not in set(['A4', 'Letter']):
    print("Please choose a valid paper size in config.py")
    sys.exit(0)

s = input("""What do you want to create?:\n
    1   Full nautical almanac   (for a year)
    2   Just tables for the sun (for a year)
    3   Nautical almanac   - 6 days from today
    4   Tables for the sun - 30 days from today
""")

if s in set(['1', '2', '3', '4']):
    if int(s) < 3:
        print("Please enter the year you want to create the nautical almanac")
        years = input("  for as yyyy ... or the FIRST and LAST year as yyyy-yyyy\n")
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

    if s == '1':
        print("Please wait - this can take a while.")
        for yearint in range(int(yearfr),int(yearto)+1):
            start = time.time()
            year = "{:4d}".format(yearint)  # year = "%4d" %yearint
            msg = "\nCreating the nautical almanac for the year {}".format(year)
            print(msg)
            first_day = datetime.date(yearint, 1, 1)
            filename = "almanac{}{}.tex".format(ff,year+DecFmt)
            outfile = open(filename, mode="w", encoding="utf8")
            outfile.write(tables.almanac(first_day,122))
            outfile.close()
            stop = time.time()
            msg = "execution time = {:0.2f} seconds".format(stop-start) # msg = "execution time = %0.2f seconds" %(stop-start)
            print(msg)
            print()
            command = 'pdflatex {}'.format(filename)
            os.system(command)
            print("finished creating nautical almanac for {}".format(year))
            os.remove(filename)
            if os.path.isfile("almanac{}{}.log".format(ff,symd+DecFmt)):
                os.remove("almanac{}{}.log".format(ff,year+DecFmt))
            if os.path.isfile("almanac{}{}.aux".format(ff,symd+DecFmt)):
                os.remove("almanac{}{}.aux".format(ff,year+DecFmt))

    elif s == '2':
        for yearint in range(int(yearfr),int(yearto)+1):
            year = "{:4d}".format(yearint)  # year = "%4d" %yearint
            msg = "\nCreating the sun tables only for the year {}".format(year)
            print(msg)
            first_day = datetime.date(yearint, 1, 1)
            filename = "sunalmanac{}{}.tex".format(ff,year+DecFmt)
            outfile = open(filename, mode="w", encoding="utf8")
            outfile.write(suntables.almanac(first_day,25))
            outfile.close()
            command = 'pdflatex {}'.format(filename)
            os.system(command)
            print("finished creating sun tables for {}".format(year))
            os.remove(filename)
            if os.path.isfile("sunalmanac{}{}.log".format(ff,symd+DecFmt)):
                os.remove("sunalmanac{}{}.log".format(ff,year+DecFmt))
            if os.path.isfile("sunalmanac{}{}.aux".format(ff,symd+DecFmt)):
                os.remove("sunalmanac{}{}.aux".format(ff,year+DecFmt))

    elif s == '3':
##        config.init()		# initialize log file
        msg = "\nCreating nautical almanac tables - from {}".format(sdmy)
        print(msg)
        filename = "almanac{}{}.tex".format(ff,symd+DecFmt)
        outfile = open(filename, mode="w", encoding="utf8")
        outfile.write(tables.almanac(first_day,2))
        outfile.close()
##        msg = 'Count of incorrect values: {}'.format(config.errors)
##        config.writeLOG('\n' + msg + '\n')
##        config.closeLOG()
        command = 'pdflatex {}'.format(filename)
        os.system(command)
        print("finished")
        os.remove(filename)
        if os.path.isfile("almanac{}{}.log".format(ff,symd+DecFmt)):
            os.remove("almanac{}{}.log".format(ff,symd+DecFmt))
        if os.path.isfile("almanac{}{}.aux".format(ff,symd+DecFmt)):
            os.remove("almanac{}{}.aux".format(ff,symd+DecFmt))

    elif s == '4':
        msg = "\nCreating the sun tables only - from {}".format(sdmy)
        print(msg)
        filename = "sunalmanac{}{}.tex".format(ff,symd+DecFmt)
        outfile = open(filename, mode="w", encoding="utf8")
        outfile.write(suntables.almanac(first_day,2))
        outfile.close()
        command = 'pdflatex {}'.format(filename)
        os.system(command)
        print("finished")
        os.remove(filename)
        if os.path.isfile("sunalmanac{}{}.log".format(ff,symd+DecFmt)):
            os.remove("sunalmanac{}{}.log".format(ff,symd+DecFmt))
        if os.path.isfile("sunalmanac{}{}.aux".format(ff,symd+DecFmt)):
            os.remove("sunalmanac{}{}.aux".format(ff,symd+DecFmt))
else:
    print("Error! Choose 1, 2, 3 or 4")
