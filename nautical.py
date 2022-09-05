#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright (C) 2014  Enno Rodegerdts
#   Copyright (C) 2022  Andrew Bauer

#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# NOTE: the new format statement requires a literal '{' to be entered as '{{',
#       and a literal '}' to be entered as '}}'. The old '%' format specifier
#       will be removed from Python at some later time. See:
# https://docs.python.org/3/whatsnew/3.0.html#pep-3101-a-new-approach-to-string-formatting

# NOTE: As mentioned by Klaus Höppner in "Typesetting tables with LaTeX", 'tabular*'
#       style tables often (surprisingly) expand the space between columns.
#       Switiching to 'tabular' style has the effect that the first column 
#       varies in width, e.g. as "Wed" is wider than "Fri". 
#       Also column 'v' in the Moon table, e.g. e.g. 6.9' versus 15.3'.
#       Also column 'd' in the Moon table, e.g. e.g. -8.2' versus -13.9'.
#       'Tabular' table style normally permits column width specification only for 
#       (left-justified) paragraph column content (with the 'p' column specifier).
#       A workaround is to use 'tabularx' table style and set the custom width
#       to the maximum column width on variable column-width columns. However -
#       \multicolumn entries must not cross any X-column, so it's out of question.
#       A solution to extending the column specifiers on a 'tabular' table style
#       with left-, center- and right-justified data plus a column width specifier
#       is possible: https://de.wikibooks.org/wiki/LaTeX-W%C3%B6rterbuch:_tabular
#       This works, but again increases the overall table width unnecessarily.
#       Conclusion/Resolution:
#       The following code now uses the 'tabular' table style without any
#       column width specifiers - thus table widths vary slightly from page to page.

###### Standard library imports ######
from datetime import datetime, timedelta
from math import copysign, degrees

###### Third party imports ######
import ephem

###### Local application imports ######
from alma_ephem import *
import config

#----------------------
#   internal methods
#----------------------

def fmtdate(d):
    if config.pgsz == 'Letter': return d.strftime("%m/%d/%Y")
    return d.strftime("%d.%m.%Y")

def fmtdates(d1,d2):
    if config.pgsz == 'Letter': return d1.strftime("%m/%d/%Y") + " - " + d2.strftime("%m/%d/%Y")
    return d1.strftime("%d.%m.%Y") + " - " + d2.strftime("%d.%m.%Y")

def declCompare(prev_rad, curr_rad, next_rad, hr):
    # for Declinations only...
    # decide if to print N/S; decide if to print degrees
    # note: the first three arguments are PyEphem angles in radians
    prNS = False
    prDEG = False
    psign = copysign(1.0,prev_rad)
    csign = copysign(1.0,curr_rad)
    nsign = copysign(1.0,next_rad)
    pdeg = abs(degrees(prev_rad))
    cdeg = abs(degrees(curr_rad))
    ndeg = abs(degrees(next_rad))
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

def double_events_found(m1, m2):
    # check for two moonrise/moonset events on the same day & latitude
    dbl = False
    for i in range(len(m1)):
        if m2[i] != '--:--':
            dbl = True
    return dbl

# >>>>>>>>>>>>>>>>>>>>>>>>
def planetstab(dfloat):
    # generates a LaTeX table for the navigational plantets (traditional style)
    # OLD: \begin{tabular*}{0.74\textwidth}[t]{@{\extracolsep{\fill}}|c|r|rr|rr|rr|rr|}
    # OLD: \begin{tabular}[t]{|C{15pt}|r|rr|rr|rr|rr|}

    tab = r'''\noindent
\setlength{\tabcolsep}{5.8pt}  % default 6pt
\begin{tabular}[t]{|c|r|rr|rr|rr|rr|}
\multicolumn{1}{c}{\normalsize{}} & \multicolumn{1}{c}{\normalsize{Aries}} &  \multicolumn{2}{c}{\normalsize{Venus}}& \multicolumn{2}{c}{\normalsize{Mars}} & \multicolumn{2}{c}{\normalsize{Jupiter}} & \multicolumn{2}{c}{\normalsize{Saturn}}\\
'''
    # note: 74% table width above removes "Overfull \hbox (1.65279pt too wide)"
    n = 0
    while n < 3:
        da = dfloat + n
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
            da = dfloat + n
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

        vd = vdm_planets(dfloat + n)
        tab = tab + r'''\hline
\multicolumn{{2}}{{|c|}}{{\rule{{0pt}}{{2.4ex}}Mer.pass. {}}} & 
\multicolumn{{2}}{{c|}}{{\(\nu\) {}$'$ \emph{{d}} {}$'$ m {}\hphantom{{0}}}} & 
\multicolumn{{2}}{{c|}}{{\(\nu\) {}$'$ \emph{{d}} {}$'$ m {}\hphantom{{0}}}} & 
\multicolumn{{2}}{{c|}}{{\(\nu\) {}$'$ \emph{{d}} {}$'$ m {}\hphantom{{0}}}} & 
\multicolumn{{2}}{{c|}}{{\(\nu\) {}$'$ \emph{{d}} {}$'$ m {}\hphantom{{0}}}}\\
\hline
\multicolumn{{10}}{{c}}{{}}\\
'''.format(ariestransit(dfloat + n),vd[0],vd[1],vd[2],vd[3],vd[4],vd[5],vd[6],vd[7],vd[8],vd[9],vd[10],vd[11])
        # the phantom character '0' compensates the format with two decimal places in SFalmanac
        n += 1

    tab = tab + r'''\end{tabular}
'''
    return tab

# >>>>>>>>>>>>>>>>>>>>>>>>
def planetstabm(dfloat):
    # generates a LaTeX table for the navigational plantets (modern style)

    tab = r'''\vspace{6Pt}\noindent
\renewcommand{\arraystretch}{1.1}
\setlength{\tabcolsep}{4pt}  % default 6pt
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
        da = dfloat + n
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
            da = dfloat + n
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

        vd = vdm_planets(dfloat + n)
        tab = tab + r'''\cmidrule{{1-2}} \cmidrule{{4-5}} \cmidrule{{7-8}} \cmidrule{{10-11}} \cmidrule{{13-14}}
\multicolumn{{2}}{{c}}{{\footnotesize{{Mer.pass. {}}}}} && 
\multicolumn{{2}}{{c}}{{\footnotesize{{\(\nu\){}$'$ \emph{{d}}{}$'$ m{}\hphantom{{0}}}}}} && 
\multicolumn{{2}}{{c}}{{\footnotesize{{\(\nu\){}$'$ \emph{{d}}{}$'$ m{}\hphantom{{0}}}}}} && 
\multicolumn{{2}}{{c}}{{\footnotesize{{\(\nu\){}$'$ \emph{{d}}{}$'$ m{}\hphantom{{0}}}}}} && 
\multicolumn{{2}}{{c}}{{\footnotesize{{\(\nu\){}$'$ \emph{{d}}{}$'$ m{}\hphantom{{0}}}}}}\\
\cmidrule{{1-2}} \cmidrule{{4-5}} \cmidrule{{7-8}} \cmidrule{{10-11}} \cmidrule{{13-14}}
'''.format(ariestransit(dfloat + n),vd[0],vd[1],vd[2],vd[3],vd[4],vd[5],vd[6],vd[7],vd[8],vd[9],vd[10],vd[11])
        # the phantom character '0' compensates the format with two decimal places in SFalmanac
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

# >>>>>>>>>>>>>>>>>>>>>>>>
def starstab(dfloat):
    # returns a table with ephemerides for the navigational stars
    # OLD: \begin{tabular*}{0.25\textwidth}[t]{@{\extracolsep{\fill}}|rrr|}

    if config.tbls == "m":
        out = r'''\renewcommand{\arraystretch}{1.1}
\setlength{\tabcolsep}{4pt}  % default 6pt
\begin{tabular}[t]{|rrr|}
\multicolumn{3}{c}{\normalsize{Stars}}\\
\hline
& \multicolumn{1}{c}{\multirow{2}{*}{\textbf{SHA}}} 
& \multicolumn{1}{c|}{\multirow{2}{*}{\textbf{Dec}}}\\
& & \multicolumn{1}{c|}{} \\
'''
    else:
        out = r'''\setlength{\tabcolsep}{5pt}  % default 6pt
\begin{tabular}[t]{|rrr|}
\multicolumn{3}{c}{\normalsize{Stars}}\\
\hline
\rule{0pt}{2.4ex} & \multicolumn{1}{c}{\textbf{SHA}} & \multicolumn{1}{c|}{\textbf{Dec}}\\
\hline\rule{0pt}{2.6ex}\noindent
'''
    stars = stellar(dfloat+1)
    for i in range(len(stars)):
        out = out + r'''{} & {} & {} \\
'''.format(stars[i][0],stars[i][1],stars[i][2])
    m = r'''\hline
'''

    # returns 3 tables with SHA & Mer.pass for Venus, Mars, Jupiter and Saturn
    for i in range(3):
        dt = ephem.date(dfloat+i).datetime()
        datestr = r'''{} {} {}'''.format(dt.strftime("%b"), dt.strftime("%d"), dt.strftime("%a"))
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
        datex = ephem.date(dfloat + i)
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
    
    out = out + r'''\end{tabular}'''
    return out

# >>>>>>>>>>>>>>>>>>>>>>>>
def sunmoontab(dfloat):
    # generates LaTeX table for sun and moon (traditional style)
    # OLD: \begin{tabular*}{0.54\textwidth}[t]{@{\extracolsep{\fill}}|c|rr|rrrrr|}
    # OLD note: 54% table width above removes "Overfull \hbox (1.65279pt too wide)"
    #                 and "Underfull \hbox (badness 10000)"
    # OLD: \begin{tabular}[t]{|C{15pt}|rr|rR{18pt}rR{18pt}r|}

    # note: table may have different widths due to the 1st column (e.g. Fri versus Wed)
    # note: table may have different widths due to the 'v' column (e.g. 6.9' versus 15.3')
    # note: table may have different widths due to the 'd' column (e.g. -8.2' versus -13.9')

    tab = r'''\noindent
\setlength{\tabcolsep}{5.8pt}  % default 6pt
\begin{tabular}[t]{|c|rr|rrrrr|}
\multicolumn{1}{c}{\normalsize{h}}& \multicolumn{2}{c}{\normalsize{Sun}} & \multicolumn{5}{c}{\normalsize{Moon}}\\
'''
    n = 0
    while n < 3:
        da = dfloat + n
        tab = tab + r'''\hline
\multicolumn{{1}}{{|c|}}{{\rule{{0pt}}{{2.6ex}}\textbf{{{}}}}} &\multicolumn{{1}}{{c}}{{\textbf{{GHA}}}} & \multicolumn{{1}}{{c|}}{{\textbf{{Dec}}}}  & \multicolumn{{1}}{{c}}{{\textbf{{GHA}}}} & \multicolumn{{1}}{{c}}{{\(\nu\)}} & \multicolumn{{1}}{{c}}{{\textbf{{Dec}}}} & \multicolumn{{1}}{{c}}{{\textit{{d}}}} & \multicolumn{{1}}{{c|}}{{\textbf{{HP}}}}\\
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
            da = dfloat + n
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
                if mNS != mlastNS or copysign(1.0,eph[8]) != copysign(1.0,nexteph[8]):
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

        vd = sun_moon_SD(dfloat + n)
        tab = tab + r'''\hline
\rule{{0pt}}{{2.4ex}} & \multicolumn{{1}}{{c}}{{SD = {}$'$}} & \multicolumn{{1}}{{c|}}{{\textit{{d}} = {}$'$}} & \multicolumn{{5}}{{c|}}{{SD = {}$'$}}\\
\hline
'''.format(vd[1],vd[0],vd[2])
        if n < 2:
            # add space between tables...
            tab = tab + r'''\multicolumn{7}{c}{}\\[-1.5ex]'''
        n += 1
    tab = tab + r'''\end{tabular}
'''
    return tab

# >>>>>>>>>>>>>>>>>>>>>>>>
def sunmoontabm(dfloat):
    # generates LaTeX table for sun and moon (modern style)

    tab = r'''\noindent
\renewcommand{\arraystretch}{1.1}
\setlength{\tabcolsep}{4pt}  % default 6pt
\quad
\begin{tabular}[t]{crrcrrrrr}
\multicolumn{1}{c}{\normalsize{h}} & 
\multicolumn{2}{c}{\normalsize{Sun}} & &
\multicolumn{5}{c}{\normalsize{Moon}}\\
\cmidrule{2-3} \cmidrule{5-9}'''
    # note: \quad\quad above shifts all tables to the right (still within margins)
    n = 0
    while n < 3:
        da = dfloat + n
        tab = tab + r'''
\multicolumn{{1}}{{c}}{{\textbf{{{}}}}} & \multicolumn{{1}}{{c}}{{\textbf{{GHA}}}} & \multicolumn{{1}}{{c}}{{\textbf{{Dec}}}} & & \multicolumn{{1}}{{c}}{{\textbf{{GHA}}}} & \multicolumn{{1}}{{c}}{{\textbf{{\(\nu\)}}}} & \multicolumn{{1}}{{c}}{{\textbf{{Dec}}}} & \multicolumn{{1}}{{c}}{{\textit{{d}}}} & \multicolumn{{1}}{{c}}{{\textbf{{HP}}}}\\
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
            da = dfloat + n
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
                if mNS != mlastNS or copysign(1.0,eph[8]) != copysign(1.0,nexteph[8]):
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

        vd = sun_moon_SD(dfloat + n)
        tab = tab + r'''\cmidrule{{2-3}} \cmidrule{{5-9}}
\multicolumn{{1}}{{c}}{{}} & \multicolumn{{1}}{{c}}{{\footnotesize{{SD = {}$'$}}}} & 
\multicolumn{{1}}{{c}}{{\footnotesize{{\textit{{d}} = {}$'$}}}} && \multicolumn{{5}}{{c}}{{\footnotesize{{SD = {}$'$}}}}\\
\cmidrule{{2-3}} \cmidrule{{5-9}}
'''.format(vd[1],vd[0],vd[2])
        if n < 2:
            vsep = "[-1.5ex]"
            if config.pgsz == "Letter":
                vsep = "[-2.0ex]"
            # add space between tables...
            tab = tab + r'''\multicolumn{{7}}{{c}}{{}}\\{}'''.format(vsep)
        n += 1
    tab = tab + r'''\end{tabular}\quad\quad
'''
    return tab

# >>>>>>>>>>>>>>>>>>>>>>>>
def twilighttab(dfloat):
    # returns the twilight and moonrise tables, finally EoT data

# Twilight tables ...........................................
    #lat = [72,70,68,66,64,62,60,58,56,54,52,50,45,40,35,30,20,10,0, -10,-20,-30,-35,-40,-45,-50,-52,-54,-56,-58,-60]
    latNS = [72, 70, 58, 40, 10, -10, -50, -60]
    # OLD: \begin{tabular*}{0.45\textwidth}[t]{@{\extracolsep{\fill}}|r|ccc|ccc|}

    if config.tbls == "m":
    # The header begins with a thin empty row as top padding; and the top row with
    # bold text has some padding below it. This result gives a balanced impression.
        tab = r'''\renewcommand{\arraystretch}{1.05}
\setlength{\tabcolsep}{5pt}  % default 6pt
\begin{tabular}[t]{|r|ccc|ccc|}
\multicolumn{7}{c}{\normalsize{}}\\
\hline
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
        tab = r'''\setlength{\tabcolsep}{5.8pt}  % default 6pt
\begin{tabular}[t]{|r|ccc|ccc|}
\multicolumn{7}{c}{\normalsize{}}\\
\hline
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
            hsph = ""
        else:
            hsph = hemisph
            if j%6 == 0:
                tab = tab + r'''\rule{0pt}{2.6ex}
'''
        lasthemisph = hemisph
        # day+1 to calculate for the second day (three days are printed on one page)
        twi = twilight(dfloat+1, i, hemisph)
        line = r'''\textbf{{{}}}'''.format(hsph) + " " + r'''{}$^\circ$'''.format(abs(i))
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

    weekday = [ephem.date(dfloat).datetime().strftime("%a"),ephem.date(dfloat+1).datetime().strftime("%a"),ephem.date(dfloat+2).datetime().strftime("%a")]
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
            hsph = ""
        else:
            hsph = hemisph
            if j%6 == 0:
                tab = tab + r'''\rule{0pt}{2.6ex}
'''
        lasthemisph = hemisph
        moon, moon2 = moonrise_set(dfloat,i)
        if not(double_events_found(moon,moon2)):
            tab = tab + r'''\textbf{{{}}}'''.format(hsph) + " " + r'''{}$^\circ$'''.format(abs(i))
            tab = tab + r''' & {} & {} & {} & {} & {} & {} \\
'''.format(moon[0],moon[1],moon[2],moon[3],moon[4],moon[5])
        else:
# print a row with two moonrise/moonset events on the same day & latitude
            tab = tab + r'''\multirow{{2}}{{*}}{{\textbf{{{}}} {}$^\circ$}}'''.format(hsph,abs(i))
            #cellcolor = r'''\cellcolor[gray]{0.9}'''
# top row...
            for k in range(len(moon)):
                if moon2[k] != '--:--':
                    #tab = tab + r''' & {}'''.format(cellcolor + moon[k])
                    tab = tab + r''' & \colorbox{{khaki!45}}{{{}}}'''.format(moon[k])
                else:
                    tab = tab + r''' & \multirow{{2}}{{*}}{{{}}}'''.format(moon[k])
            tab = tab + r'''\\
'''	# terminate top row
# bottom row...
            for k in range(len(moon)):
                if moon2[k] != '--:--':
                    #tab = tab + r''' & {}'''.format(cellcolor + moon2[k])
                    tab = tab + r''' & \colorbox{{khaki!45}}{{{}}}'''.format(moon2[k])
                else:
                    tab = tab + r'''&'''
            tab = tab + r'''\\
'''	# terminate bottom row
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
        d = ephem.date(dfloat+k)
        eq = equation_of_time(d)
        if k == 2:
            tab = tab + r'''{} & {} & {} & {} & {} & {} & {}({}\%) \\[0.3ex]
'''.format(d.datetime().strftime("%d"),eq[0],eq[1],eq[2],eq[3],eq[4],eq[5],eq[6])
        else:
            tab = tab + r'''{} & {} & {} & {} & {} & {} & {}({}\%) \\
'''.format(d.datetime().strftime("%d"),eq[0],eq[1],eq[2],eq[3],eq[4],eq[5],eq[6])
    tab = tab + r'''\hline
\end{tabular}'''
    return tab

#----------------------
#   page preparation
#----------------------

def doublepage(first_day, page1):
    # creates a doublepage (3 days) of the nautical almanac

    first_day = r'''{}/{}/{}'''.format(first_day.year,first_day.month,first_day.day)
    dfloat = ephem.Date(first_day)      # convert date to float
    page = ''

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    if config.FANCYhd:
        page = r'''
% ------------------ N E W   E V E N   P A G E ------------------
\newpage'''

        page += r'''
  \newgeometry{{nomarginpar, top={}, bottom={}, outer={}, inner={}, headsep={}, footskip={}}}'''.format(eventm,evenbm,evenom,evenim,evenhs,evenfs)
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    else:   # old formatting
        if not(page1):
            page = r'''
% ------------------ N E W   E V E N   P A G E ------------------
\newpage
\restoregeometry    % reset to even-page margins'''
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    leftindent = ""
    rightindent = ""
    if config.tbls == "m":
        leftindent = "\quad"
        rightindent = "\hphantom{\quad}"

    # print date based on dfloat (as Ephem routines use dfloat)
# ...........................................................
    if config.FANCYhd:
        page += r'''
\sffamily
\fancyhead[LE]{{{}\textsf{{\textbf{{{}, {}, {}   ({}.,  {}.,  {}.)}}}}}}'''.format(leftindent,ephem.date(dfloat).datetime().strftime("%B %d"),ephem.date(dfloat+1).datetime().strftime("%d"),ephem.date(dfloat+2).datetime().strftime("%d"),ephem.date(dfloat).datetime().strftime("%a"),ephem.date(dfloat+1).datetime().strftime("%a"),ephem.date(dfloat+2).datetime().strftime("%a"))

        page = page + r'''
\begin{scriptsize}
'''
# ...........................................................
    else:   # old formatting
        page = page + r'''
\sffamily
\noindent
{}\textbf{{{}, {}, {}   ({}.,  {}.,  {}.)}}'''.format(leftindent,ephem.date(dfloat).datetime().strftime("%B %d"),ephem.date(dfloat+1).datetime().strftime("%d"),ephem.date(dfloat+2).datetime().strftime("%d"),ephem.date(dfloat).datetime().strftime("%a"),ephem.date(dfloat+1).datetime().strftime("%a"),ephem.date(dfloat+2).datetime().strftime("%a"))

        if config.tbls == "m":
            page += r'\\[1.0ex]'  # \par leaves about 1.2ex
        else:
            page += r'\\[0.7ex]'

        page += r'''
\begin{scriptsize}
'''
# ...........................................................

    if config.tbls == "m":
        page += planetstabm(dfloat)
    else:
        page += planetstab(dfloat) + r'''\enskip
'''
    page += starstab(dfloat)
    # print date based on dfloat (as Ephem routines use dfloat)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    if config.FANCYhd:
        str1 = r'''
\end{scriptsize}
% ------------------ N E W   O D D   P A G E ------------------
\newpage'''
        str1 += r'''
  \newgeometry{{nomarginpar, top={}, bottom={}, inner={}, outer={}, headsep={}, footskip={}}}'''.format(oddtm,oddbm,oddim,oddom,oddhs,oddfs)
        str1 += r'''
\fancyhead[RO]{{\textsf{{\textbf{{{} to {}}}}}}}
\fancyheadoffset[RO]{{0pt}}% bugfix - otherwise its shifted right
\begin{{scriptsize}}
'''.format(ephem.date(dfloat).datetime().strftime("%Y %B %d"), ephem.date(dfloat+2).datetime().strftime("%b. %d"))
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    else:   # old formatting
        str1 = r'''
\end{{scriptsize}}
% ------------------ N E W   O D D   P A G E ------------------
\newpage
\newgeometry{{nomarginpar, top={}, bottom={}, left={}, right={}}}
\begin{{flushright}}
\textbf{{{} to {}}}{}%
\end{{flushright}}\par
\begin{{scriptsize}}
'''.format(oddtm, bm, oddim, oddom, ephem.date(dfloat).datetime().strftime("%Y %B %d"), ephem.date(dfloat+2).datetime().strftime("%b. %d"), rightindent)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    page += str1

    if config.tbls == "m":
        page += sunmoontabm(dfloat)
    else:
        page += sunmoontab(dfloat) + r'''\enskip
'''
    page += twilighttab(dfloat)
    # to avoid "Overfull \hbox" messages, leave a paragraph end before the end of a size change. (This may only apply to tabular* table style) See lines below...
    page += r'''
\end{scriptsize}'''
    return page


def pages(first_day, dtp):
    # dtp = 0 if for entire year; = -1 if for entire month; else days to print

    out = ''
    page1 = True
    dpp = 3         # 3 days per page
    day1 = first_day

    if dtp == 0:        # if entire year
        year = first_day.year
        yr = year
        while year == yr:
            day3 = day1 + timedelta(days=2)
            out += doublepage(day1, page1)
            page1 = False
            day1 += timedelta(days=3)
            year = day1.year
    elif dtp == -1:     # if entire month
        mth = first_day.month
        m = mth
        while mth == m:
            day3 = day1 + timedelta(days=2)
            out += doublepage(day1, page1)
            page1 = False
            day1 += timedelta(days=3)
            mth = day1.month
    else:           # print 'dtp' days beginning with first_day
        i = dtp   # don't decrement dtp
        while i > 0:
            out += doublepage(day1, page1)
            page1 = False
            i -= 3
            day1 += timedelta(days=3)

    return out

#--------------------------
#   external entry point
#--------------------------

def almanac(first_day, dtp):
    # make almanac starting from first_day
    # dtp = 0 if for entire year; = -1 if for entire month; else days to print

    if config.FANCYhd:
        return makeNAnew(first_day, dtp) # use the 'fancyhdr' package
    else:
        return makeNAold(first_day, dtp) # use old formatting

#   The following functions are intentionally separate functions.
#   'makeEVold' is required for TeX Live 2019, which is the standard
#   version in Ubuntu 20.04 LTS which expires in April 2030.

def hdrNAnew(first_day, dtp, tm1, bm1, lm1, rm1, vsep1, vsep2):
    # build the front page

    tex = r'''
\pagestyle{frontpage}
    \begin{titlepage}
    \begin{center}
    \textsc{\Large Generated using Ephem}\\[0.7cm]'''

    if config.dockerized:   # DOCKER ONLY
        fn = "../A4chartNorth_P.pdf"
    else:
        fn = "./A4chartNorth_P.pdf"

    tex += r'''
    % TRIM values: left bottom right top
    \includegraphics[clip, trim=5mm 8cm 5mm 21mm, width=0.8\textwidth]{{{}}}\\'''.format(fn)

    tex += r'''[{}]
    \textsc{{\huge The Nautical Almanac}}\\[{}]'''.format(vsep1,vsep2)

    if dtp == 0:
        tex += r'''
    \HRule \\[0.5cm]
    {{ \Huge \bfseries {}}}\\[0.2cm]
    \HRule \\'''.format(first_day.year)
    elif dtp == -1:
        tex += r'''
    \HRule \\[0.5cm]
    {{ \Huge \bfseries {}}}\\[0.2cm]
    \HRule \\'''.format(first_day.strftime("%B %Y"))
    elif dtp > 1:
        tex += r'''
    \HRule \\[0.5cm]
    {{ \Huge \bfseries {}}}\\[0.2cm]
    \HRule \\'''.format(fmtdates(first_day,first_day+timedelta(days=dtp-1)))
    else:
        tex += r'''
    \HRule \\[0.5cm]
    {{ \Huge \bfseries {}}}\\[0.2cm]
    \HRule \\'''.format(fmtdate(first_day))

    if config.tbls == "m":
        tex += r'''
    \begin{center}\begin{tabular}[t]{rl}
    \large\emph{Author:} & \large Andrew \textsc{Bauer}\\
    \large\emph{Original concept from:} & \large Enno \textsc{Rodegerdts}\\
    \end{tabular}\end{center}'''
    else:
        tex += r'''
    \begin{center}\begin{tabular}[t]{rl}
    \large\emph{Original author:} & \large Enno \textsc{Rodegerdts}\\
    \large\emph{Enhancements:} & \large Andrew \textsc{Bauer}\\
    \end{tabular}\end{center}'''

    tex += r'''
    {\large \today}
    \HRule \\[0.2cm]
    \end{center}
    \begin{description}[leftmargin=5.5em,style=nextline]\footnotesize
    \item[Disclaimer:] These are computer generated tables - use them at your own risk.
    The accuracy has been randomly checked, but cannot be guaranteed.
    The author claims no liability for any consequences arising from use of these tables.
    Besides, this publication only contains the 'daily pages' of the Nautical Almanac: an official version of the Nautical Almanac is indispensable.
    \end{description}
\end{titlepage}'''

    return tex

def makeNAnew(first_day, dtp):
    # make almanac starting from first_day
    global oddtm,  oddbm,  oddim,  oddom,  oddhs,  oddfs  # required by doublepage
    global eventm, evenbm, evenim, evenom, evenhs, evenfs

    # NOTE: 'bm' (bottom margin) is an unrealistic value used only to determine the vertical size of 'body' (textheight), which must be large enough to include all the tables. 'tm' (top margin) and 'hds' (headsep) determine the top of body. Note: 'fs' (footskip) does not position the footer.

    # page size specific parameters
    if config.pgsz == "A4":
        # A4 ... pay attention to the limited page width
        paper = "a4paper"
        # title page...
        vsep1 = "2.0cm"
        vsep2 = "1.5cm"
        tm1 = "21mm"
        bm1 = "15mm"
        lm1 = "10mm"
        rm1 = "10mm"
        # even data pages...
        eventm = "25mm"     # data pages... was "21mm"
        evenbm = "16mm"     # was "18mm"
        evenhs = "1.8pt"    # headsep  (page 2 onwards)
        evenfs = "12pt"     # footskip (page 2 onwards)
        evenim = "10mm"     # inner margin (right side on even pages)
        evenom = "9mm"      # outer margin (left side on even pages)
        # odd data pages...
        oddtm = "27.5mm"    # was "21mm"
        oddbm = "16mm"      # was "18mm"
        oddhs = "6.5pt"     # headsep  (page 3 onwards)
        oddfs = "12pt"      # footskip (page 3 onwards)
        oddim = "14mm"      # inner margin (left side on odd pages)
        oddom = "11mm"      # outer margin (right side on odd pages)
        if config.tbls == "m":
            # even data pages...
            eventm = "15.8mm"   # was "10mm"
            evenbm = "12mm"     # was "15mm"
            evenhs = "3.0pt"    # headsep  (page 2 onwards)
            evenfs = "12pt"     # footskip (page 2 onwards)
            evenim = "10mm"
            evenom = "10mm"
            # odd data pages...
            oddtm = "16mm"      # was "10mm"
            oddbm = "13mm"      # was "15mm"
            oddhs = "4.6pt"     # headsep  (page 3 onwards)
            oddfs = "12pt"      # footskip (page 3 onwards)
            oddim = "14mm"
            oddom = "11mm"
    else:
        # LETTER ... pay attention to the limited page height
        paper = "letterpaper"
        # title page...
        vsep1 = "1.5cm"
        vsep2 = "1.0cm"
        tm1 = "12mm"
        bm1 = "15mm"
        lm1 = "12mm"
        rm1 = "12mm"
        # even data pages...
        eventm = "17.2mm"   # data pages... was "12.2mm"
        evenbm = "12mm"     # was "13mm"
        evenhs = "1.5pt"    # headsep  (page 2 onwards)
        evenfs = "12pt"     # footskip (page 2 onwards)
        evenim = "13mm"     # inner margin (right side on even pages)
        evenom = "13mm"     # outer margin (left side on even pages)
        # odd data pages...
        oddtm = "19mm"      # was "12.2mm"
        oddbm = "12mm"      # was "13mm"
        oddhs = "6.1pt"     # headsep  (page 3 onwards)
        oddfs = "12pt"      # footskip (page 3 onwards)
        oddim = "14mm"      # inner margin (left side on odd pages)
        oddom = "11mm"      # outer margin (right side on odd pages)
        if config.tbls == "m":
            # even data pages...
            eventm = "9.4mm"    # was "4mm"
            evenbm = "8mm"      # was "8mm"
            evenhd = "2.8pt"    # headsep  (page 2 onwards)
            evenfs = "12pt"     # footskip (page 2 onwards)
            evenim = "12.5mm"
            evenom = "12.5mm"
            # odd data pages... use 26.06.2024 as a testcase
            oddtm = "8mm"       # was "4mm"
            oddbm = "8mm"       # was "8mm"
            oddhs = "0pt"       # headsep  (page 3 onwards)
            oddfs = "12pt"      # footskip (page 3 onwards)
            oddim = "13mm"
            oddom = "13mm"

#------------------------------------------------------------------------------
#   This edition employs the 'fancyhdr' v4.0.3 package
#   CAUTION: do not use '\newgeometry' & '\restoregeometry' as advised here:
#   https://tex.stackexchange.com/questions/247972/top-margin-fancyhdr
#------------------------------------------------------------------------------

    tex = r'''\documentclass[10pt, twoside, {}]{{report}}'''.format(paper)

    # document preamble...
    tex += r'''
%\usepackage[utf8]{inputenc}
\usepackage[english]{babel}
\usepackage{fontenc}
\usepackage{enumitem} % used to customize the {description} environment'''

    # to troubleshoot add "showframe, verbose," below:
    tex += r'''
\usepackage[nomarginpar, top={}, bottom={}, left={}, right={}]{{geometry}}'''.format(tm1,bm1,lm1,rm1)

    # define page styles
    tex += r'''
%------------ page styles ------------
\usepackage{fancyhdr}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\fancypagestyle{frontpage}{
%  \fancyhf{}% clear all header and footer fields
}
\fancypagestyle{datapage}[frontpage]{'''

    tex += r'''
  \fancyfootoffset[R]{0pt}% recalculate \headwidth
  \cfoot{\centerline{Page \thepage}}
  \fancyfoot[LE,RO]{\textsf{\footnotesize{https://pypi.org/project/pyalmanac/}}}
} %-----------------------------------'''

    if config.tbls == "m":
        tex += r'''
\usepackage[table]{xcolor}
% [table] option loads the colortbl package for coloring rows, columns, and cells within tables.
\definecolor{LightCyan}{rgb}{0.88,1,1}
\usepackage{booktabs}'''
    else:
        tex += r'''
\usepackage{xcolor}  % highlight double moon events on same day'''

    # Note: \DeclareUnicodeCharacter is not compatible with some versions of pdflatex
    tex += r'''
\definecolor{khaki}{rgb}{0.76, 0.69, 0.57}
\usepackage{multirow}
\newcommand{\HRule}{\rule{\linewidth}{0.5mm}}
\usepackage[pdftex]{graphicx}	% for \includegraphics
\usepackage{tikz}				% for \draw  (load after 'graphicx')
%\showboxbreadth=50  % use for logging
%\showboxdepth=50    % use for logging
%\DeclareUnicodeCharacter{00B0}{\ensuremath{{}^\circ}}
\setlength\fboxsep{1.5pt}       % ONLY used by \colorbox in alma_ephem.py
\begin{document}'''

    if not config.DPonly:
        tex += hdrNAnew(first_day,dtp,tm1,bm1,lm1,rm1,vsep1,vsep2)

# NOTE: the first data page must be even (otherwise there's no header)
    tex += r'''
\pagestyle{datapage}  % the default page style for the document
\setcounter{page}{2}'''

    tex += pages(first_day,dtp)
    tex += r'''
\end{document}'''
    return tex

# ===   ===   ===   ===   ===   ===   ===   ===   ===   ===   ===   ===   ===
# ===   ===   ===   ===   O L D   F O R M A T T I N G   ===   ===   ===   ===
# ===   ===   ===   ===   ===   ===   ===   ===   ===   ===   ===   ===   ===

def hdrNAold(first_day, dtp, tm1, bm1, lm1, rm1, vsep1, vsep2):
    # build the front page

    tex = r'''
% for the title page only...
\newgeometry{{nomarginpar, top={}, bottom={}, left={}, right={}}}'''.format(tm1,bm1,lm1,rm1)

    tex += r'''
    \begin{titlepage}
    \begin{center}
    \textsc{\Large Generated using Ephem}\\[0.7cm]'''

    if config.dockerized:   # DOCKER ONLY
        fn = "../A4chartNorth_P.pdf"
    else:
        fn = "./A4chartNorth_P.pdf"

    tex += r'''
    % TRIM values: left bottom right top
    \includegraphics[clip, trim=5mm 8cm 5mm 21mm, width=0.8\textwidth]{{{}}}\\'''.format(fn)

    tex += r'''[{}]
    \textsc{{\huge The Nautical Almanac}}\\[{}]'''.format(vsep1,vsep2)

    if dtp == 0:
        tex += r'''
    \HRule \\[0.5cm]
    {{ \Huge \bfseries {}}}\\[0.2cm]
    \HRule \\'''.format(first_day.year)
    elif dtp == -1:
        tex += r'''
    \HRule \\[0.5cm]
    {{ \Huge \bfseries {}}}\\[0.2cm]
    \HRule \\'''.format(first_day.strftime("%B %Y"))
    elif dtp > 1:
        tex += r'''
    \HRule \\[0.5cm]
    {{ \Huge \bfseries {}}}\\[0.2cm]
    \HRule \\'''.format(fmtdates(first_day,first_day+timedelta(days=dtp-1)))
    else:
        tex += r'''
    \HRule \\[0.5cm]
    {{ \Huge \bfseries {}}}\\[0.2cm]
    \HRule \\'''.format(fmtdate(first_day))

    if config.tbls == "m":
        tex += r'''
    \begin{center}\begin{tabular}[t]{rl}
    \large\emph{Author:} & \large Andrew \textsc{Bauer}\\
    \large\emph{Original concept from:} & \large Enno \textsc{Rodegerdts}\\
    \end{tabular}\end{center}'''
    else:
        tex += r'''
    \begin{center}\begin{tabular}[t]{rl}
    \large\emph{Original author:} & \large Enno \textsc{Rodegerdts}\\
    \large\emph{Enhancements:} & \large Andrew \textsc{Bauer}\\
    \end{tabular}\end{center}'''

    tex += r'''
    {\large \today}
    \HRule \\[0.2cm]
    \end{center}
    \begin{description}[leftmargin=5.5em,style=nextline]\footnotesize
    \item[Disclaimer:] These are computer generated tables - use them at your own risk.
    The accuracy has been randomly checked, but cannot be guaranteed.
    The author claims no liability for any consequences arising from use of these tables.
    Besides, this publication only contains the 'daily pages' of the Nautical Almanac: an official version of the Nautical Almanac is indispensable.
    \end{description}
\end{titlepage}
\restoregeometry    % so it does not affect the rest of the pages'''

    return tex

def makeNAold(first_day, dtp):
    # make almanac starting from first_day
    global tm, bm, oddtm, oddim, oddom     # required by doublepage

    # page size specific parameters
    if config.pgsz == "A4":
        # A4 ... pay attention to the limited page width
        paper = "a4paper"
        vsep1 = "2.0cm"
        vsep2 = "1.5cm"
        tm1 = "21mm"    # title page...
        bm1 = "15mm"
        lm1 = "10mm"
        rm1 = "10mm"
        tm = "21mm"     # data pages...
        bm = "18mm"
        # even data pages...
        im = "10mm"     # inner margin (right side on even pages)
        om = "9mm"      # outer margin (left side on even pages)
        # odd data pages...
        oddtm = tm
        oddim = "14mm"  # inner margin (left side on odd pages)
        oddom = "11mm"  # outer margin (right side on odd pages)
        if config.tbls == "m":
            # even data pages...
            tm = "10mm"
            bm = "15mm"
            im = "10mm"
            om = "10mm"
            # odd data pages...
            oddtm = tm
            oddim = "14mm"
            oddom = "11mm"
    else:
        # LETTER ... pay attention to the limited page height
        paper = "letterpaper"
        vsep1 = "1.5cm"
        vsep2 = "1.0cm"
        tm1 = "12mm"    # title page...
        bm1 = "15mm"
        lm1 = "12mm"
        rm1 = "12mm"
        tm = "12.2mm"   # data pages...
        bm = "13mm"
        # even data pages...
        im = "13mm"     # inner margin (right side on even pages)
        om = "13mm"     # outer margin (left side on even pages)
        # odd data pages...
        oddtm = tm
        oddim = "14mm"  # inner margin (left side on odd pages)
        oddom = "11mm"  # outer margin (right side on odd pages)
        if config.tbls == "m":
            # even data pages...
            tm = "4mm"
            bm = "8mm"
            im = "12mm"
            om = "12mm"
            # odd data pages... use 26.06.2024 & 18.06.2025 as testcases
            oddtm = "2.6mm"
            oddim = "14mm"
            oddom = "14mm"

    tex = r'''\documentclass[10pt, twoside, {}]{{report}}'''.format(paper)

    tex += r'''
%\usepackage[utf8]{inputenc}
\usepackage[english]{babel}
\usepackage{fontenc}
\usepackage{enumitem} % used to customize the {description} environment'''

    # to troubleshoot add "showframe, verbose," below:
    tex += r'''
\usepackage[nomarginpar, top={}, bottom={}, left={}, right={}]{{geometry}}'''.format(tm,bm,im,om)

    if config.tbls == "m":
        tex += r'''
\usepackage[table]{xcolor}
% [table] option loads the colortbl package for coloring rows, columns, and cells within tables.
\definecolor{LightCyan}{rgb}{0.88,1,1}
\usepackage{booktabs}'''
    else:
        tex += r'''
\usepackage{xcolor}  % highlight double moon events on same day'''

    # Note: \DeclareUnicodeCharacter is not compatible with some versions of pdflatex
    tex += r'''
\definecolor{khaki}{rgb}{0.76, 0.69, 0.57}
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

    if not config.DPonly:
        tex += hdrNAold(first_day,dtp,tm1,bm1,lm1,rm1,vsep1,vsep2)

    # Nautical Almanac pages begin with a left page (page 2)
    tex += r'''
\setcounter{page}{2}'''

    tex += pages(first_day,dtp)
    tex += r'''
\end{document}'''
    return tex