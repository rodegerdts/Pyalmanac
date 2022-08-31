#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#   Copyright (C) 2014  Enno Rodegerdts
#   Copyright (C) 2022  Andrew Bauer

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

###### Standard library imports ######
import os
import sys
import time
from datetime import date, datetime, timedelta

###### Local application imports ######
import config
# !! execute the next 3 lines before importing from nautical/eventtables !!
config.WINpf = True if sys.platform.startswith('win') else False
config.LINUXpf = True if sys.platform.startswith('linux') else False
config.MACOSpf = True if sys.platform == 'darwin' else False
config.FANCYhd = False  # default for TeX Live <= "TeX Live 2019/Debian"
import nautical
import suntables
import eventtables
import increments


def toUnix(fn):
    if config.dockerized or config.LINUXpf or config.MACOSpf:
        fn = fn.replace("(","[").replace(")","]")
    return fn

def deletePDF(filename):
    if os.path.exists(filename + ".pdf"):
        try:
            os.remove(filename + ".pdf")
        except PermissionError:
            print("ERROR: please close '{}' so it can be re-created".format(filename + ".pdf"))
            sys.exit(0)
    if os.path.exists(filename + ".tex"):
        os.remove(filename + ".tex")

def makePDF(pdfcmd, fn, msg = ""):
    command = 'pdflatex {}'.format(pdfcmd + fn + ".tex")
    if pdfcmd == "":
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

def tidy_up(fn, kl, kt):
    if not kt: os.remove(fn + ".tex")
    if not kl:
        if os.path.isfile(fn + ".log"):
            os.remove(fn + ".log")
    if os.path.isfile(fn + ".aux"):
        os.remove(fn + ".aux")
    return

def check_exists(fn):
    # check a required file exist to avoid a more obscure error in pdfTeX if "-v" not used...
    if not os.path.exists(fn):
        print("Error - missing file: {}".format(fn))
        sys.exit(0)

def check_mth(mm):
    if not 1 <= int(mm) <= 12:
        print("ERROR: Enter month between 01 and 12")
        sys.exit(0)

def check_date(year, month, day):
    yy = int(year)
    mm = int(month)
    day_count_for_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if yy%4==0 and (yy%100 != 0 or yy%400==0):
        day_count_for_month[2] = 29
    if not (1 <= mm <= 12 and 1 <= int(day) <= day_count_for_month[mm]):
        print("ERROR: Enter a valid date")
        sys.exit(0)

def check_years(yearfr, yearto):
    global yrmin, yrmax

    if str(yearfr).isnumeric():
        if yrmin <= int(yearfr) <= yrmax:
            first_day = date(int(yearfr), 1, 1)
        else:
            print("!! Please pick a year between {} and {} !!".format(yrmin,yrmax))
            sys.exit(0)
    else:
        print("Error! First year is not numeric")
        sys.exit(0)

    if str(yearto).isnumeric():
        if yrmin <= int(yearto) <= yrmax:
            first_day_to = date(int(yearto), 1, 1)
        else:
            print("!! Please pick a year between {} and {} !!".format(yrmin,yrmax))
            sys.exit(0)
        if int(yearto) < int(yearfr):
            print("Error! The LAST year must be later than the FIRST year")
            sys.exit(0)
    else:
        print("Error! Last year is not numeric")
        sys.exit(0)


###### Main Program ######

if __name__ == '__main__':
    if sys.version_info[0] < 3:
        print("This runs only with Python 3")
        sys.exit(0)

    # check if TeX Live is compatible with the 'fancyhdr' package...
    process = os.popen("tex --version")
    returned_value = process.read()
    process.close()
    if returned_value == "":
        print("- - - Neither TeX Live nor MiKTeX is installed - - -")
        sys.exit(0)
    pos1 = returned_value.find("(") 
    pos2 = returned_value.find(")")
    if pos1 != -1 and pos2 != -1:
        texver = returned_value[pos1+1:pos2]
        # e.g. "TeX Live 2019/Debian", "TeX Live 2022/dev/Debian", "MiKTeX 22.7.30"
        if texver[:8] == "TeX Live":
            yrtxt = texver[9:13]
            if yrtxt.isnumeric():
                yr = int(yrtxt)
                if yr >= 2020:
                    config.FANCYhd = True  # TeX Live can handle the 'fancyhdr' package
#                if yr < 2020:
#                    print("TeX version = '" + texver + "'")
#                    print("Upgrade TeX Live to 'TeX Live 2020' at least")
#                    sys.exit(0)
        else:
            config.FANCYhd = True  # assume MiKTeX can handle the 'fancyhdr' package

    # command line arguments...
    validargs = ['-v', '-log', '-tex', '-old', 'a4', '-let', '-dpo']
    for i in list(range(1, len(sys.argv))):
        if sys.argv[i] not in validargs:
            print("Invalid argument: {}".format(sys.argv[i]))
            print("\nValid command line arguments are:")
            print(" -v   ... 'verbose': to send pdfTeX output to the terminal")
            print(" -log ... to keep the log file")
            print(" -tex ... to keep the tex file")
            print(" -old ... old formatting without the fancyhdr package")
            print(" -a4  ... A4 papersize")
            print(" -let ... Letter papersize")
            print(" -dpo ... data pages only")
            sys.exit(0)

    # NOTE: pdfTeX 3.14159265-2.6-1.40.21 (TeX Live 2020/Debian), as used in the Docker
    #       Image, does not have the options "-quiet" or "-verbose".
    listarg = "" if "-v" in set(sys.argv[1:]) else "-interaction=batchmode -halt-on-error "
    keeplog = True if "-log" in set(sys.argv[1:]) else False
    keeptex = True if "-tex" in set(sys.argv[1:]) else False
    config.DPonly = True if "-dpo" in set(sys.argv[1:]) else False
    if "-old" in set(sys.argv[1:]): config.FANCYhd = False  # don't use the 'fancyhdr' package
    forcepgsz = False
    if not("-a4" in set(sys.argv[1:]) and "-let" in set(sys.argv[1:])):
        if "-a4" in set(sys.argv[1:]): forcepgsz = True
        if "-let" in set(sys.argv[1:]): forcepgsz = True
    if forcepgsz:
        if "-a4" in set(sys.argv[1:]): config.pgsz = "A4"
        if "-let" in set(sys.argv[1:]): config.pgsz = "Letter"

    d = datetime.utcnow().date()
    first_day = date(d.year, d.month, d.day)
    yy = "%s" % d.year

    # if this code runs locally (not in Docker), the settings in config.py are used.
    # if this code runs in Docker without use of an environment file, the settings in config.py apply.
    # if this code runs in Docker with an environment file ("--env-file ./.env"), then its values apply.
    if config.dockerized:
        docker_main = os.getcwd()
        spdf = docker_main + "/"            # path to pdf/png/jpg in the Docker Image
        config.pgsz = os.getenv('PGSZ', config.pgsz)
        config.search_next_rising_sun = os.getenv('SNRS', str(config.search_next_rising_sun))
        stdt = os.getenv('SDATE', 'None')
        if stdt != 'None':      # for testing a specific date
            try:
                first_day = date(int(stdt[0:4]), int(stdt[5:7]), int(stdt[8:10]))
            except:
                print("Invalid date format for SDATE in .env: {}".format(stdt))
                sys.exit(0)
            d = first_day
        err1 = " the Docker .env file"
        err2 = "for SNRS in the Docker .env file"
    else:
        spad = spdf = "./"   # path when executing the GitHub files in a folder
        config.search_next_rising_sun = str(config.search_next_rising_sun)
        err1 = "config.py"
        err2 = "for search_next_rising_sun in config.py"

    if config.pgsz not in set(['A4', 'Letter']):
        print("Please choose a valid paper size in {}".format(err1))
        sys.exit(0)

    if config.search_next_rising_sun.lower() not in set(['true', 'false']):
        print("Please choose a boolean value {}".format(err2))
        sys.exit(0)

    # ------------ process user input ------------

    global yrmin, yrmax
    yrmin = 1000
    yrmax = 3000
    config.search_next_rising_sun = (config.search_next_rising_sun.lower() == 'true')   # to boolean
    f_prefix = config.docker_prefix
    f_postfix = config.docker_postfix

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
                    sys.exit(0)

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
                
                first_day = date(int(yy), int(mm), int(dd))
                d = first_day

                if not entireYr and not entireMth and daystoprocess == 0:
                    daystoprocess = 1       # default
                    nn = input("""  Enter number of days to process from starting date:
""")
                    if len(nn) > 0:
                        if not nn.isnumeric():
                            print("ERROR: Not a number")
                            sys.exit(0)
                        daystoprocess = int(nn)
                        if daystoprocess > 300:
                            print("ERROR: 'Days to process' not <= 300")
                            sys.exit(0)

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
        #print(datetime.now().time())
        papersize = config.pgsz

    # ------------ create the desired tables ------------

        if s == '1' and entireYr:        # Nautical Almanac (for a year)
            check_exists(spdf + "A4chartNorth_P.pdf")
            print("Please wait - this can take a while.")
            for yearint in range(int(yearfr),int(yearto)+1):
                start = time.time()
                year = "{:4d}".format(yearint)  # year = "%4d" %yearint
                msg = "\nCreating the nautical almanac for the year {}\n".format(year)
                print(msg)
                first_day = date(yearint, 1, 1)
                ff = "NAtrad" if config.tbls != 'm' else "NAmod"
                fn = toUnix("{}({})_{}".format(ff,papersize,year+DecFmt))
                deletePDF(f_prefix + fn)
                # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
                outfile.write(nautical.almanac(first_day,0))
                outfile.close()
                # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                stop = time.time()
                msg = "execution time = {:0.2f} seconds".format(stop-start)
                print(msg)
                print()
                if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
                makePDF(listarg, fn)
                tidy_up(fn, keeplog, keeptex)
                if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

        if s == '1' and entireMth:        # Nautical Almanac (for a month)
            check_exists(spdf + "A4chartNorth_P.pdf")
            start = time.time()
            msg = "\nCreating the nautical almanac for {}".format(first_day.strftime("%B %Y"))
            print(msg)
            ff = "NAtrad" if config.tbls != 'm' else "NAmod"
            fn = toUnix("{}({})_{}".format(ff,papersize,syr + '-' + smth + DecFmt))
            deletePDF(f_prefix + fn)
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
            outfile.write(nautical.almanac(first_day,-1))
            outfile.close()
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            stop = time.time()
            msg = "execution time = {:0.2f} seconds".format(stop-start)
            print(msg)
            print()
            if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
            makePDF(listarg, fn)
            tidy_up(fn, keeplog, keeptex)
            if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

        if s == '1' and not entireYr and not entireMth:       # Nautical Almanac (for a few days)
            check_exists(spdf + "A4chartNorth_P.pdf")
            start = time.time()
            txt = "from" if daystoprocess > 1 else "for"
            msg = "\nCreating the nautical almanac {} {}".format(txt,first_day.strftime("%d %B %Y"))
            print(msg)
            ff = "NAtrad" if config.tbls != 'm' else "NAmod"
            dto = ""
            if daystoprocess > 1:   # filename as 'from date'-'to date'
                lastdate = d + timedelta(days=daystoprocess-1)
                dto = lastdate.strftime("-%Y%m%d")
            fn = toUnix("{}({})_{}".format(ff,papersize,symd+dto+DecFmt))
            deletePDF(f_prefix + fn)
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
            outfile.write(nautical.almanac(first_day,daystoprocess))
            outfile.close()
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            stop = time.time()
            msg = "execution time = {:0.2f} seconds".format(stop-start)
            print(msg)
            print()
            if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
            makePDF(listarg, fn)
            tidy_up(fn, keeplog, keeptex)
            if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

        elif s == '2' and entireYr:      # Sun Tables (for a year)
            check_exists(spdf + "Ra.jpg")
            for yearint in range(int(yearfr),int(yearto)+1):
                year = "{:4d}".format(yearint)  # year = "%4d" %yearint
                msg = "\nCreating the sun tables for the year {}\n".format(year)
                print(msg)
                first_day = date(yearint, 1, 1)
                ff = "STtrad" if config.tbls != 'm' else "STmod"
                fn = toUnix("{}({})_{}".format(ff,papersize,year+DecFmt))
                deletePDF(f_prefix + fn)
                # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
                outfile.write(suntables.sunalmanac(first_day,0))
                outfile.close()
                # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
                makePDF(listarg, fn)
                tidy_up(fn, keeplog, keeptex)
                if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

        elif s == '2' and entireMth:      # Sun Tables (for a month)
            check_exists(spdf + "Ra.jpg")
            msg = "\nCreating the sun tables for {}".format(first_day.strftime("%B %Y"))
            print(msg)
            ff = "STtrad" if config.tbls != 'm' else "STmod"
            fn = toUnix("{}({})_{}".format(ff,papersize,syr + '-' + smth + DecFmt))
            deletePDF(f_prefix + fn)
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
            outfile.write(suntables.sunalmanac(first_day,-1))
            outfile.close()
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
            makePDF(listarg, fn)
            tidy_up(fn, keeplog, keeptex)
            if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

        elif s == '2' and not entireYr and not entireMth:   # Sun Tables (for a few days)
            check_exists(spdf + "Ra.jpg")
            txt = "from" if daystoprocess > 1 else "for"
            msg = "\nCreating the sun tables {} {}".format(txt,first_day.strftime("%d %B %Y"))
            print(msg)
            ff = "STtrad" if config.tbls != 'm' else "STmod"
            dto = ""
            if daystoprocess > 1:   # filename as 'from date'-'to date'
                lastdate = d + timedelta(days=daystoprocess-1)
                dto = lastdate.strftime("-%Y%m%d")
            fn = toUnix("{}({})_{}".format(ff,papersize,symd+dto+DecFmt))
            deletePDF(f_prefix + fn)
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
            outfile.write(suntables.sunalmanac(first_day,daystoprocess))
            outfile.close()
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
            makePDF(listarg, fn)
            tidy_up(fn, keeplog, keeptex)
            if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

        elif s == '3' and entireYr:      # Event Time tables  (for a year)
            check_exists(spdf + "A4chartNorth_P.pdf")
            print("Please wait - this can take a while.")
            for yearint in range(int(yearfr),int(yearto)+1):
                start = time.time()
                year = "{:4d}".format(yearint)  # year = "%4d" %yearint
                msg = "\nCreating the event time tables for the year {}\n".format(year)
                print(msg)
                first_day = date(yearint, 1, 1)
                fn = toUnix("Event-Times({})_{}".format(papersize,year))
                deletePDF(f_prefix + fn)
                # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
                outfile.write(eventtables.makeEVtables(first_day,0))
                outfile.close()
                # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                stop = time.time()
                msg = "execution time = {:0.2f} seconds".format(stop-start)
                print(msg)
                print()
                if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
                makePDF(listarg, fn)
                tidy_up(fn, keeplog, keeptex)
                if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

        elif s == '3' and entireMth:      # Event Time tables  (for a month)
            check_exists(spdf + "A4chartNorth_P.pdf")
            start = time.time()
            msg = "\nCreating the event time tables for {}".format(first_day.strftime("%B %Y"))
            print(msg)
            fn = toUnix("Event-Times({})_{}".format(papersize,syr + '-' + smth))
            deletePDF(f_prefix + fn)
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
            outfile.write(eventtables.makeEVtables(first_day,-1))
            outfile.close()
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            stop = time.time()
            msg = "execution time = {:0.2f} seconds".format(stop-start)
            print(msg)
            print()
            if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
            makePDF(listarg, fn)
            tidy_up(fn, keeplog, keeptex)
            if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

        elif s == '3' and not entireYr and not entireMth:   # Event Time tables (for a few days)
            check_exists(spdf + "A4chartNorth_P.pdf")
            start = time.time()
            txt = "from" if daystoprocess > 1 else "for"
            msg = "\nCreating the event time tables {} {}".format(txt,first_day.strftime("%d %B %Y"))
            print(msg)
            fn = toUnix("Event-Times({})_{}".format(papersize,symd))
            if daystoprocess > 1:   # filename as 'from date'-'to date'
                lastdate = d + timedelta(days=daystoprocess-1)
                fn += lastdate.strftime("-%Y%m%d")
            deletePDF(f_prefix + fn)
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
            outfile.write(eventtables.makeEVtables(first_day,daystoprocess))
            outfile.close()
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            stop = time.time()
            msg = "execution time = {:0.2f} seconds".format(stop-start)
            print(msg)
            print()
            if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
            makePDF(listarg, fn)
            tidy_up(fn, keeplog, keeptex)
            if config.dockerized: os.chdir(docker_main)     # reset working folder to code folder

        elif s == '4':      # Nautical almanac   -  6 days from today
            check_exists(spdf + "A4chartNorth_P.pdf")
    ##        config.initLOG()		# initialize log file
            msg = "\nCreating nautical almanac tables - from {}\n".format(sdmy)
            print(msg)
            ff = "NAtrad" if config.tbls != 'm' else "NAmod"
            lastdate = d + timedelta(days=5)
            dto = lastdate.strftime("-%Y%m%d")
            fn = toUnix("{}({})_{}".format(ff,papersize,symd+dto+DecFmt))
            deletePDF(f_prefix + fn)
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
            outfile.write(nautical.almanac(first_day,6))
            outfile.close()
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    ##        msg = 'Count of incorrect values: {}'.format(config.errors)
    ##        config.writeLOG('\n' + msg + '\n')
    ##        config.closeLOG()
            if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
            makePDF(listarg, fn)
            tidy_up(fn, keeplog, keeptex)

        elif s == '5':      # Sun tables only    - 30 days from today
            check_exists(spdf + "Ra.jpg")
            msg = "\nCreating the sun tables - from {}\n".format(sdmy)
            print(msg)
            ff = "STtrad" if config.tbls != 'm' else "STmod"
            lastdate = d + timedelta(days=29)
            dto = lastdate.strftime("-%Y%m%d")
            fn = toUnix("{}({})_{}".format(ff,papersize,symd+dto+DecFmt))
            deletePDF(f_prefix + fn)
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
            outfile.write(suntables.sunalmanac(first_day,30))
            outfile.close()
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
            makePDF(listarg, fn)
            tidy_up(fn, keeplog, keeptex)

        elif s == '6':      # Event Time tables  -  6 days from today
            check_exists(spdf + "A4chartNorth_P.pdf")
            msg = "\nCreating event time tables - from {}\n".format(sdmy)
            print(msg)
            fn = toUnix("Event-Times({})_{}".format(papersize,symd))
            lastdate = d + timedelta(days=5)
            fn += lastdate.strftime("-%Y%m%d")
            deletePDF(f_prefix + fn)
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
            outfile.write(eventtables.makeEVtables(first_day,6))
            outfile.close()
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
            makePDF(listarg, fn)
            tidy_up(fn, keeplog, keeptex)

        elif s == '7':  # Increments and Corrections tables
            msg = "\nCreating the Increments and Corrections tables\n"
            print(msg)
            fn = toUnix("Inc({})").format(papersize)
            deletePDF(f_prefix + fn)
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            outfile = open(f_prefix + fn + ".tex", mode="w", encoding="utf8")
            outfile.write(increments.makelatex())
            outfile.close()
            # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            if config.dockerized: os.chdir(os.getcwd() + f_postfix)     # DOCKER ONLY
            makePDF(listarg, fn)
            tidy_up(fn, keeplog, keeptex)

    else:
        print("Error! Choose 1, 2, 3, 4, 5, 6 or 7")
