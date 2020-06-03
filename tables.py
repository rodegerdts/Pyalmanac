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

# NOTE: the new format statement requires a literal '{' to be entered as '{{',
#       and a literal '}' to be entered as '}}'. The old '%' format specifier
#       will be removed from Python at some later time. See:
# https://docs.python.org/3/whatsnew/3.0.html#pep-3101-a-new-approach-to-string-formatting

import config
from alma_ephem import *

def planetstab(date):
    # generates a LaTeX table for the navigational plantets (traditional style)
    tab = r'''\noindent
\begin{tabular*}{0.74\textwidth}[t]{@{\extracolsep{\fill}}|c|r|rr|rr|rr|rr|}
\multicolumn{1}{c}{\normalsize{}} & \multicolumn{1}{c}{\normalsize{Aries}} &  \multicolumn{2}{c}{\normalsize{Venus}}& \multicolumn{2}{c}{\normalsize{Mars}} & \multicolumn{2}{c}{\normalsize{Jupiter}} & \multicolumn{2}{c}{\normalsize{Saturn}}\\
'''
    # note: 74% table width above removes "Overfull \hbox (1.65279pt too wide)"
    n = 0
    while n < 3:
        da = date + n
        tab = tab + r'''\hline
\rule{{0pt}}{{2.4ex}}\textbf{{{}}} & \multicolumn{{1}}{{c|}}{{\textbf{{GHA}}}} & \multicolumn{{1}}{{c}}{{\textbf{{GHA}}}} & \multicolumn{{1}}{{c|}}{{\textbf{{Dec}}}} & \multicolumn{{1}}{{c}}{{\textbf{{GHA}}}} & \multicolumn{{1}}{{c|}}{{\textbf{{Dec}}}} & \multicolumn{{1}}{{c}}{{\textbf{{GHA}}}} & \multicolumn{{1}}{{c|}}{{\textbf{{Dec}}}} & \multicolumn{{1}}{{c}}{{\textbf{{GHA}}}} & \multicolumn{{1}}{{c|}}{{\textbf{{Dec}}}}\\
\hline\rule{{0pt}}{{2.6ex}}\noindent
'''.format(ephem.date(da).datetime().strftime("%a"))
        h = 0

        if config.decf != '+':	# USNO format for Declination
            # first populate an array of 24 hours with all data
            hourlydata = [[] for i in range(24)]
            while h < 24:
                hourlydata[h] = planetsGHA(da)
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
                printNS, printDEG = declCompare(preveph[9],eph[9],nexteph[9],h)
                vdec = NSdecl(eph[2],h,printNS,printDEG,False)

                printNS, printDEG = declCompare(preveph[10],eph[10],nexteph[10],h)
                mdec = NSdecl(eph[4],h,printNS,printDEG,False)

                printNS, printDEG = declCompare(preveph[11],eph[11],nexteph[11],h)
                jdec = NSdecl(eph[6],h,printNS,printDEG,False)

                printNS, printDEG = declCompare(preveph[12],eph[12],nexteph[12],h)
                sdec = NSdecl(eph[8],h,printNS,printDEG,False)

                line = r'''{} & {} & {} & {} & {} & {} & {} & {} & {} & {}'''.format(h,eph[0],eph[1],vdec,eph[3],mdec,eph[5],jdec,eph[7],sdec)
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
                eph = planetsGHA(da)
                line = r'''{} & {} & {} & {} & {} & {} & {} & {} & {} & {}'''.format(h,eph[0],eph[1],eph[2],eph[3],eph[4],eph[5],eph[6],eph[7],eph[8])
                lineterminator = r'''\\
'''
                if h < 23 and (h+1)%6 == 0:
                    lineterminator = r'''\\[2Pt]
'''
                tab = tab + line + lineterminator
                h += 1
                da = da + ephem.hour

        vd = vdm_planets(date + n)
        tab = tab + r'''\hline
\multicolumn{{2}}{{|c|}}{{\rule{{0pt}}{{2.4ex}}Mer.pass.:{}}} & \multicolumn{{2}}{{c|}}{{v{} d{} m{}}} & \multicolumn{{2}}{{c|}}{{v{} d{} m{}}} & \multicolumn{{2}}{{c|}}{{v{} d{} m{}}} & \multicolumn{{2}}{{c|}}{{v{} d{} m{}}}\\
\hline
\multicolumn{{10}}{{c}}{{}}\\
'''.format(ariestransit(date + n),vd[0],vd[1],vd[2],vd[3],vd[4],vd[5],vd[6],vd[7],vd[8],vd[9],vd[10],vd[11])
        n += 1

    tab = tab + r'''\end{tabular*}
'''
    return tab


def planetstabm(date):
    # generates a LaTeX table for the navigational plantets (modern style)
    tab = r'''\vspace{6Pt}\noindent
\renewcommand{\arraystretch}{1.1}
\setlength{\tabcolsep}{4pt}
\begin{tabular}[t]{crcrrcrrcrrcrr}
\multicolumn{1}{c}{\normalsize{h}} & 
\multicolumn{1}{c}{\normalsize{Aries}} & & 
\multicolumn{2}{c}{\normalsize{Venus}}& & 
\multicolumn{2}{c}{\normalsize{Mars}} & & 
\multicolumn{2}{c}{\normalsize{Jupiter}} & & 
\multicolumn{2}{c}{\normalsize{Saturn}}\\
\cmidrule{2-2} \cmidrule{4-5} \cmidrule{7-8} \cmidrule{10-11} \cmidrule{13-14}'''
    n = 0
    while n < 3:
        da = date + n
        tab = tab + r'''
\multicolumn{{1}}{{c}}{{\textbf{{{}}}}} & \multicolumn{{1}}{{c}}{{\textbf{{GHA}}}} && 
\multicolumn{{1}}{{c}}{{\textbf{{GHA}}}} & \multicolumn{{1}}{{c}}{{\textbf{{Dec}}}} &&  \multicolumn{{1}}{{c}}{{\textbf{{GHA}}}} & \multicolumn{{1}}{{c}}{{\textbf{{Dec}}}} &&  \multicolumn{{1}}{{c}}{{\textbf{{GHA}}}} & \multicolumn{{1}}{{c}}{{\textbf{{Dec}}}} &&  \multicolumn{{1}}{{c}}{{\textbf{{GHA}}}} & \multicolumn{{1}}{{c}}{{\textbf{{Dec}}}}\\
'''.format(ephem.date(da).datetime().strftime("%a"))
        h = 0

        if config.decf != '+':	# USNO format for Declination
            # first populate an array of 24 hours with all data
            hourlydata = [[] for i in range(24)]
            while h < 24:
                hourlydata[h] = planetsGHA(da)
                da = da+ephem.hour
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
                printNS, printDEG = declCompare(preveph[9],eph[9],nexteph[9],h)
                vdec = NSdecl(eph[2],h,printNS,printDEG,True)

                printNS, printDEG = declCompare(preveph[10],eph[10],nexteph[10],h)
                mdec = NSdecl(eph[4],h,printNS,printDEG,True)

                printNS, printDEG = declCompare(preveph[11],eph[11],nexteph[11],h)
                jdec = NSdecl(eph[6],h,printNS,printDEG,True)

                printNS, printDEG = declCompare(preveph[12],eph[12],nexteph[12],h)
                sdec = NSdecl(eph[8],h,printNS,printDEG,True)

                line = r'''\color{{blue}}{{{}}} & '''.format(h)
                line = line + r'''{} && {} & {} && {} & {} && {} & {} && {} & {} \\
'''.format(eph[0],eph[1],vdec,eph[3],mdec,eph[5],jdec,eph[7],sdec)
                if group == 1:
                    tab = tab + r'''\rowcolor{LightCyan}
'''
                tab = tab + line
                h += 1
                da = da + ephem.hour

        else:			# Positive/Negative Declinations
            while h < 24:
                band = int(h/6)
                group = band % 2
                eph = planetsGHA(da)
                line = r'''\color{{blue}}{{{}}} & '''.format(h)
                line = line + r'''{} && {} & {} && {} & {} && {} & {} && {} & {} \\
'''.format(eph[0],eph[1],eph[2],eph[3],eph[4],eph[5],eph[6],eph[7],eph[8])
                if group == 1:
                    tab = tab + r'''\rowcolor{LightCyan}
'''
                tab = tab + line
                h += 1
                da = da + ephem.hour

        vd = vdm_planets(date + n)
        tab = tab + r'''\cmidrule{{1-2}} \cmidrule{{4-5}} \cmidrule{{7-8}} \cmidrule{{10-11}} \cmidrule{{13-14}}
\multicolumn{{2}}{{c}}{{\footnotesize{{Mer.pass.:{}}}}} && 
\multicolumn{{2}}{{c}}{{\footnotesize{{v{} d{} m{}}}}} && 
\multicolumn{{2}}{{c}}{{\footnotesize{{v{} d{} m{}}}}} && 
\multicolumn{{2}}{{c}}{{\footnotesize{{v{} d{} m{}}}}} && 
\multicolumn{{2}}{{c}}{{\footnotesize{{v{} d{} m{}}}}}\\
\cmidrule{{1-2}} \cmidrule{{4-5}} \cmidrule{{7-8}} \cmidrule{{10-11}} \cmidrule{{13-14}}
'''.format(ariestransit(date + n),vd[0],vd[1],vd[2],vd[3],vd[4],vd[5],vd[6],vd[7],vd[8],vd[9],vd[10],vd[11])
        
        if n < 2:
            vsep = ""
            if config.pgsz == "Letter":
                vsep = "[-2.0ex]"
            # add space between tables...
            tab = tab + r'''\multicolumn{{10}}{{c}}{{}}\\{}'''.format(vsep)
        n += 1

    tab = tab+r'''\end{tabular}\quad
'''
    return tab


def starstab(date):
    # returns a table with ephemerieds for the navigational stars
    out = r'''\begin{tabular*}{0.25\textwidth}[t]{@{\extracolsep{\fill}}|rrr|}
\multicolumn{3}{c}{\normalsize{Stars}}\\
'''
    if config.tbls == "m":
        out = out + r'''\hline
& \multicolumn{1}{c}{\multirow{2}{*}{\textbf{SHA}}} 
& \multicolumn{1}{c|}{\multirow{2}{*}{\textbf{Dec}}}\\
& & \multicolumn{1}{c|}{} \\
'''
    else:
        out = out + r'''\hline
\rule{0pt}{2.4ex} & \multicolumn{1}{c}{\textbf{SHA}} & \multicolumn{1}{c|}{\textbf{Dec}}\\
\hline\rule{0pt}{2.6ex}\noindent
'''
    stars = stellar(date+1)
    for i in range(len(stars)):
        out = out + r'''{} & {} & {} \\
'''.format(stars[i][0],stars[i][1],stars[i][2])
    m = r'''\hline
'''

    # returns 3 tables with SHA & Mer.pass for Venus, Mars, Jupiter and Saturn
    for i in range(3):
        datestr = r'''{} {} {}'''.format(ephem.date(date+i).datetime().strftime("%b"), ephem.date(date+i).datetime().strftime("%d"), ephem.date(date+i).datetime().strftime("%a"))
        m = m + '''\hline
'''
        if config.tbls == "m":
            m = m + r'''& & \multicolumn{{1}}{{r|}}{{}}\\[-2.0ex]
\multicolumn{{1}}{{|r}}{{\textbf{{{}}}}} 
& \multicolumn{{1}}{{c}}{{\textbf{{SHA}}}} 
& \multicolumn{{1}}{{r|}}{{\textbf{{Mer.pass}}}}\\
'''.format(datestr)
        else:
            m = m + r'''& & \multicolumn{{1}}{{r|}}{{}}\\[-2.0ex]
\textbf{{{}}} & \textbf{{SHA}} & \textbf{{Mer.pass}}\\
'''.format(datestr)
        datex = ephem.date(date + i)
        p = planetstransit(datex)
        m = m + r'''Venus & {} & {} \\
'''.format(p[0],p[1])
        m = m + r'''Mars & {} & {} \\
'''.format(p[2],p[3])
        m = m + r'''Jupiter & {} & {} \\
'''.format(p[4],p[5])
        m = m + r'''Saturn & {} & {} \\
'''.format(p[6],p[7])
        m = m + r'''\hline
'''
    out = out + m

    # returns a table with Horizontal parallax for Venus and Mars
    hp = r'''\hline
'''
    hp = hp + r'''& & \multicolumn{1}{r|}{}\\[-2.5ex]
\multicolumn{2}{|r}{\rule{0pt}{2.6ex}\textbf{Horizontal parallax}} & \multicolumn{1}{c|}{}\\
'''
    hp = hp + r'''\multicolumn{{2}}{{|r}}{{Venus:}} & \multicolumn{{1}}{{c|}}{{{}}} \\
'''.format(p[9])
    hp = hp + r'''\multicolumn{{2}}{{|r}}{{Mars:}} & \multicolumn{{1}}{{c|}}{{{}}} \\
'''.format(p[8])
    hp = hp + r'''\hline
'''
    out = out + hp
    
    out = out + r'''\end{tabular*}'''
    return out


def sunmoontab(date):
    # generates LaTeX table for sun and moon (traditional style)
    tab = r'''\noindent
\begin{tabular*}{0.54\textwidth}[t]{@{\extracolsep{\fill}}|c|rr|rrrrr|}
\multicolumn{1}{c}{\normalsize{h}}& \multicolumn{2}{c}{\normalsize{Sun}} & \multicolumn{5}{c}{\normalsize{Moon}}\\
'''
    # note: 54% table width above removes "Overfull \hbox (1.65279pt too wide)"
    #                 and "Underfull \hbox (badness 10000)"
    n = 0
    while n < 3:
        da = date + n
        tab = tab + r'''\hline
\multicolumn{{1}}{{|c|}}{{\rule{{0pt}}{{2.6ex}}\textbf{{{}}}}} &\multicolumn{{1}}{{c}}{{\textbf{{GHA}}}} & \multicolumn{{1}}{{c|}}{{\textbf{{Dec}}}}  & \multicolumn{{1}}{{c}}{{\textbf{{GHA}}}} & \multicolumn{{1}}{{c}}{{\textbf{{\(\nu\)}}}} & \multicolumn{{1}}{{c}}{{\textbf{{Dec}}}} & \multicolumn{{1}}{{c}}{{\textbf{{d}}}} & \multicolumn{{1}}{{c|}}{{\textbf{{HP}}}}\\
\hline\rule{{0pt}}{{2.6ex}}\noindent
'''.format(ephem.date(da).datetime().strftime("%a"))
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
            mlastNS = ''
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

                mdec, mNS = NSdeg(eph[4],False,h)
                if mNS != mlastNS or math.copysign(1.0,eph[8]) != math.copysign(1.0,nexteph[8]):
                    mdec, mNS = NSdeg(eph[4],False,h,True)	# force N/S
                mlastNS = mNS

                line = r'''{} & {} & {} & {} & {} & {} & {} & {}'''.format(h,eph[0],sdec,eph[2],eph[3],mdec,eph[5],eph[6])
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
                line = r'''{} & {} & {} & {} & {} & {} & {} & {}'''.format(h,eph[0],eph[1],eph[2],eph[3],eph[4],eph[5],eph[6])
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
\rule{{0pt}}{{2.4ex}} & \multicolumn{{1}}{{c}}{{SD.={}}} & \multicolumn{{1}}{{c|}}{{d={}}} & \multicolumn{{5}}{{c|}}{{S.D.={}}}\\
\hline
'''.format(vd[1],vd[0],vd[2])
        if n < 2:
            # add space between tables...
            tab = tab + r'''\multicolumn{7}{c}{}\\[-1.5ex]'''
        n += 1
    tab = tab + r'''\end{tabular*}'''
    return tab


def sunmoontabm(date):
    # generates LaTeX table for sun and moon (modern style)
    tab = r'''\noindent
\renewcommand{\arraystretch}{1.1}
\setlength{\tabcolsep}{4pt}
\quad\quad
\begin{tabular}[t]{crrcrrrrr}
\multicolumn{1}{c}{\normalsize{h}} & 
\multicolumn{2}{c}{\normalsize{Sun}} & &
\multicolumn{5}{c}{\normalsize{Moon}}\\
\cmidrule{2-3} \cmidrule{5-9}'''
    # note: \quad\quad above shifts all tables to the right (still within margins)
    n = 0
    while n < 3:
        da = date + n
        tab = tab + r'''
\multicolumn{{1}}{{c}}{{\textbf{{{}}}}} & \multicolumn{{1}}{{c}}{{\textbf{{GHA}}}} & \multicolumn{{1}}{{c}}{{\textbf{{Dec}}}} & & \multicolumn{{1}}{{c}}{{\textbf{{GHA}}}} & \multicolumn{{1}}{{c}}{{\textbf{{\(\nu\)}}}} & \multicolumn{{1}}{{c}}{{\textbf{{Dec}}}} & \multicolumn{{1}}{{c}}{{\textbf{{d}}}} & \multicolumn{{1}}{{c}}{{\textbf{{HP}}}}\\
'''.format(ephem.date(da).datetime().strftime("%a"))
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
            mlastNS = ''
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
                band = int(h/6)
                group = band % 2

                # format declination checking for hemisphere change
                printNS, printDEG = declCompare(preveph[7],eph[7],nexteph[7],h)
                sdec = NSdecl(eph[1],h,printNS,printDEG,True)

                mdec, mNS = NSdeg(eph[4],True,h)
                if mNS != mlastNS or math.copysign(1.0,eph[8]) != math.copysign(1.0,nexteph[8]):
                    mdec, mNS = NSdeg(eph[4],True,h,True)	# force NS
                mlastNS = mNS

                line = r'''\color{{blue}}{{{}}} & '''.format(h)
                line = line + r'''{} & {} && {} & {} & {} & {} & {} \\
'''.format(eph[0],sdec,eph[2],eph[3],mdec,eph[5],eph[6])

                if group == 1:
                    tab = tab + r'''\rowcolor{LightCyan}
'''
                tab = tab + line
                h += 1
                da = da + ephem.hour

        else:			# Positive/Negative Declinations
            while h < 24:
                eph = sunmoon(da)
                band = int(h/6)
                group = band % 2
                line = r'''\color{{blue}}{{{}}} & '''.format(h)
                line = line + r'''{} & {} && {} & {} & {} & {} & {} \\
'''.format(eph[0],eph[1],eph[2],eph[3],eph[4],eph[5],eph[6])
                if group == 1:
                    tab = tab + r'''\rowcolor{LightCyan}
'''
                tab = tab + line
                h += 1
                da = da + ephem.hour

        vd = sun_moon_SD(date + n)
        tab = tab + r'''\cmidrule{{2-3}} \cmidrule{{5-9}}
\multicolumn{{1}}{{c}}{{}} & \multicolumn{{1}}{{c}}{{\footnotesize{{SD.={}}}}} & 
\multicolumn{{1}}{{c}}{{\footnotesize{{d={}}}}} && \multicolumn{{5}}{{c}}{{\footnotesize{{S.D.={}}}}}\\
\cmidrule{{2-3}} \cmidrule{{5-9}}
'''.format(vd[1],vd[0],vd[2])
        if n < 2:
            vsep = "[-1.5ex]"
            if config.pgsz == "Letter":
                vsep = "[-2.0ex]"
            # add space between tables...
            tab = tab + r'''\multicolumn{{7}}{{c}}{{}}\\{}'''.format(vsep)
        n += 1
    tab = tab + r'''\end{tabular}
\quad\quad'''
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
        deg = deg[10:]	# skip the degrees (always dd°mm.m) - note: the degree symbol '$^\circ$' is eight bytes long
        if (hr+3)%6 == 0:
            deg = r'''\raisebox{0.24ex}{\boldmath$\cdot$~\boldmath$\cdot$~~}''' + deg
    if modernFMT:
        if printNS or hr%6 == 0:
            sdeg = r'''\textcolor{{blue}}{{{}}}'''.format(hemisph) + deg
        else:
            sdeg = deg
    else:
        if printNS or hr%6 == 0:
            sdeg = r'''\textbf{{{}}}'''.format(hemisph) + deg
        else:
            sdeg = deg
    #print("sdeg: ", sdeg)
    return sdeg


def NSdeg(deg, modern=False, hr=0, forceNS=False):
    # reformat degrees latitude to Ndd°mm.m or Sdd°mm.m
    if deg[0:1] == '-':
        hemisph = 'S'
        deg = deg[1:]
    else:
        hemisph = 'N'
    if modern:
        if forceNS or hr%6 == 0:
            sdeg = r'''\textcolor{{blue}}{{{}}}'''.format(hemisph) + deg
        else:
            sdeg = deg
    else:
        if forceNS or hr%6 == 0:
            sdeg = r'''\textbf{{{}}}'''.format(hemisph) + deg
        else:
            sdeg = deg
    return sdeg, hemisph


def twilighttab(date):
    # returns the twilight and moonrise tables, finally EoT data

# Twilight tables ...........................................
    #lat = [72,70,68,66,64,62,60,58,56,54,52,50,45,40,35,30,20,10,0, -10,-20,-30,-35,-40,-45,-50,-52,-54,-56,-58,-60]
    latNS = [72, 70, 58, 40, 10, -10, -50, -60]
    tab = r'''
\begin{tabular*}{0.45\textwidth}[t]{@{\extracolsep{\fill}}|r|ccc|ccc|}
\multicolumn{7}{c}{\normalsize{}}\\
'''

    if config.tbls == "m":
    # The header begins with a thin empty row as top padding; and the top row with
    # bold text has some padding below it. This result gives a balanced impression.
        tab = tab + r'''\hline
\multicolumn{1}{|c|}{} & & & \multicolumn{1}{|c|}{} & \multicolumn{1}{c|}{} & & \multicolumn{1}{c|}{}\\[-2.0ex]
\multicolumn{1}{|c|}{\multirow{2}{*}{\textbf{Lat.}}} & 
\multicolumn{2}{c}{\footnotesize{\textbf{Twilight}}} & 
\multicolumn{1}{|c|}{\multirow{2}{*}{\textbf{Sunrise}}} & 
\multicolumn{1}{c|}{\multirow{2}{*}{\textbf{Sunset}}} & 
\multicolumn{2}{c|}{\footnotesize{\textbf{Twilight}}}\\[0.6ex]
\multicolumn{1}{|c|}{} & 
\multicolumn{1}{c}{Naut.} & 
\multicolumn{1}{c}{Civil} & 
\multicolumn{1}{|c|}{} & 
\multicolumn{1}{c|}{} & 
\multicolumn{1}{c}{Civil} & 
\multicolumn{1}{c|}{Naut.}\\
\hline\rule{0pt}{2.6ex}\noindent
'''
    else:
        tab = tab + r'''\hline
\multicolumn{1}{|c|}{\rule{0pt}{2.4ex}\multirow{2}{*}{\textbf{Lat.}}} & 
\multicolumn{2}{c}{\textbf{Twilight}} & 
\multicolumn{1}{|c|}{\multirow{2}{*}{\textbf{Sunrise}}} & 
\multicolumn{1}{c|}{\multirow{2}{*}{\textbf{Sunset}}} & 
\multicolumn{2}{c|}{\textbf{Twilight}}\\
\multicolumn{1}{|c|}{} & 
\multicolumn{1}{c}{Naut.} & 
\multicolumn{1}{c}{Civil} & 
\multicolumn{1}{|c|}{} & 
\multicolumn{1}{c|}{} & 
\multicolumn{1}{c}{Civil} & 
\multicolumn{1}{c|}{Naut.}\\
\hline\rule{0pt}{2.6ex}\noindent
'''
    lasthemisph = ""
    j = 5
    for i in config.lat:
        if i >= 0:
            hemisph = 'N'
        else:
            hemisph = 'S'
        if not(i in latNS):
            hs = ""
        else:
            hs = hemisph
            if j%6 == 0:
                tab = tab + r'''\rule{0pt}{2.6ex}
'''
        lasthemisph = hemisph
        # day+1 to calculate for the second day (three days are printed on one page)
        twi = twilight(date+1, i, hemisph)
        line = r'''\textbf{{{}}}'''.format(hs) + " " + r'''{}$^\circ$'''.format(abs(i))
        line = line + r''' & {} & {} & {} & {} & {} & {} \\
'''.format(twi[0],twi[1],twi[2],twi[4],twi[5],twi[6])
        tab = tab + line
        j += 1
    # add space between tables...
    tab = tab + r'''\hline\multicolumn{7}{c}{}\\[-1.5ex]
'''

# Moonrise & Moonset ...........................................
    if config.tbls == "m":
        tab = tab + r'''\hline
\multicolumn{1}{|c|}{} & & & \multicolumn{1}{c|}{} & & & \multicolumn{1}{c|}{}\\[-2.0ex]
\multicolumn{1}{|c|}{\multirow{2}{*}{\textbf{Lat.}}} & 
\multicolumn{3}{c|}{\footnotesize{\textbf{Moonrise}}} & 
\multicolumn{3}{c|}{\footnotesize{\textbf{Moonset}}}\\[0.6ex]
'''
    else:
        tab = tab + r'''\hline
\multicolumn{1}{|c|}{\rule{0pt}{2.4ex}\multirow{2}{*}{\textbf{Lat.}}} & 
\multicolumn{3}{c|}{\textbf{Moonrise}} & 
\multicolumn{3}{c|}{\textbf{Moonset}}\\
'''

    weekday = [ephem.date(date).datetime().strftime("%a"),ephem.date(date+1).datetime().strftime("%a"),ephem.date(date+2).datetime().strftime("%a")]
    tab = tab + r'''\multicolumn{{1}}{{|c|}}{{}} & 
\multicolumn{{1}}{{c}}{{{}}} & 
\multicolumn{{1}}{{c}}{{{}}} & 
\multicolumn{{1}}{{c|}}{{{}}} & 
\multicolumn{{1}}{{c}}{{{}}} & 
\multicolumn{{1}}{{c}}{{{}}} & 
\multicolumn{{1}}{{c|}}{{{}}} \\
\hline\rule{{0pt}}{{2.6ex}}\noindent
'''.format(weekday[0],weekday[1],weekday[2],weekday[0],weekday[1],weekday[2])

    moon = [0,0,0,0,0,0]
    moon2 = [0,0,0,0,0,0]
    lasthemisph = ""
    j = 5
    for i in config.lat:
        if i >= 0:
            hemisph = 'N'
        else:
            hemisph = 'S'
        if not(i in latNS):
            hs = ""
        else:
            hs = hemisph
            if j%6 == 0:
                tab = tab + r'''\rule{0pt}{2.6ex}
'''
        lasthemisph = hemisph
        moon, moon2 = moonrise_set(date,i)
        if not(double_events_found(moon,moon2)):
            tab = tab + r'''\textbf{{{}}}'''.format(hs) + " " + r'''{}$^\circ$'''.format(abs(i))
            tab = tab + r''' & {} & {} & {} & {} & {} & {} \\
'''.format(moon[0],moon[1],moon[2],moon[3],moon[4],moon[5])
        else:
# print a row with two moonrise/moonset events on the same day & latitude
            tab = tab + r'''\multirow{{2}}{{*}}{{\textbf{{{}}} {}$^\circ$}}'''.format(hs,abs(i))
# top row...
            for k in range(len(moon)):
                if moon2[k] != '--:--':
                    tab = tab + r''' & {}'''.format(moon[k])
                else:
                    tab = tab + r''' & \multirow{{2}}{{*}}{{{}}}'''.format(moon[k])
            tab = tab + r'''\\'''	# terminate top row
# bottom row...
            for k in range(len(moon)):
                if moon2[k] != '--:--':
                    tab = tab + r''' & {}'''.format(moon2[k])
                else:
                    tab = tab + r'''&'''
            tab = tab + r'''\\'''	# terminate bottom row
        j += 1
    # add space between tables...
    tab = tab + r'''\hline\multicolumn{7}{c}{}\\[-1.5ex]
'''

# Equation of Time section ...........................................
    if config.tbls == "m":
        tab = tab + r'''\hline
\multicolumn{1}{|c|}{} & & & \multicolumn{1}{c|}{} & & & \multicolumn{1}{c|}{}\\[-2.0ex]
\multicolumn{1}{|c|}{\multirow{4}{*}{\footnotesize{\textbf{Day}}}} & 
\multicolumn{3}{c|}{\footnotesize{\textbf{Sun}}} & 
\multicolumn{3}{c|}{\footnotesize{\textbf{Moon}}}\\[0.6ex]
\multicolumn{1}{|c|}{} & 
\multicolumn{2}{c}{Eqn.of Time} & 
\multicolumn{1}{|c|}{Mer.} & 
\multicolumn{2}{c}{Mer.Pass.} & 
\multicolumn{1}{|c|}{}\\
\multicolumn{1}{|c|}{} &\multicolumn{1}{c}{00\textsuperscript{h}} & \multicolumn{1}{c}{12\textsuperscript{h}} & \multicolumn{1}{|c|}{Pass} & \multicolumn{1}{c}{Upper} & \multicolumn{1}{c}{Lower} &\multicolumn{1}{|c|}{Age}\\
\multicolumn{1}{|c|}{} &\multicolumn{1}{c}{mm:ss} & \multicolumn{1}{c}{mm:ss} & \multicolumn{1}{|c|}{hh:mm} & \multicolumn{1}{c}{hh:mm} & \multicolumn{1}{c}{hh:mm} &\multicolumn{1}{|c|}{}\\
\hline\rule{0pt}{3.0ex}\noindent
'''
    else:
        tab = tab + r'''\hline
\multicolumn{1}{|c|}{\rule{0pt}{2.4ex}\multirow{4}{*}{\textbf{Day}}} & 
\multicolumn{3}{c|}{\textbf{Sun}} & \multicolumn{3}{c|}{\textbf{Moon}}\\
\multicolumn{1}{|c|}{} & \multicolumn{2}{c}{Eqn.of Time} & \multicolumn{1}{|c|}{Mer.} & \multicolumn{2}{c}{Mer.Pass.} & \multicolumn{1}{|c|}{}\\
\multicolumn{1}{|c|}{} & \multicolumn{1}{c}{00\textsuperscript{h}} & \multicolumn{1}{c}{12\textsuperscript{h}} & \multicolumn{1}{|c|}{Pass} & \multicolumn{1}{c}{Upper} & \multicolumn{1}{c}{Lower} &\multicolumn{1}{|c|}{Age}\\
\multicolumn{1}{|c|}{} & \multicolumn{1}{c}{mm:ss} & \multicolumn{1}{c}{mm:ss} & \multicolumn{1}{|c|}{hh:mm} & \multicolumn{1}{c}{hh:mm} & \multicolumn{1}{c}{hh:mm} &\multicolumn{1}{|c|}{}\\
\hline\rule{0pt}{3.0ex}\noindent
'''

    for k in range(3):
        d = ephem.date(date+k)
        eq = equation_of_time(d)
        if k == 2:
            tab = tab + r'''{} & {} & {} & {} & {} & {} & {}({}\%) \\[0.3ex]
'''.format(d.datetime().strftime("%d"),eq[0],eq[1],eq[2],eq[3],eq[4],eq[5],eq[6])
        else:
            tab = tab + r'''{} & {} & {} & {} & {} & {} & {}({}\%) \\
'''.format(d.datetime().strftime("%d"),eq[0],eq[1],eq[2],eq[3],eq[4],eq[5],eq[6])
    tab = tab + r'''\hline
\end{tabular*}'''
    return tab


def double_events_found(m1, m2):
    # check for two moonrise/moonset events on the same day & latitude
    dbl = False
    for i in range(len(m1)):
        if m2[i] != '--:--':
            dbl = True
    return dbl


def doublepage(date, page1):
    # creates a doublepage (3 days) of the nautical almanac
    page = ''
    if not(page1):
        page = r'''
% ------------------ N E W   P A G E ------------------
\newpage'''

    leftindent = ""
    rightindent = ""
    if config.tbls == "m":
        leftindent = "\quad"
        rightindent = "\hphantom{\quad}"

    page = page + r'''
\sffamily
\noindent
{}\textbf{{{}, {}, {}   ({}.,  {}.,  {}.)}}'''.format(leftindent,ephem.date(date).datetime().strftime("%B %d"),ephem.date(date+1).datetime().strftime("%d"),ephem.date(date+2).datetime().strftime("%d"),ephem.date(date).datetime().strftime("%a"),ephem.date(date+1).datetime().strftime("%a"),ephem.date(date+2).datetime().strftime("%a"))

    if config.tbls == "m":
        page = page + r'\par'
    else:
        page = page + r'\\[1.0ex]'

    page = page + r'''
\begin{scriptsize}
'''

    if config.tbls == "m":
        page = page + planetstabm(date)
    else:
        page = page + planetstab(date)
    page = page + starstab(date)
    str1 = r'''

\end{{scriptsize}}
% ------------------ N E W   P A G E ------------------
\newpage
\begin{{flushright}}
\textbf{{{} to {}}}{}%
\end{{flushright}}\par
\begin{{scriptsize}}
'''.format(ephem.date(date).datetime().strftime("%Y %B %d"),ephem.date(date+2).datetime().strftime("%b. %d"),rightindent)
    page = page + str1
    if config.tbls == "m":
        page = page + sunmoontabm(date)
    else:
        page = page + sunmoontab(date)
    page = page + twilighttab(date)
    page = page + r'''

\end{scriptsize}'''
    # to avoid "Overfull \hbox" messages, always leave a paragraph end before the end of a size change. (See lines above)
    return page


def pages(date, p):
    # make 'p' doublepages beginning with date
    out = ''
    page1 = True
    for i in range(p):
        out = out + doublepage(date,page1)
        page1 = False
        date += 3
    return out


def almanac(first_day, pagenum):
    # make almanac from date till date
    year = first_day.year
    mth = first_day.month
    day = first_day.day

    # page size specific parameters
    if config.pgsz == "A4":
        paper = "a4paper"
        vsep1 = "2.0cm"
        vsep2 = "1.5cm"
        tm1 = "21mm"    # title page...
        bm1 = "15mm"
        lm1 = "10mm"
        rm1 = "10mm"
        tm = "21mm"     # data pages...
        bm = "18mm"
        lm = "12mm"
        rm = "8mm"
        if config.tbls == "m":
            tm = "10mm"
            bm = "15mm"
            lm = "10mm"
            rm = "10mm"
    else:
        paper = "letterpaper"
        vsep1 = "1.5cm"
        vsep2 = "1.0cm"
        tm1 = "12mm"    # title page...
        bm1 = "15mm"
        lm1 = "12mm"
        rm1 = "12mm"
        tm = "12.2mm"   # data pages...
        bm = "13mm"
        lm = "15mm"
        rm = "11mm"
        if config.tbls == "m":
            tm = "4mm"
            bm = "10mm"
            lm = "13mm"
            rm = "13mm"

    alm = r'''\documentclass[10pt, twoside, {}]{{report}}
'''.format(paper)

    alm = alm + r'''
%\usepackage[utf8]{inputenc}
\usepackage[english]{babel}
\usepackage{fontenc}'''

    # to troubleshoot add "showframe, verbose," below:
    alm = alm + r'''
\usepackage[nomarginpar, top={}, bottom={}, left={}, right={}]{{geometry}}'''.format(tm,bm,lm,rm)

    if config.tbls == "m":
        alm = alm + r'''
\usepackage[table]{xcolor}
\definecolor{LightCyan}{rgb}{0.88,1,1}
\usepackage{booktabs}'''

    # Note: \DeclareUnicodeCharacter is not compatible with some versions of pdflatex
    alm = alm + r'''
\usepackage{multirow}
\newcommand{\HRule}{\rule{\linewidth}{0.5mm}}
\setlength{\footskip}{15pt}
\usepackage[pdftex]{graphicx}	% for \includegraphics
\usepackage{tikz}				% for \draw  (load after 'graphicx')
%\showboxbreadth=50  % use for logging
%\showboxdepth=50    % use for logging
%\DeclareUnicodeCharacter{00B0}{\ensuremath{{}^\circ}}
\setlength\fboxsep{1.5pt}       % ONLY used by \colorbox in alma_ephem.py
\begin{document}'''

    alm = alm + r'''
% for the title page only...
\newgeometry{{nomarginpar, top={}, bottom={}, left={}, right={}}}'''.format(tm1,bm1,lm1,rm1)

    alm = alm + r'''
    \begin{titlepage}
    \begin{center}
    \textsc{\Large Generated by PyAlmanac}\\[0.7cm]
    % TRIM values: left bottom right top
    \includegraphics[clip, trim=5mm 8cm 5mm 21mm, width=0.8\textwidth]{./A4chartNorth_P.pdf}\\'''

    alm = alm + r'''[{}]
    \textsc{{\huge The Nautical Almanac}}\\[{}]'''.format(vsep1,vsep2)

    if pagenum == 122:
        alm = alm + r'''
    \HRule \\[0.5cm]
    {{ \Huge \bfseries {}}}\\[0.2cm]
    \HRule \\'''.format(year)
    else:
        alm = alm + r'''
    \HRule \\[0.5cm]
    {{ \Huge \bfseries from {}.{}.{}}}\\[0.2cm]
    \HRule \\'''.format(day,mth,year)

    if config.tbls == "m":
        alm = alm + r'''
    \begin{center}\begin{tabular}[t]{rl}
    \large\emph{Author:} & \large Andrew \textsc{Bauer}\\
    \large\emph{Original concept from:} & \large Enno \textsc{Rodegerdts}\\
    \end{tabular}\end{center}'''
    else:
        alm = alm + r'''
    \begin{center}\begin{tabular}[t]{rl}
    \large\emph{Original author:} & \large Enno \textsc{Rodegerdts}\\
    \large\emph{Enhancements:} & \large Andrew \textsc{Bauer}\\
    \end{tabular}\end{center}'''

    alm = alm + r'''
    {\large \today}
    \HRule \\[0.2cm]
    \end{center}
    \begin{description}\footnotesize
    \item[Disclaimer:] These are computer generated tables. Use on your own risk. 
    The accuracy has been checked as good as possible but can not be guaranteed. 
    This means, if you get lost on the oceans because of errors in this publication I can not be held liable. 
    For security relevant applications you should buy an official version of the nautical almanac. You need one anyway since this publication only contains the daily pages of the Nautical Almanac.
    \end{description}
\end{titlepage}
\restoregeometry    % so it does not affect the rest of the pages'''

    first_day = r'''{}/{}/{}'''.format(year,mth,day)
    date = ephem.Date(first_day)    # date to float
    alm = alm + pages(date,pagenum)
    alm = alm + '''
\end{document}'''
    return alm