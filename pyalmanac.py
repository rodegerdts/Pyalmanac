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
import nautical
import suntables
import eventtables
import config
import increments


def deletePDF(filename):
    if os.path.exists(filename + ".pdf"):
        try:
            os.remove(filename + ".pdf")
        except PermissionError:
            print("ERROR: please close '{}' so it can be re-created".format(filename + ".pdf"))
            sys.exit(0)
    if os.path.exists(filename + ".tex"):
        os.remove(filename + ".tex")

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
                print("finished creating '{}'".format(fn + ".pdf"))
    return

def check_mth(mm):
    if not 1 <= int(mm) <= 12:
        print("ERROR: Enter month between 01 and 12")
        sys.exit()

def check_date(year, month, day):
    yy = int(year)
    mm = int(month)
    day_count_for_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if yy%4==0 and (yy%100 != 0 or yy%400==0):
        day_count_for_month[2] = 29
    if not (1 <= mm <= 12 and 1 <= int(day) <= day_count_for_month[mm]):
        print("ERROR: Enter a valid date")
        sys.exit()

def check_years(yearfr, yearto):
    global yrmin, yrmax

    if str(yearfr).isnumeric():
        if yrmin <= int(yearfr) <= yrmax:
            first_day = datetime.date(int(yearfr), 1, 1)
        else:
            print("!! Please pick a year between {} and {} !!".format(yrmin,yrmax))
            sys.exit(0)
    else:
        print("Error! First year is not numeric")
        sys.exit(0)

    if str(yearto).isnumeric():
        if yrmin <= int(yearto) <= yrmax:
            first_day_to = datetime.date(int(yearto), 1, 1)
        else:
            print("!! Please pick a year between {} and {} !!".format(yrmin,yrmax))
            sys.exit(0)
        if int(yearto) < int(yearfr):
            print("Error! The LAST year must be later than the FIRST year")
            sys.exit(0)
    else:
        print("Error! Last year is not numeric")
        sys.exit(0)

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
yy = "%s" % d.year

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
    config.search_next_rising_sun = str(config.search_next_rising_sun)
    err1 = "config.py"
    err2 = "for search_next_rising_sun in config.py"

if config.pgsz not in set(['A4', 'Letter']):
    print("Please choose a valid paper size in {}".format(err1))
    sys.exit(0)

if config.search_next_rising_sun.lower() not in set(['true', 'false']):
    print("Please choose a boolean value {}".format(err2))
    sys.exit(0)

global yrmin, yrmax
yrmin = 1000
yrmax = 3000
config.search_next_rising_sun = (config.search_next_rising_sun.lower() == 'true')   # to boolean
f_prefix = config.docker_prefix
f_postfix = config.docker_postfix

# ------------ process user input ------------

s = input("""\nWhat do you want to create?:\n
    1   Nautical Almanac   (for a day/month/year)
    2   Sun tables only    (for a day/month/year)
    3   Event Time tables  (for a day/month/year)
    4   Nautical almanac   -  6 days from today
    5   Sun tables only    - 30 days from today
    6   Event Time tables  -  6 days from today
    7   "Increments and Corrections" tables (static data)
""")

if s in set(['1', '2', '3', '4', '5', '6', '7']):
    if int(s) < 4:
        daystoprocess = 0
        ss = input("""  Enter as numeric digits:\n
    - starting date as 'DDMMYYYY'
    - or just 'YYYY' (for a whole year)
    - or 'YYYY-YYYY' (for first and last year)
    - or just 'MM' (01 - 12) for the current or a future month
    - or '-MM' for a previous month (e.g. '-02' is last February)
    - nothing for the current day
""")
        sErr = False    # syntax error
        entireMth = False
        entireYr  = False

        if len(ss) == 0:
            daystoprocess = 1
            if d.year > yrmax:
                print("!! Only years up to {} are valid!!".format(yrmax))
                sys.exit(0)
        else:
            if len(ss) not in [2,3,4,8,9]: sErr = True
            if len(ss) == 3:
                if ss[0] != '-': sErr = True
                if not ss[1:].isnumeric(): sErr = True
            elif len(ss) == 9:
                if ss[4] != '-': sErr = True
                if not (ss[:4].isnumeric() and ss[5:].isnumeric()): sErr = True
            elif not ss.isnumeric(): sErr = True

            if sErr:
                print("ERROR: Enter numeric digits in the correct format")
                sys.exit()

            if len(ss) == 2:
                entireMth = True
                dd = "01"
                mm = ss[0:2]
                check_mth(mm)
                if int(mm) < d.month: yy = str(d.year + 1)
            elif len(ss) == 3:
                entireMth = True
                dd = "01"
                mm = ss[1:3]
                check_mth(mm)
                if int(mm) >= d.month: yy = str(d.year - 1)
            elif len(ss) == 4:
                entireYr = True
                dd = "01"
                mm = "01"
                yy = ss
                yearfr = ss
                yearto = ss
                check_years(yearfr, yearto)
            elif len(ss) == 9 and ss[4] == '-':
                entireYr = True
                dd = "01"
                mm = "01"
                yy = ss[0:4]
                yearfr = ss[0:4]
                yearto = ss[5:]
                check_years(yearfr, yearto)
            elif len(ss) == 8:
                dd = ss[:2]
                mm = ss[2:4]
                check_mth(mm)
                yy = ss[4:]
                check_date(yy,mm,dd)
            
            first_day = datetime.date(int(yy), int(mm), int(dd))
            d = first_day

            if not entireYr and not entireMth and daystoprocess == 0:
                daystoprocess = 1       # default
                nn = input("""  Enter number of days to process from starting date:
""")
                if len(nn) > 0:
                    if not nn.isnumeric():
                        print("ERROR: Not a number")
                        sys.exit()
                    daystoprocess = int(nn)
                    if daystoprocess > 300:
                        print("ERROR: 'Days to process' not <= 300")
                        sys.exit()

    if s != '3' and int(s) <= 5:
        tsin = input("""  What table style is required?:\n
    t   Traditional
    m   Modern
""")
        ff = '_'
        DecFmt = ''
        config.tbls = tsin[0:1]	# table style
        config.decf = tsin[1:2]	# Declination format ('+' or nothing)
        if config.tbls != 'm':
            config.tbls = ''		# anything other than 'm' is traditional
            ff = ''
        if config.decf != '+':		# Positive/Negative Declinations
            config.decf = ''		# USNO format for Declination
        else:
            DecFmt = '[old]'

    sday = "{:02d}".format(d.day)       # sday = "%02d" % d.day
    smth = "{:02d}".format(d.month)     # smth = "%02d" % d.month
    syr  = "{}".format(d.year)          # syr  = "%s" % d.year
    symd = syr + smth + sday
    sdmy = sday + "." + smth + "." + syr
    #print(datetime.datetime.now().time())

# ------------ create the desired tables ------------

    if s == '1' and entireYr:        # Nautical Almanac (for a year)
        print("Please wait - this can take a while.")
        for yearint in range(int(yearfr),int(yearto)+1):
            start = time.time()
            year = "{:4d}".format(yearint)  # year = "%4d" %yearint
            msg = "\nCreating the nautical almanac for the year {}\n".format(year)
            print(msg)
            first_day = datetime.date(yearint, 1, 1)
            ff = "NAtrad_" if config.tbls != 'm' else "NAmod_"
            fn = "{}{}".format(ff,year+DecFmt)
            deletePDF(f_prefix + fn)
            outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
            outfile.write(nautical.almanac(first_day,0))
            outfile.close()
            stop = time.time()
            msg = "execution time = {:0.2f} seconds".format(stop-start)
            print(msg)
            print()
            if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
            makePDF(args, fn)
            tidy_up(fn)
            if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

    if s == '1' and entireMth:        # Nautical Almanac (for a month)
        start = time.time()
        msg = "\nCreating the nautical almanac for {}".format(first_day.strftime("%B %Y"))
        print(msg)
        ff = "NAtrad_" if config.tbls != 'm' else "NAmod_"
        fn = "{}{}".format(ff,syr + '-' + smth + DecFmt)
        deletePDF(f_prefix + fn)
        outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
        outfile.write(nautical.almanac(first_day,-1))
        outfile.close()
        stop = time.time()
        msg = "execution time = {:0.2f} seconds".format(stop-start)
        print(msg)
        print()
        if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
        makePDF(args, fn)
        tidy_up(fn)
        if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

    if s == '1' and not entireYr and not entireMth:       # Nautical Almanac (for a few days)
        start = time.time()
        txt = "from" if daystoprocess > 1 else "for"
        msg = "\nCreating the nautical almanac {} {}".format(txt,first_day.strftime("%d %B %Y"))
        print(msg)
        ff = "NAtrad_" if config.tbls != 'm' else "NAmod_"
        dto = ""
        if daystoprocess > 1:   # filename as 'from date'-'to date'
            lastdate = d + datetime.timedelta(days=daystoprocess-1)
            dto = lastdate.strftime("-%Y%m%d")
        fn = "{}".format(ff+symd+dto+DecFmt)
        deletePDF(f_prefix + fn)
        outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
        outfile.write(nautical.almanac(first_day,daystoprocess))
        outfile.close()
        stop = time.time()
        msg = "execution time = {:0.2f} seconds".format(stop-start)
        print(msg)
        print()
        if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
        makePDF(args, fn)
        tidy_up(fn)
        if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

    elif s == '2' and entireYr:      # Sun Tables (for a year)
        for yearint in range(int(yearfr),int(yearto)+1):
            year = "{:4d}".format(yearint)  # year = "%4d" %yearint
            msg = "\nCreating the sun tables for the year {}\n".format(year)
            print(msg)
            first_day = datetime.date(yearint, 1, 1)
            ff = "STtrad_" if config.tbls != 'm' else "STmod_"
            fn = "{}{}".format(ff,year+DecFmt)
            deletePDF(f_prefix + fn)
            outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
            outfile.write(suntables.sunalmanac(first_day,0))
            outfile.close()
            if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
            makePDF(args, fn)
            tidy_up(fn)
            if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

    elif s == '2' and entireMth:      # Sun Tables (for a month)
        msg = "\nCreating the sun tables for {}".format(first_day.strftime("%B %Y"))
        print(msg)
        ff = "STtrad_" if config.tbls != 'm' else "STmod_"
        fn = "{}{}".format(ff,syr + '-' + smth + DecFmt)
        deletePDF(f_prefix + fn)
        outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
        outfile.write(suntables.sunalmanac(first_day,-1))
        outfile.close()
        if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
        makePDF(args, fn)
        tidy_up(fn)
        if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

    elif s == '2' and not entireYr and not entireMth:   # Sun Tables (for a few days)
        txt = "from" if daystoprocess > 1 else "for"
        msg = "\nCreating the sun tables {} {}".format(txt,first_day.strftime("%d %B %Y"))
        print(msg)
        ff = "STtrad_" if config.tbls != 'm' else "STmod_"
        dto = ""
        if daystoprocess > 1:   # filename as 'from date'-'to date'
            lastdate = d + datetime.timedelta(days=daystoprocess-1)
            dto = lastdate.strftime("-%Y%m%d")
        fn = "{}".format(ff+symd+dto+DecFmt)
        deletePDF(f_prefix + fn)
        outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
        outfile.write(suntables.sunalmanac(first_day,daystoprocess))
        outfile.close()
        if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
        makePDF(args, fn)
        tidy_up(fn)
        if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

    elif s == '3' and entireYr:      # Event Time tables  (for a year)
        print("Please wait - this can take a while.")
        for yearint in range(int(yearfr),int(yearto)+1):
            start = time.time()
            year = "{:4d}".format(yearint)  # year = "%4d" %yearint
            msg = "\nCreating the event time tables for the year {}\n".format(year)
            print(msg)
            first_day = datetime.date(yearint, 1, 1)
            fn = "Event-Times_{}".format(year)
            deletePDF(f_prefix + fn)
            outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
            outfile.write(eventtables.maketables(first_day,0))
            outfile.close()
            stop = time.time()
            msg = "execution time = {:0.2f} seconds".format(stop-start)
            print(msg)
            print()
            if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
            makePDF(args, fn)
            tidy_up(fn)
            if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

    elif s == '3' and entireMth:      # Event Time tables  (for a month)
        start = time.time()
        msg = "\nCreating the event time tables for {}".format(first_day.strftime("%B %Y"))
        print(msg)
        fn = "Event-Times_{}".format(syr + '-' + smth)
        deletePDF(f_prefix + fn)
        outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
        outfile.write(eventtables.maketables(first_day,-1))
        outfile.close()
        stop = time.time()
        msg = "execution time = {:0.2f} seconds".format(stop-start)
        print(msg)
        print()
        if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
        makePDF(args, fn)
        tidy_up(fn)
        if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

    elif s == '3' and not entireYr and not entireMth:   # Event Time tables (for a few days)
        start = time.time()
        txt = "from" if daystoprocess > 1 else "for"
        msg = "\nCreating the event time tables {} {}".format(txt,first_day.strftime("%d %B %Y"))
        print(msg)
        fn = "Event-Times_{}".format(symd)
        if daystoprocess > 1:   # filename as 'from date'-'to date'
            lastdate = d + datetime.timedelta(days=daystoprocess-1)
            fn += lastdate.strftime("-%Y%m%d")
        deletePDF(f_prefix + fn)
        outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
        outfile.write(eventtables.maketables(first_day,daystoprocess))
        outfile.close()
        stop = time.time()
        msg = "execution time = {:0.2f} seconds".format(stop-start)
        print(msg)
        print()
        if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
        makePDF(args, fn)
        tidy_up(fn)
        if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

    elif s == '4':      # Nautical almanac   -  6 days from today
##        config.initLOG()		# initialize log file
        msg = "\nCreating nautical almanac tables - from {}\n".format(sdmy)
        print(msg)
        ff = "NAtrad_" if config.tbls != 'm' else "NAmod_"
        fn = "{}".format(ff+symd)
        lastdate = d + datetime.timedelta(days=5)
        fn += lastdate.strftime("-%Y%m%d") + DecFmt
        deletePDF(f_prefix + fn)
        outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
        outfile.write(nautical.almanac(first_day,6))
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
        ff = "STtrad_" if config.tbls != 'm' else "STmod_"
        fn = "{}".format(ff+symd)
        lastdate = d + datetime.timedelta(days=29)
        fn += lastdate.strftime("-%Y%m%d") + DecFmt
        deletePDF(f_prefix + fn)
        outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
        outfile.write(suntables.sunalmanac(first_day,30))
        outfile.close()
        if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
        makePDF(args, fn)
        tidy_up(fn)

    elif s == '6':      # Event Time tables  -  6 days from today
        msg = "\nCreating event time tables - from {}\n".format(sdmy)
        print(msg)
        fn = "Event-Times_{}".format(symd)
        lastdate = d + datetime.timedelta(days=5)
        fn += lastdate.strftime("-%Y%m%d")
        deletePDF(f_prefix + fn)
        outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
        outfile.write(eventtables.maketables(first_day,6))
        outfile.close()
        if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
        makePDF(args, fn)
        tidy_up(fn)

    elif s == '7':
        msg = "\nCreating the Increments and Corrections tables\n"
        print(msg)
        fn = "Inc"
        deletePDF(f_prefix + fn)
        outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
        outfile.write(increments.makelatex())
        outfile.close()
        if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
        makePDF(args, fn)
        tidy_up(fn)

else:
    print("Error! Choose 1, 2, 3, 4, 5, 6 or 7")
