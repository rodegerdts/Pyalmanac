#!/usr/bin/env python2
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
import datetime
import config

##Main##
d = datetime.datetime.utcnow().date()
first_day = datetime.date(d.year, d.month, d.day)

#first_day = datetime.date(2019, 1, 1)	# for testing a specific date
#d = first_day							# for testing a specific date

sday = "%02d" % d.day
smth = "%02d" % d.month
syr  = "%s" % d.year
symd = syr + smth + sday
sdmy = sday + "." + smth + "." + syr
#print 'Today is %s' %symd

s =  raw_input("""What do you want to create?:\n
1   Full nautical almanac   (for a year)
2   Just tables for the sun (for a year)
3   Nautical almanac   - 6 days from today
4   Tables for the sun - 30 days from today
""")

if s in set(['1', '2', '3', '4']):
    if int(s) < 3:
        year =  raw_input("Please enter the year you want to create the nautical almanac for:\n ")
        if unicode(year, 'utf-8').isnumeric():
            if 1000 <= int(year) <= 3000:
                first_day = datetime.date(int(year), 1, 1)
            else:
                print "Error! Please pick a year between 1000 and 3000"
                sys.exit(0)
        else:
            print "Error! Year is not numeric"
            sys.exit(0)

    tsin = raw_input("""What table  style is required?:\n
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
        print "Creating the nautical almanac for the year %s" %year
        print "Please wait - this can take a while."
        filename = "almanac%s%s.tex" %(ff,year+DecFmt)
        outfile = open(filename, 'w')
        outfile.write(tables.almanac(first_day,122))
        outfile.close()
        command = 'pdflatex %s' %filename
        os.system(command)
        print "finished"
        os.remove(filename)
        os.remove("almanac%s%s.log" %(ff,year+DecFmt))
        os.remove("almanac%s%s.aux" %(ff,year+DecFmt))

    elif s == '2':
        print "Creating the sun tables only. \n The year %s" %year
        print "Please wait - this can take a while."
        filename = "sunalmanac%s%s.tex" %(ff,year+DecFmt)
        outfile = open(filename, 'w')
        outfile.write(suntables.almanac(first_day,25))
        outfile.close()
        command = 'pdflatex %s' %filename
        os.system(command)
        print "finished"
        os.remove(filename)
        os.remove("sunalmanac%s%s.log" %(ff,year+DecFmt))
        os.remove("sunalmanac%s%s.aux" %(ff,year+DecFmt))

    elif s == '3':
##        config.init()		# initialize error logging
        print "Creating nautical almanac tables - from %s" %(sdmy)
        filename = "almanac%s%s.tex" %(ff,symd+DecFmt)
        outfile = open(filename, 'w')
        outfile.write(tables.almanac(first_day,2))
        outfile.close()
##        err = 'Count of incorrect values: %s' %config.errors
##        config.writeERR('\n' + err + '\n')
##        config.closeERR()
        command = 'pdflatex %s' %filename
        os.system(command)
        print "finished"
        os.remove(filename)
        os.remove("almanac%s%s.log" %(ff,symd+DecFmt))
        os.remove("almanac%s%s.aux" %(ff,symd+DecFmt))

    elif s == '4':
        print "Creating the sun tables only - from %s" %(sdmy)
        filename = "sunalmanac%s%s.tex" %(ff,symd+DecFmt)
        outfile = open(filename, 'w')
        outfile.write(suntables.almanac(first_day,2))
        outfile.close()
        command = 'pdflatex %s' %filename
        os.system(command)
        print "finished"
        os.remove(filename)
        os.remove("sunalmanac%s%s.log" %(ff,symd+DecFmt))
        os.remove("sunalmanac%s%s.aux" %(ff,symd+DecFmt))
else:
    print "Error! Choose 1, 2, 3 or 4"
