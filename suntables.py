#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

import config
from alma_ephem import *

def suntab(date):
    # generates LaTeX table for sun only (traditional)
    tab = r'''\noindent
\begin{tabular*}{0.2\textwidth}[t]{@{\extracolsep{\fill}}|c|rr|}
'''
    n = 0
    while n < 3:
        da = date + n
        tab = tab + r'''\hline
\multicolumn{1}{|c|}{\rule{0pt}{2.6ex}\textbf{%s}} & \multicolumn{1}{c}{\textbf{GHA}} & \multicolumn{1}{c|}{\textbf{Dec}}\\
\hline\rule{0pt}{2.6ex}\noindent
''' %(ephem.date(da).datetime().strftime("%d"))
        h = 0

        if config.decf != '+':	# USNO format for Declination
            # first populate an array of 24 hours with all data
            hourlydata = [[] for i in range(24)]
            while h < 24:
                hourlydata[h] = sunmoon(da)
                da = da + ephem.hour
                h += 1
            # now print the data per hour
            da = date + n
            h = 0

            while h < 24:
                eph = hourlydata[h]
                if h > 0:
                    preveph = hourlydata[h-1]
                else:
                    preveph = hourlydata[0]		# hour -1 = hour 0
                if h < 23:
                    nexteph = hourlydata[h+1]
                else:
                    nexteph = hourlydata[23]	# hour 24 = hour 23

                # format declination checking for hemisphere change
                printNS, printDEG = declCompare(preveph[7],eph[7],nexteph[7],h)
                sdec = NSdecl(eph[1],h,printNS,printDEG,False)

                line = "%s & %s & %s" %(h,eph[0],sdec)
                lineterminator = r'''\\
'''
                if h < 23 and (h+1)%6 == 0:
                    lineterminator = r'''\\[2Pt]
'''
                tab = tab + line + lineterminator
                h += 1
                da = da + ephem.hour

        else:			# Positive/Negative Declinations
            while h < 24:
                eph = sunmoon(da)
                line = "%s & %s & %s" %(h,eph[0],eph[1])
                lineterminator = r'''\\
'''
                if h < 23 and (h+1)%6 == 0:
                    lineterminator = r'''\\[2Pt]
'''
                tab = tab + line + lineterminator
                h += 1
                da = da + ephem.hour

        vd = sun_moon_SD(date + n)
        tab = tab + r'''\hline
\rule{0pt}{2.4ex} & \multicolumn{1}{c}{SD.=%s} & \multicolumn{1}{c|}{d=%s}\\
\hline
''' %(vd[1],vd[0])
        if n < 2:
            # add space between tables...
            tab = tab + r'''\multicolumn{1}{c}{}\\[-0.5ex]'''
        n += 1

    tab = tab + r'''\end{tabular*}'''
    return tab


def suntabm(date):
    # generates LaTeX table for sun only (modern)
    if config.decf != '+':	# USNO format for Declination
        tabsep = "4pt"
    else:
        tabsep = "3.8pt"
    
    tab = r'''\noindent
\renewcommand{\arraystretch}{1.1}
\setlength{\tabcolsep}{%s}
\begin{tabular}[t]{@{}crr}''' %(tabsep)

    n = 0
    while n < 3:
        da = date + n
        tab = tab + r'''
\multicolumn{1}{c}{\footnotesize{\textbf{%s}}} & \multicolumn{1}{c}{\footnotesize{\textbf{GHA}}} & \multicolumn{1}{c}{\footnotesize{\textbf{Dec}}}\\
\cmidrule{1-3}
''' %(ephem.date(da).datetime().strftime("%d"))
        h = 0

        if config.decf != '+':	# USNO format for Declination
            # first populate an array of 24 hours with all data
            hourlydata = [[] for i in range(24)]
            while h < 24:
                hourlydata[h] = sunmoon(da)
                da = da + ephem.hour
                h += 1
            # now print the data per hour
            da = date + n
            h = 0

            while h < 24:
                band = int(h/6)
                group = band % 2
                eph = hourlydata[h]
                if h > 0:
                    preveph = hourlydata[h-1]
                else:
                    preveph = hourlydata[0]		# hour -1 = hour 0
                if h < 23:
                    nexteph = hourlydata[h+1]
                else:
                    nexteph = hourlydata[23]	# hour 24 = hour 23

                # format declination checking for hemisphere change
                printNS, printDEG = declCompare(preveph[7],eph[7],nexteph[7],h)
                sdec = NSdecl(eph[1],h,printNS,printDEG,True)

                line = r'''\color{blue} {%s} & ''' %(h)
                line = line + "%s & %s" %(eph[0],sdec)
                if group == 1:
                    tab = tab + r'''\rowcolor{LightCyan}'''
                lineterminator = r'''\\
'''
                if h < 23 and (h+1)%6 == 0:
                    lineterminator = r'''\\[2Pt]
'''
                tab = tab + line + lineterminator
                h += 1
                da = da + ephem.hour

        else:			# Positive/Negative Declinations
            while h < 24:
                band = int(h/6)
                group = band % 2
                eph = sunmoon(da)
                line = r'''\color{blue} {%s} & ''' %(h)
                line = line + "%s & %s" %(eph[0],eph[1])
                if group == 1:
                    tab = tab + r'''\rowcolor{LightCyan}'''
                lineterminator = r'''\\
'''
                if h < 23 and (h+1)%6 == 0:
                    lineterminator = r'''\\[2Pt]
'''
                tab = tab + line + lineterminator
                h += 1
                da = da + ephem.hour

        vd = sun_moon_SD(date + n)
        tab = tab + r'''\cmidrule{2-3}
& \multicolumn{1}{c}{\footnotesize{SD.=%s}} & \multicolumn{1}{c}{\footnotesize{d=%s}}\\
\cmidrule{2-3}''' %(vd[1],vd[0])
        if n < 2:
            # add space between tables...
            tab = tab + r'''
\multicolumn{3}{c}{}\\[-1.5ex]'''
        n += 1
    tab = tab + r'''
\end{tabular}'''
    return tab


def declCompare(prev_rad, curr_rad, next_rad, hr):
    # for Declinations only...
    # decide if to print N/S; decide if to print degrees
    # note: the first three arguments are PyEphem angles in radians
    prNS = False
    prDEG = False
    psign = math.copysign(1.0,prev_rad)
    csign = math.copysign(1.0,curr_rad)
    nsign = math.copysign(1.0,next_rad)
    pdeg = abs(math.degrees(prev_rad))
    cdeg = abs(math.degrees(curr_rad))
    ndeg = abs(math.degrees(next_rad))
    pdegi = int(pdeg)
    cdegi = int(cdeg)
    ndegi = int(ndeg)
    pmin = round((pdeg-pdegi)*60, 1)	# minutes (float), rounded to 1 decimal place
    cmin = round((cdeg-cdegi)*60, 1)	# minutes (float), rounded to 1 decimal place
    nmin = round((ndeg-ndegi)*60, 1)	# minutes (float), rounded to 1 decimal place
    pmini = int(pmin)
    cmini = int(cmin)
    nmini = int(nmin)
    if pmini == 60:
        pmin -= 60
        pdegi += 1
    if cmini == 60:
        cmin -= 60
        cdegi += 1
    if nmini == 60:
        nmin -= 60
        ndegi += 1
    # now we have the values in degrees+minutes as printed

    if hr%6 == 0:
        prNS = True			# print N/S for hour = 0, 6, 12, 18
    else:
        if psign != csign:
            prNS = True		# print N/S if previous sign different
    if hr < 23:
        if csign != nsign:
            prNS = True		# print N/S if next sign different
    if prNS == False:
        if pdegi != cdegi:
            prDEG = True	# print degrees if changed since previous value
        if cdegi != ndegi:
            prDEG = True	# print degrees if next value is changed
    else:
        prDEG= True			# print degrees is N/S to be printed
    return prNS, prDEG


def NSdecl(deg, hr, printNS, printDEG, modernFMT):
    # reformat degrees latitude to Ndd°mm.m or Sdd°mm.m
    if deg[0:1] == '-':
        hemisph = 'S'
        deg = deg[1:]
    else:
        hemisph = 'N'
    if not(printDEG):
        deg = deg[3:]	# skip the degrees (always dd°mm.m)
        if (hr+3)%6 == 0:
            deg = r'''\raisebox{0.24ex}{\boldmath$\cdot$~\boldmath$\cdot$~~}''' + deg
    if modernFMT:
        if printNS or hr%6 == 0:
            sdeg = "\\textcolor{blue}{%s}" %hemisph + deg
        else:
            sdeg = deg
    else:
        if printNS or hr%6 == 0:
            sdeg = "\\textbf{%s}" %hemisph + deg
        else:
            sdeg = deg
    #print("sdeg: ", sdeg)
    return sdeg


def page(date):
    # creates a page(15 days) of the Sun almanac
    page = r'''
%% ------------------ N E W   P A G E ------------------
\newpage
\sffamily
\noindent
\begin{flushright}
\textbf{%s to %s}\par
\end{flushright}
\begin{scriptsize}
''' %(ephem.date(date).datetime().strftime("%Y %B %d"),ephem.date(date+14).datetime().strftime("%b. %d"))
    if config.tbls == "m":
        page = page + suntabm(date)
        page = page + r'''\quad
'''
        page = page + suntabm(date+3)
        page = page + r'''\quad
'''
        page = page + suntabm(date+6)
        page = page + r'''\quad
'''
        page = page + suntabm(date+9)
        page = page + r'''\quad
'''
        page = page + suntabm(date+12)
    else:
        page = page + suntab(date)
        page = page + suntab(date+3)
        page = page + suntab(date+6)
        page = page + suntab(date+9)
        page = page + suntab(date+12)
    page = page + r'''

\end{scriptsize}'''
    # to avoid "Overfull \hbox" messages, always leave a paragraph end before the end of a size change. (See line above)
    return page


def pages(date, p):
    # make 'p' pages beginning with date
    out = ''
    for i in range(p):
        out = out + page(date)
        date += 15
    return out


def almanac(first_day, pagenum):
    # make almanac from date till date
    year = first_day.year
    mth = first_day.month
    day = first_day.day

    alm = r'''\documentclass[10pt, twoside, a4paper]{report}
\usepackage[utf8]{inputenc}
\usepackage[english]{babel}
\usepackage{fontenc}'''

    if config.tbls == "m" and config.decf != '+':	# USNO format for Declination
        alm = alm + r'''
\usepackage[ top=8mm, bottom=18mm, left=13mm, right=8mm ]{geometry}'''

    if config.tbls == "m" and config.decf == '+':	# Positive/Negative Declinations
        alm = alm + r'''
\usepackage[ top=8mm, bottom=18mm, left=17mm, right=11mm ]{geometry}'''

    if config.tbls == "m":
        alm = alm + r'''
\usepackage[table]{xcolor}
\definecolor{LightCyan}{rgb}{0.88,1,1}
\usepackage{booktabs}'''
    else:
        alm = alm + r'''
\usepackage[ top=21mm, bottom=21mm, left=16mm, right=10mm]{geometry}'''
    
    alm = alm + r'''
\newcommand{\HRule}{\rule{\linewidth}{0.5mm}}
\usepackage[pdftex]{graphicx}
%\showboxbreadth=50  % use for logging
%\showboxdepth=50    % use for logging
\DeclareUnicodeCharacter{00B0}{\ensuremath{{}^\circ}}
\begin{document}
\begin{titlepage}'''

    if config.tbls == "m":
        alm = alm + r'''\vspace*{2cm}'''

    alm = alm + r'''
    \begin{center}
    \textsc{\Large Generated by PyAlmanac}\\[1.5cm]
    \includegraphics[width=0.4\textwidth]{./Ra}\\[1cm]
    \textsc{\huge The Nautical Almanac for the Sun}\\[0.7cm]'''

    if pagenum == 25:
        alm = alm + r'''
    \HRule \\[0.6cm]
    { \Huge \bfseries %s}\\[0.4cm]
    \HRule \\[1.5cm]''' %(year)
    else:
        alm = alm + r'''
    \HRule \\[0.6cm]
    { \Huge \bfseries from %s.%s.%s}\\[0.4cm]
    \HRule \\[1.5cm]''' %(day,mth,year)

    if config.tbls == "m":
        alm = alm + r'''
    \begin{center} \large
    \emph{Author:}\\
    Enno \textsc{Rodegerdts}\\[6Pt]
    \emph{Table Design:}\\
    Andrew \textsc{Bauer}'''
    else:
        alm = alm + r'''
    \begin{center} \large
    \emph{Author:}\\
    Enno \textsc{Rodegerdts}\\'''

    alm = alm + r'''
    \end{center}
    \vfill
    {\large \today}
    \HRule \\[0.6cm]
    \end{center}
    \begin{description}\footnotesize
    \item[Disclaimer:] These are computer generated tables. Use on your own risk. 
    The accuracy has been checked as good as possible but can not be guaranteed. 
    This means, if you get lost on the oceans because of errors in this publication I can not be held liable. 
    For security relevant applications you should buy an official version of the nautical almanac.
    \end{description}
\end{titlepage}
'''

    if config.tbls == "m":
        alm = alm + r'''\vspace*{3cm}'''
    else:
        alm = alm + r'''\vspace*{1.5cm}'''

    alm = alm + r'''
    \noindent
    DIP corrects for height of eye over the surface. This value has to be subtracted from the sextant altitude ($H_s$). The  correction in degrees for height of eye in meters is given by the following formula: 
    \[d=0.0293\sqrt{m}\]
    This is the first correction (apart from index error) that has to be applied to the measured altitude.\\[12pt]
    \noindent
    The next correction is for refraction in the Earth's atmosphere. As usual this table is correct for 10°C and a pressure of 1010 hPa. This correction has to be applied to apparent altitude ($H_a$). The exact values can be calculated by the following formula.
    \[R_0=\cot \left( H_a + \frac{7.31}{H_a+4.4}\right)\]
    For other than standard conditions, calculate a correction factor for $R_0$ by: \[f=\frac{0.28P}{T+273}\] where $P$ is the pressure in hectopascal and $T$ is the temperature in °C.\\[12pt]
    \noindent
    Semidiameter has to be added for lower limb sights and subtracted for upper limb sights. The value for semidiameter is tabulated in the daily pages.\\[12pt]
    \noindent
    To correct your sextant altitude $H_s$ do the following:
    Calculate $H_a$ by
     \[H_a= H_s+I-dip\] 
    where $I$ is the sextant's index error. Then calculate the observed altitude $H_o$ by
    \[H_o= H_a-R+P\pm SD\]
    where $R$ is refraction, $P$ is parallax and $SD$ is the semidiameter.\\[12pt]
    \noindent
    Sight reduction tables can be downloaded for the US governments internet pages. Search for HO-229 or HO-249.  These values can also be calculated with two, relatively simple, formulas:
    \[ \sin H_c= \sin L \sin d + \cos L \cos d \cos LHA\]
    and
    \[\cos A = \frac{\sin d - \sin L \sin H_c}{\cos L \cos H_c}\]
    where $A$ is the azimuth angle, $L$ is the latitude, $d$ is the declination and $LHA$ is the local hour angle. The azimuth ($Z_n$) is given by the following rule:
    \begin{itemize}
    \item if the $LHA$ is greater than 180°, $Z_n=A$
    \item if the $LHA$ is less than 180°, $Z_n = 360^\circ - A$
    \end{itemize}'''

    first_day = r'''%s/%s/%s''' %(year,mth,day)
    date = ephem.Date(first_day)    # date to float
    alm = alm + pages(date,pagenum)
    alm = alm + '''
\end{document}'''
    return alm