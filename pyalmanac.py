#! /usr/bin/python
# -*- coding: UTF-8 -*-

#	Copyright (C) 2014  Enno Rodegerdts

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


##Main###
year =  raw_input("Please enter the year you want to create the nautical almanac for:\n ")
s =  raw_input("""Do you want to create the full tables or just tables for the sun?:\n
1	Full nautical almanac
2	Just tables for the sun
""")
if s == "2":
	print "Creating the sun tables only. \n The year %s" %year
	print "Please wait this can take a while."
	filename = "sunalmanac%s.tex" %year
	outfile = open(filename, 'w')
	outfile.write(suntables.almanac(year))
	outfile.close()
	command = 'pdflatex %s' %filename
	os.system(command)
	print "finished"
	os.remove("sunalmanac%s.log" %year)
	os.remove("sunalmanac%s.aux" %year)
	os.remove(filename)
elif s == "1":
	print "Creating the nautical almanac for the year %s" %year
	print "Please wait this can take a while."
	filename = "almanac%s.tex" %year
	outfile = open(filename, 'w')
	outfile.write(tables.almanac(year))
	outfile.close()
	command = 'pdflatex %s' %filename
	os.system(command)
	print "finished"
	os.remove(filename)
	os.remove("almanac%s.log" %year)
	os.remove("almanac%s.aux" %year)
else:
	print "Error! Choose either 1 or 2"
	