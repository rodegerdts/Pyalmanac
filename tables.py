#!/usr/bin/env python2
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

def planetstab(date):
    # generates a LaTeX table for the navigational plantets (traditional style)
    tab = r'''\noindent
    \begin{tabular*}{0.75\textwidth}[t]{@{\extracolsep{\fill}}|c|r|rr|rr|rr|rr|}
    \multicolumn{1}{c}{\normalsize{}} & \multicolumn{1}{c}{\normalsize{Aries}} &  \multicolumn{2}{c}{\normalsize{Venus}}& \multicolumn{2}{c}{\normalsize{Mars}} & \multicolumn{2}{c}{\normalsize{Jupiter}} & \multicolumn{2}{c}{\normalsize{Saturn}}\\ 
'''
    n = 0
    while n < 3:
        da = date + n
        tab = tab + r'''\hline
    \rule{0pt}{2.4ex}\textbf{%s} & \multicolumn{1}{c|}{\textbf{GHA}} & \multicolumn{1}{c}{\textbf{GHA}} & \multicolumn{1}{c|}{\textbf{Dec}} & \multicolumn{1}{c}{\textbf{GHA}} & \multicolumn{1}{c|}{\textbf{Dec}}& \multicolumn{1}{c}{\textbf{GHA}} & \multicolumn{1}{c|}{\textbf{Dec}}& \multicolumn{1}{c}{\textbf{GHA}} & \multicolumn{1}{c|}{\textbf{Dec}} \\ 
    \hline\rule{0pt}{2.6ex}\noindent
''' %(ephem.date(da).datetime().strftime("%a"))
        h = 0

        if config.decf != '+':	# USNO format for Declination
            # first populate an array of 24 hours with all data
            hourlydata = [[] for i in range(24)]
            while h < 24:
                hourlydata[h] = planets(da)
                da = da + ephem.hour
                h += 1
            # now print the data per hour
            da = date + n
            h = 0
            vlastNS = ''
            mlastNS = ''
            jlastNS = ''
            slastNS = ''
            while h < 24:
                eph = hourlydata[h]
                if h < 23:
                    nexteph = hourlydata[h+1]
                else:
                    nexteph = hourlydata[23]	# hour 24 = hour 23

                # format declination checking for hemisphere change
                vdec, vNS = NSdeg(eph[2],False,h)
                if vNS != vlastNS or math.copysign(1.0,eph[9]) != math.copysign(1.0,nexteph[9]):
                    vdec, vNS = NSdeg(eph[2],False,h,True)	# force NS
                mdec, mNS = NSdeg(eph[4],False,h)
                if mNS != mlastNS or math.copysign(1.0,eph[10]) != math.copysign(1.0,nexteph[10]):
                    mdec, mNS = NSdeg(eph[4],False,h,True)	# force NS
                jdec, jNS = NSdeg(eph[6],False,h)
                if jNS != jlastNS or math.copysign(1.0,eph[11]) != math.copysign(1.0,nexteph[11]):
                    jdec, jNS = NSdeg(eph[6],False,h,True)	# force NS
                sdec, sNS = NSdeg(eph[8],False,h)
                if sNS != slastNS or math.copysign(1.0,eph[12]) != math.copysign(1.0,nexteph[12]):
                    sdec, sNS = NSdeg(eph[8],False,h,True)	# force NS
                vlastNS = vNS
                mlastNS = mNS
                jlastNS = jNS
                slastNS = sNS

                line = "%s & %s & %s & %s & %s & %s & %s & %s & %s & %s" %(h,eph[0],eph[1],vdec,eph[3],mdec,eph[5],jdec,eph[7],sdec)
                lineterminator = "\\\ \n"
                if h < 23 and (h+1)%6 == 0:
                    lineterminator = "\\\[2Pt] \n"
                tab = tab + line + lineterminator
                h += 1
                da = da + ephem.hour

        else:			# Positive/Negative Declinations
            while h < 24:
                eph = planets(da)
                line = "%s & %s & %s & %s & %s & %s & %s & %s & %s & %s" %(h,eph[0],eph[1],eph[2],eph[3],eph[4],eph[5],eph[6],eph[7],eph[8])
                lineterminator = "\\\ \n"
                if h < 23 and (h+1)%6 == 0:
                    lineterminator = "\\\[2Pt] \n"
                tab = tab + line + lineterminator
                h += 1
                da = da + ephem.hour

        vd = vdmean(date + n)
        tab = tab + r"""\hline 
        \multicolumn{2}{|c|}{\rule{0pt}{2.4ex}Mer.pass.:%s} &  \multicolumn{2}{c|}{v%s d%s m%s}& \multicolumn{2}{c|}{v%s d%s m%s} & \multicolumn{2}{c|}{v%s d%s m%s} & \multicolumn{2}{c|}{v%s d%s m%s}\\ 
        \hline
        \multicolumn{10}{c}{}\\
""" %(ariestransit(date + n),vd[3],vd[4],vd[5],vd[6],vd[7],vd[8],vd[9],vd[10],vd[11],vd[12],vd[13],vd[14])
        n += 1

    tab = tab + r"""\end{tabular*}
"""
    return tab


def planetstabm(date):
    # generates a LaTeX table for the navigational plantets (modern style)
    tab = r'''\vspace{6Pt}\noindent
    \renewcommand{\arraystretch}{1.1}
    \setlength{\tabcolsep}{4pt}
    \begin{tabular}[t]{@{}crcrrcrrcrrcrr@{}}
    \multicolumn{1}{c}{\normalsize{h}} & 
    \multicolumn{1}{c}{\normalsize{Aries}} & & 
    \multicolumn{2}{c}{\normalsize{Venus}}& & 
    \multicolumn{2}{c}{\normalsize{Mars}} & & 
    \multicolumn{2}{c}{\normalsize{Jupiter}} & & 
    \multicolumn{2}{c}{\normalsize{Saturn}}\\ 
    \cmidrule{2-2} \cmidrule{4-5} \cmidrule{7-8} \cmidrule{10-11} \cmidrule{13-14}
'''
    n = 0
    while n < 3:
        da = date + n
        tab = tab + r'''
    \multicolumn{1}{c}{\textbf{%s}} & \multicolumn{1}{c}{\textbf{GHA}} && 
    \multicolumn{1}{c}{\textbf{GHA}} & \multicolumn{1}{c}{\textbf{Dec}} &&  \multicolumn{1}{c}{\textbf{GHA}} & \multicolumn{1}{c}{\textbf{Dec}} &&  \multicolumn{1}{c}{\textbf{GHA}} & \multicolumn{1}{c}{\textbf{Dec}} &&  \multicolumn{1}{c}{\textbf{GHA}} & \multicolumn{1}{c}{\textbf{Dec}} \\
''' %(ephem.date(da).datetime().strftime("%a"))
        h = 0

        if config.decf != '+':	# USNO format for Declination
            # first populate an array of 24 hours with all data
            hourlydata = [[] for i in range(24)]
            while h < 24:
                hourlydata[h] = planets(da)
                da = da+ephem.hour
                h += 1
            # now print the data per hour
            da = date + n
            h = 0
            vlastNS = ''
            mlastNS = ''
            jlastNS = ''
            slastNS = ''
            while h < 24:
                band = int(h/6)
                group = band % 2
                eph = hourlydata[h]
                if h < 23:
                    nexteph = hourlydata[h+1]
                else:
                    nexteph = hourlydata[23]	# hour 24 = hour 23

                # format declination checking for hemisphere change
                vdec, vNS = NSdeg(eph[2],True,h)
                if vNS != vlastNS or math.copysign(1.0,eph[9]) != math.copysign(1.0,nexteph[9]):
                    vdec, vNS = NSdeg(eph[2],True,h,True)	# force NS
                mdec, mNS = NSdeg(eph[4],True,h)
                if mNS != mlastNS or math.copysign(1.0,eph[10]) != math.copysign(1.0,nexteph[10]):
                    mdec, mNS = NSdeg(eph[4],True,h,True)	# force NS
                jdec, jNS = NSdeg(eph[6],True,h)
                if jNS != jlastNS or math.copysign(1.0,eph[11]) != math.copysign(1.0,nexteph[11]):
                    jdec, jNS = NSdeg(eph[6],True,h,True)	# force NS
                sdec, sNS = NSdeg(eph[8],True,h)
                if sNS != slastNS or math.copysign(1.0,eph[12]) != math.copysign(1.0,nexteph[12]):
                    sdec, sNS = NSdeg(eph[8],True,h,True)	# force NS
                vlastNS = vNS
                mlastNS = mNS
                jlastNS = jNS
                slastNS = sNS

                line = r'''\color{blue} {%s} & 
''' %(h)
                line = line + "%s && %s & %s && %s & %s && %s & %s && %s & %s\\\ \n" %(eph[0],eph[1],vdec,eph[3],mdec,eph[5],jdec,eph[7],sdec)
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
                eph = planets(da)
                line = r'''\color{blue} {%s} & 
''' %(h)
                line = line + "%s && %s & %s && %s & %s && %s & %s && %s & %s\\\ \n" %(eph[0],eph[1],eph[2],eph[3],eph[4],eph[5],eph[6],eph[7],eph[8])
                if group == 1:
                    tab = tab + r'''\rowcolor{LightCyan}
'''
                tab = tab + line
                h += 1
                da = da + ephem.hour

        vd = vdmean(date + n)
        tab = tab + r"""\cmidrule{1-2} \cmidrule{4-5} \cmidrule{7-8} \cmidrule{10-11} \cmidrule{13-14} 
        \multicolumn{2}{c}{\footnotesize{Mer.pass.:%s}} && 
        \multicolumn{2}{c}{\footnotesize{v%s d%s m%s}} && 
        \multicolumn{2}{c}{\footnotesize{v%s d%s m%s}} && 
        \multicolumn{2}{c}{\footnotesize{v%s d%s m%s}} && 
        \multicolumn{2}{c}{\footnotesize{v%s d%s m%s}}\\ 
        \cmidrule{1-2} \cmidrule{4-5} \cmidrule{7-8} \cmidrule{10-11} \cmidrule{13-14}
""" %(ariestransit(date + n),vd[3],vd[4],vd[5],vd[6],vd[7],vd[8],vd[9],vd[10],vd[11],vd[12],vd[13],vd[14])
        if n < 2:
            tab = tab + r"""\multicolumn{10}{c}{}\\
"""
        n += 1

    tab = tab+r"""
    \end{tabular}
    \quad"""
    return tab


def starstab(date):
    # returns a table with ephemerieds for the navigational stars
    out = r"""\begin{tabular*}{0.25\textwidth}[t]{@{\extracolsep{\fill}}|rrr|}
    \multicolumn{3}{c}{\normalsize{Stars}}  \\ 
"""
    if config.tbls == "m":
        out = out + r"""\hline
        & \multicolumn{1}{c}{\multirow{2}{*}{\textbf{SHA}}} 
        & \multicolumn{1}{c|}{\multirow{2}{*}{\textbf{Dec}}} \\
        & & \multicolumn{1}{c|}{} \\
"""
    else:
        out = out + r"""\hline
        \rule{0pt}{2.4ex} & \multicolumn{1}{c}{\textbf{SHA}} & \multicolumn{1}{c|}{\textbf{Dec}} \\ 
        \hline\rule{0pt}{2.6ex}\noindent
"""
    stars = stellar(date+1)
    for i in range(len(stars)):
        out = out + r"""%s & %s & %s \\""" %(stars[i][0],stars[i][1],stars[i][2])
        out = out + '\n'
    m = '\\hline\n'

    # returns 3 tables with SHA & Mer.pass for Venus, Mars, Jupiter and Saturn
    for i in range(3):
        datestr = r"""\rule{0pt}{2.6ex}%s %s %s""" %(ephem.date(date+i).datetime().strftime("%b"), ephem.date(date+i).datetime().strftime("%d"), ephem.date(date+i).datetime().strftime("%a"))
        m = m + '\\hline \n'
        if config.tbls == "m":
            m = m + """\multicolumn{1}{|r}{\multirow{2}{*}{\\textbf{%s}}} 
            & \multicolumn{1}{c}{\multirow{2}{*}{\\textbf{SHA}}} 
            & \multicolumn{1}{r|}{\multirow{2}{*}{\\textbf{Mer.pass}}} \\\\
            & & \multicolumn{1}{r|}{} \\\ \n""" %datestr
        else:
            m = m + (" \\textbf{%s} & \\textbf{SHA} & \\textbf{Mer.pass} \\\ \n" %datestr)
        datex = str(ephem.date(date + i))
        p = planetstransit(datex)
        m = m + 'Venus & %s & %s \\\ \n' %(p[0],p[1])
        m = m + 'Mars & %s & %s \\\ \n' %(p[2],p[3])
        m = m + 'Jupiter & %s & %s \\\ \n' %(p[4],p[5])
        m = m + 'Saturn & %s & %s \\\ \n' %(p[6],p[7])
        m = m + '\\hline \n'
    out = out + m

    # returns a table with Horizontal parallax for Venus and Mars
    hp = '\\hline \n'
    hp = hp + '\multicolumn{2}{|r}{\\rule{0pt}{2.6ex}\\textbf{Horizontal parallax}} & \multicolumn{1}{c|}{}\\\ \n'
    hp = hp + '\multicolumn{2}{|r}{Venus:} & \multicolumn{1}{c|}{%s} \\\ \n' %(p[9])
    hp = hp + '\multicolumn{2}{|r}{Mars:} & \multicolumn{1}{c|}{%s} \\\ \n' %(p[8])
    hp = hp + '\\hline \n'
    out = out + hp
    
    out = out + r'\end{tabular*}'
    return out


def sunmoontab(date):
    # generates LaTeX table for sun and moon (traditional style)
    tab = r'''\noindent
    \begin{tabular*}{0.55\textwidth}[t]{@{\extracolsep{\fill}}|c|rr|rrrrr|}
    \multicolumn{1}{c}{\normalsize{h}}& \multicolumn{2}{c}{\normalsize{Sun}} & \multicolumn{5}{c}{\normalsize{Moon}} \\ 
'''
    n = 0
    while n < 3:
        da = date + n
        tab = tab + r'''\hline
    \multicolumn{1}{|c|}{\rule{0pt}{2.6ex}\textbf{%s}} &\multicolumn{1}{c}{\textbf{GHA}} & \multicolumn{1}{c|}{\textbf{Dec}}  & \multicolumn{1}{c}{\textbf{GHA}} & \multicolumn{1}{c}{\textbf{\(\nu\)}} & \multicolumn{1}{c}{\textbf{Dec}} & \multicolumn{1}{c}{\textbf{d}} & \multicolumn{1}{c|}{\textbf{HP}} \\ 
    \hline\rule{0pt}{2.6ex}\noindent
''' %(ephem.date(da).datetime().strftime("%a"))
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
            slastNS = ''
            mlastNS = ''
            while h < 24:
                eph = hourlydata[h]
                if h < 23:
                    nexteph = hourlydata[h+1]
                else:
                    nexteph = hourlydata[23]	# hour 24 = hour 23

                # format declination checking for hemisphere change
                sdec, sNS = NSdeg(eph[1],False,h)
                if sNS != slastNS or math.copysign(1.0,eph[7]) != math.copysign(1.0,nexteph[7]):
                    sdec, sNS = NSdeg(eph[1],False,h,True)	# force N/S
                mdec, mNS = NSdeg(eph[4],False,h)
                if mNS != mlastNS or math.copysign(1.0,eph[8]) != math.copysign(1.0,nexteph[8]):
                    mdec, mNS = NSdeg(eph[4],False,h,True)	# force N/S
                slastNS = sNS
                mlastNS = mNS

                line = "%s & %s & %s & %s & %s & %s & %s & %s" %(h,eph[0],sdec,eph[2],eph[3],mdec,eph[5],eph[6])
                lineterminator = "\\\ \n"
                if h < 23 and (h+1)%6 == 0:
                    lineterminator = "\\\[2Pt] \n"
                tab = tab + line + lineterminator
                h += 1
                da = da + ephem.hour

        else:			# Positive/Negative Declinations
            while h < 24:
                eph = sunmoon(da)
                line = "%s & %s & %s & %s & %s & %s & %s & %s" %(h,eph[0],eph[1],eph[2],eph[3],eph[4],eph[5],eph[6])
                lineterminator = "\\\ \n"
                if h < 23 and (h+1)%6 == 0:
                    lineterminator = "\\\[2Pt] \n"
                tab = tab + line + lineterminator
                h += 1
                da = da + ephem.hour

        vd = vdmean(date + n)
        tab = tab + r"""\hline
    \rule{0pt}{2.4ex} & \multicolumn{1}{c}{SD.=%s} & \multicolumn{1}{c|}{d=%s} & \multicolumn{5}{c|}{S.D.=%s} \\
    \hline
""" %(vd[1],vd[0],vd[2])
        if n < 2:
            # add space between tables...
            tab = tab + r"""\multicolumn{7}{c}{}\\[-1.5ex]"""
        n += 1
    tab = tab+r"""\end{tabular*}"""
    return tab


def sunmoontabm(date):
    # generates LaTeX table for sun and moon (modern style)
    tab = r'''\noindent
    \renewcommand{\arraystretch}{1.1}
    \setlength{\tabcolsep}{4pt}
    \quad\quad
    \begin{tabular}[t]{@{}crrcrrrrr@{}}
    \multicolumn{1}{c}{\normalsize{h}} & 
    \multicolumn{2}{c}{\normalsize{Sun}} & &
    \multicolumn{5}{c}{\normalsize{Moon}} \\ 
    \cmidrule{2-3} \cmidrule{5-9}
'''
    # note: \quad\quad above shifts all tables to the right (still within margins)
    n = 0
    while n < 3:
        da = date + n
        tab = tab + r'''
    \multicolumn{1}{c}{\textbf{%s}} & \multicolumn{1}{c}{\textbf{GHA}} & \multicolumn{1}{c}{\textbf{Dec}} & & \multicolumn{1}{c}{\textbf{GHA}} & \multicolumn{1}{c}{\textbf{\(\nu\)}} & \multicolumn{1}{c}{\textbf{Dec}} & \multicolumn{1}{c}{\textbf{d}} & \multicolumn{1}{c}{\textbf{HP}} \\ 
''' %(ephem.date(da).datetime().strftime("%a"))
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
            slastNS = ''
            mlastNS = ''
            while h < 24:
                eph = hourlydata[h]
                if h < 23:
                    nexteph = hourlydata[h+1]
                else:
                    nexteph = hourlydata[23]	# hour 24 = hour 23
                band = int(h/6)
                group = band % 2

                # format declination checking for hemisphere change
                sdec, sNS = NSdeg(eph[1],True,h)
                if sNS != slastNS or math.copysign(1.0,eph[7]) != math.copysign(1.0,nexteph[7]):
                    sdec, sNS = NSdeg(eph[1],True,h,True)	# force NS
                mdec, mNS = NSdeg(eph[4],True,h)
                if mNS != mlastNS or math.copysign(1.0,eph[8]) != math.copysign(1.0,nexteph[8]):
                    mdec, mNS = NSdeg(eph[4],True,h,True)	# force NS
                slastNS = sNS
                mlastNS = mNS

                line = r'''\color{blue} {%s} & 
''' %(h)
                line = line + "%s & %s && %s & %s & %s & %s & %s \\\ \n" %(eph[0],sdec,eph[2],eph[3],mdec,eph[5],eph[6])

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
                line = r'''\color{blue} {%s} & 
''' %(h)
                line = line + "%s & %s && %s & %s & %s & %s & %s \\\ \n" %(eph[0],eph[1],eph[2],eph[3],eph[4],eph[5],eph[6])
                if group == 1:
                    tab = tab + r'''\rowcolor{LightCyan}
'''
                tab = tab + line
                h += 1
                da = da + ephem.hour

        vd = vdmean(date + n)
        tab = tab + r"""\cmidrule{2-3} \cmidrule{5-9}
        \multicolumn{1}{c}{} & \multicolumn{1}{c}{\footnotesize{SD.=%s}} & 
        \multicolumn{1}{c}{\footnotesize{d=%s}} && \multicolumn{5}{c}{\footnotesize{S.D.=%s}} \\
        \cmidrule{2-3} \cmidrule{5-9}
""" %(vd[1],vd[0],vd[2])
        if n < 2:
            # add space between tables...
            tab = tab + r"""\multicolumn{7}{c}{}\\[-1.5ex]
"""
        n += 1
    tab = tab + r"""
    \end{tabular}
    \quad\quad"""
    return tab


def NSdeg(deg, modern=False, hr=0, forceNS=False):
    # reformat degrees latitude to Ndd°mm.m or Sdd°mm.m
    if deg[0:1] == '-':
        hemisph = "S"
        deg = deg[1:]
    else:
        hemisph = "N"
    if modern:
        if forceNS or hr%6 == 0:
            sdeg = "\\textcolor{blue}{%s}" %hemisph + deg
        else:
            sdeg = deg
    else:
        if forceNS or hr%6 == 0:
            sdeg = "\\textbf{%s}" %hemisph + deg
        else:
            sdeg = deg
    return sdeg, hemisph


def twilighttab(date):
    # returns the twilight and moonrise tables, finally EoT data

# Twilight tables ...........................................
    #lat = [72,70,68,66,64,62,60,58,56,54,52,50,45,40,35,30,20,10,0, -10,-20,-30,-35,-40,-45,-50,-52,-54,-56,-58,-60]
    latNS = [72, 70, 58, 40, 10, -10, -50, -60]
    tab = r'''\begin{tabular*}{0.45\textwidth}[t]{@{\extracolsep{\fill}}|r|ccc|ccc|}
    \multicolumn{7}{c}{\normalsize{}} \\'''

    if config.tbls == "m":
    # The header begins with a thin empty row as top padding; and the top row with
    # bold text has some padding below it. This result gives a balanced impression.
        tab = tab + r"""\hline
    \multicolumn{1}{|c|}{} & & & \multicolumn{1}{|c|}{} & \multicolumn{1}{c|}{} & & \multicolumn{1}{c|}{}\\[-2.0ex]

    \multicolumn{1}{|c|}{\multirow{2}{*}{\textbf{Lat.}}} & 
    \multicolumn{2}{c}{\multirow{1}{*}{\footnotesize{\textbf{Twilight}}}} & 
    \multicolumn{1}{|c|}{\multirow{2}{*}{\textbf{Sunrise}}} & 
    \multicolumn{1}{c|}{\multirow{2}{*}{\textbf{Sunset}}} & 
    \multicolumn{2}{c|}{\multirow{1}{*}{\footnotesize{\textbf{Twilight}}}} \\[0.6ex] 

    \multicolumn{1}{|c|}{} & 
    \multicolumn{1}{c}{Naut.} & 
    \multicolumn{1}{c}{Civil} & 
    \multicolumn{1}{|c|}{} & 
    \multicolumn{1}{c|}{} & 
    \multicolumn{1}{c}{Civil} & 
    \multicolumn{1}{c|}{Naut.}\\ 
    \hline\rule{0pt}{2.6ex}\noindent
"""
    else:
        tab = tab + r"""\hline
    \multicolumn{1}{|c|}{\rule{0pt}{2.4ex}\multirow{2}{*}{\textbf{Lat.}}} & 
    \multicolumn{2}{c}{\textbf{Twilight}} & 
    \multicolumn{1}{|c|}{\multirow{2}{*}{\textbf{Sunrise}}} & 
    \multicolumn{1}{c|}{\multirow{2}{*}{\textbf{Sunset}}} & 
    \multicolumn{2}{c|}{\textbf{Twilight}} \\ 

    \multicolumn{1}{|c|}{} & 
    \multicolumn{1}{c}{Naut.} & 
    \multicolumn{1}{c}{Civil} & 
	\multicolumn{1}{|c|}{} & 
	\multicolumn{1}{c|}{} &
    \multicolumn{1}{c}{Civil} & 
    \multicolumn{1}{c|}{Naut.}\\ 
    \hline\rule{0pt}{2.6ex}\noindent
"""
    lasthemisph = ""
    j = 5
    for i in config.lat:
        if i >= 0:
            hemisph = "N"
        else:
            hemisph = "S"
        if not(i in latNS):
            hs = ""
        else:
            hs = hemisph
            if j%6 == 0:
                tab = tab + r"""\rule{0pt}{2.6ex}
"""
        lasthemisph = hemisph
        twi = twilight(date+1,i)
        line = "\\textbf{%s}" % hs + " " + "%s°" %(abs(i))
        line = line + " & %s & %s & %s & %s & %s & %s \\\ \n" %(twi[0],twi[1],twi[2],twi[4],twi[5],twi[6])
        tab = tab + line
        j += 1
    # add space between tables...
    tab = tab + r"""\hline\multicolumn{7}{c}{}\\[-1.5ex]"""

# Moonrise & Moonset ...........................................
    if config.tbls == "m":
        tab = tab + r"""\hline
    \multicolumn{1}{|c|}{} & & & \multicolumn{1}{c|}{} & & & \multicolumn{1}{c|}{}\\[-2.0ex] 

    \multicolumn{1}{|c|}{\multirow{2}{*}{\textbf{Lat.}}} & 
    \multicolumn{3}{c|}{\multirow{1}{*}{\footnotesize{\textbf{Moonrise}}}} & 
    \multicolumn{3}{c|}{\multirow{1}{*}{\footnotesize{\textbf{Moonset}}}} \\[0.6ex] 
"""
    else:
        tab = tab + r"""\hline
    \multicolumn{1}{|c|}{\rule{0pt}{2.4ex}\multirow{2}{*}{\textbf{Lat.}}} & 
    \multicolumn{3}{c|}{\textbf{Moonrise}} & 
    \multicolumn{3}{c|}{\textbf{Moonset}} \\ 
"""

    weekday = [ephem.date(date).datetime().strftime("%a"),ephem.date(date+1).datetime().strftime("%a"),ephem.date(date+2).datetime().strftime("%a")]
    tab = tab + r"""\multicolumn{1}{|c|}{} & 
    \multicolumn{1}{c}{%s} & 
    \multicolumn{1}{c}{%s} & 
    \multicolumn{1}{c|}{%s} & 
    \multicolumn{1}{c}{%s} & 
    \multicolumn{1}{c}{%s} & 
    \multicolumn{1}{c|}{%s} \\ 
    \hline\rule{0pt}{2.6ex}\noindent
""" %(weekday[0],weekday[1],weekday[2],weekday[0],weekday[1],weekday[2])

    moon = [0,0,0,0,0,0]
    moon2 = [0,0,0,0,0,0]
    lasthemisph = ""
    j = 5
    for i in config.lat:
        if i >= 0:
            hemisph = "N"
        else:
            hemisph = "S"
        if not(i in latNS):
            hs = ""
        else:
            hs = hemisph
            if j%6 == 0:
                tab = tab + r"""\rule{0pt}{2.6ex}
"""
        lasthemisph = hemisph
        moon, moon2 = moonrise(date,i)
        if not(double_events_found(moon,moon2)):
            tab = tab + "\\textbf{%s}" % hs + " " + "%s°" %(abs(i))
            tab = tab + " & %s & %s & %s & %s & %s & %s \\\ \n" %(moon[0],moon[1],moon[2],moon[3],moon[4],moon[5])
        else:
# print a row with two moonrise/moonset events on the same day & latitude
            tab = tab + r"""\multirow{2}{*}{\textbf{%s} %s°}""" %(hs,abs(i))
# top row...
            for k in range(len(moon)):
                if moon2[k] != '--:--':
                    tab = tab + r""" & %s""" %(moon[k])
                else:
                    tab = tab + r""" & \multirow{2}{*}{%s}""" %(moon[k])
            tab = tab + r"""\\"""	# terminate top row
# bottom row...
            for k in range(len(moon)):
                if moon2[k] != '--:--':
                    tab = tab + r""" & %s""" %(moon2[k])
                else:
                    tab = tab + r"""&"""
            tab = tab + r"""\\"""	# terminate bottom row
        j += 1
    # add space between tables...
    tab = tab + r"""\hline\multicolumn{7}{c}{}\\[-1.5ex]"""

# Equation of Time section ...........................................
    if config.tbls == "m":
        tab = tab + r"""\hline
    \multicolumn{1}{|c|}{} & & & \multicolumn{1}{c|}{} & & & \multicolumn{1}{c|}{}\\[-2.0ex]

    \multicolumn{1}{|c|}{\multirow{4}{*}{\footnotesize{\textbf{Day}}}} & 
    \multicolumn{3}{c|}{\multirow{1}{*}{\footnotesize{\textbf{Sun}}}} & 
    \multicolumn{3}{c|}{\multirow{1}{*}{\footnotesize{\textbf{Moon}}}} \\[0.6ex] 

    \multicolumn{1}{|c|}{} & 
    \multicolumn{2}{c}{Eqn.of Time} & 
    \multicolumn{1}{|c|}{Mer.} & 
    \multicolumn{2}{c}{Mer.Pass.} & 
    \multicolumn{1}{|c|}{} \\ 

    \multicolumn{1}{|c|}{} &\multicolumn{1}{c}{00\textsuperscript{h}} & \multicolumn{1}{c}{12\textsuperscript{h}} & \multicolumn{1}{|c|}{Pass} & \multicolumn{1}{c}{Upper} & \multicolumn{1}{c}{Lower} &\multicolumn{1}{|c|}{Age} \\ 

    \multicolumn{1}{|c|}{} &\multicolumn{1}{c}{mm:ss} & \multicolumn{1}{c}{mm:ss} & \multicolumn{1}{|c|}{hh:mm} & \multicolumn{1}{c}{hh:mm} & \multicolumn{1}{c}{hh:mm} &\multicolumn{1}{|c|}{} \\ 
    \hline\rule{0pt}{3.0ex}\noindent
"""
    else:
        tab = tab + r"""\hline
    \multicolumn{1}{|c|}{\rule{0pt}{2.4ex}\multirow{4}{*}{\textbf{Day}}} & 
	\multicolumn{3}{c|}{\textbf{Sun}} & \multicolumn{3}{c|}{\textbf{Moon}} \\ 

    \multicolumn{1}{|c|}{} & \multicolumn{2}{c}{Eqn.of Time} & \multicolumn{1}{|c|}{Mer.} & \multicolumn{2}{c}{Mer.Pass.} & \multicolumn{1}{|c|}{} \\ 

    \multicolumn{1}{|c|}{} & \multicolumn{1}{c}{00\textsuperscript{h}} & \multicolumn{1}{c}{12\textsuperscript{h}} & \multicolumn{1}{|c|}{Pass} & \multicolumn{1}{c}{Upper} & \multicolumn{1}{c}{Lower} &\multicolumn{1}{|c|}{Age} \\

    \multicolumn{1}{|c|}{} & \multicolumn{1}{c}{mm:ss} & \multicolumn{1}{c}{mm:ss} & \multicolumn{1}{|c|}{hh:mm} & \multicolumn{1}{c}{hh:mm} & \multicolumn{1}{c}{hh:mm} &\multicolumn{1}{|c|}{} \\
    \hline\rule{0pt}{3.0ex}\noindent
"""

    for k in range(3):
        d = ephem.date(date+k)
        eq = equation_of_time(d)
        if k == 2:
            tab = tab + "%s & %s & %s & %s & %s & %s & %s(%s\\%%) \\\[0.3ex] \n" %(d.datetime().strftime("%d"),eq[0],eq[1],eq[2],eq[3],eq[4],eq[5],eq[6])
        else:
            tab = tab + "%s & %s & %s & %s & %s & %s & %s(%s\\%%) \\\ \n" %(d.datetime().strftime("%d"),eq[0],eq[1],eq[2],eq[3],eq[4],eq[5],eq[6])
    tab = tab + r"""\hline
    \end{tabular*}
"""
    return tab


def double_events_found(m1, m2):
    # check for two moonrise/moonset events on the same day & latitude
    dbl = False
    for i in range(len(m1)):
        if m2[i] != '--:--':
            dbl = True
    return dbl


def doublepage(date):
    # creates a doublepage (3 days) of the nautical almanac
    page = r"""
    \sffamily
    \noindent
    \textbf{%s, %s, %s   (%s.,  %s.,  %s.)}
    
    \begin{scriptsize}
""" %(ephem.date(date).datetime().strftime("%B %d"),ephem.date(date+1).datetime().strftime("%d"),ephem.date(date+2).datetime().strftime("%d"),ephem.date(date).datetime().strftime("%a"),ephem.date(date+1).datetime().strftime("%a"),ephem.date(date+2).datetime().strftime("%a"))
    if config.tbls == "m":
        page = page + planetstabm(date)
    else:
        page = page + planetstab(date)
    page = page + starstab(date)
    str1 = r"""\end{scriptsize}

    \newpage
    \begin{flushright}
    \textbf{%s to %s}
    \end{flushright}
    
    \begin{scriptsize}
""" %(ephem.date(date).datetime().strftime("%Y %B %d"),ephem.date(date+2).datetime().strftime("%b. %d"))
    page = page + str1
    if config.tbls == "m":
        page = page + sunmoontabm(date)
    else:
        page = page + sunmoontab(date)
    page = page + twilighttab(date)
    page = page + r"""\end{scriptsize}

    \newpage
"""
    return page
    
    
def pages(date, p):
    # make 'p' doublepages beginning with date
    d = ephem.date(date)
    out = ''
    for i in range(p):
        out = out + doublepage(d)
        d = d + 3
    return out
    
    
def almanac(first_day, pagenum):
    # make almanac from date till date
    year = first_day.year
    mth = first_day.month
    day = first_day.day

    alm = r"""\documentclass[10pt, twoside, a4paper]{report}
    \usepackage[utf8x]{inputenc}
    \usepackage[english]{babel}
    \usepackage{fontenc}
"""
    if config.tbls == "m":
        alm = alm + r"""
    \usepackage[ top=10mm, bottom=18mm, left=12mm, right=10mm ]{geometry}
    \usepackage[table]{xcolor}
    \definecolor{LightCyan}{rgb}{0.88,1,1}
    \usepackage{booktabs}
    \usepackage{multirow}
"""
    else:
        alm = alm + r"""
    \usepackage[ top=21mm, bottom=21mm, left=12mm, right=8mm]{geometry}
    \usepackage{multirow}
"""

    alm = alm + r"""
    \newcommand{\HRule}{\rule{\linewidth}{0.5mm}}
    \usepackage[pdftex]{graphicx}	% for \includegraphics

    \begin{document}

    \begin{titlepage}
"""
    if config.tbls == "m":
        alm = alm + r'''\vspace*{2cm}'''

    alm = alm + r"""
    \begin{center}
     
    \textsc{\Large Generated by PyAlmanac}\\[1.5cm]

    \includegraphics[width=0.45\textwidth]{./Sky-large}\\[1cm]

    \textsc{\huge The Nautical Almanac}\\[0.7cm]
"""
    if pagenum == 122:
        alm = alm + r"""
        \HRule \\[0.6cm]
        { \Huge \bfseries %s}\\[0.4cm]
        \HRule \\[1.5cm]
""" %(year)
    else:
        alm = alm + r"""
        \HRule \\[0.6cm]
        { \Huge \bfseries from %s.%s.%s}\\[0.4cm]
        \HRule \\[1.5cm]
""" %(day,mth,year)

    if config.tbls == "m":
        alm = alm + r"""
        \begin{center} \large
        \emph{Author:}\\
        Enno \textsc{Rodegerdts}\\[6Pt]
        \emph{Table Design:}\\
        Andrew \textsc{Bauer}
"""
    else:
        alm = alm + r"""
        \begin{center} \large
        \emph{Author:}\\
        Enno \textsc{Rodegerdts}\\
"""

    alm = alm + r"""\end{center}

    \vfill

    {\large \today}
    \HRule \\[0.6cm]
    \end{center}
    
    \begin{description}\footnotesize
    
    \item[Disclaimer:] These are computer generated tables. Use on your own risk. 
    The accuracy has been checked as good as possible but can not be guaranteed. 
    This means, if you get lost on the oceans because of errors in this publication I can not be held liable. 
    For security relevant applications you should buy an official version of the nautical almanac. You need one anyway since this publication only contains the daily pages of the Nautical Almanac.
    
    \end{description}
    
    \end{titlepage}
"""
    first_day = r"""%s/%s/%s""" %(year,mth,day)
    y = ephem.Date(first_day)
    #y = ephem.date(str(year))
    alm = alm + pages(y,pagenum)
    alm = alm + '\end{document}'
    return alm

