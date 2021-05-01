#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright (C) 2021  Andrew Bauer

#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
# 
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
# 
#   You should have received a copy of the GNU General Public License along
#   with this program.  If not, see <https://www.gnu.org/licenses/>.

# NOTE: the new format statement requires a literal '{' to be entered as '{{',
#       and a literal '}' to be entered as '}}'. The old '%' format specifier
#       will be removed from Python at some later time. See:
# https://docs.python.org/3/whatsnew/3.0.html#pep-3101-a-new-approach-to-string-formatting

# Third party imports
import ephem

# Local application imports
from alma_ephem import *
import config


def double_events_found(m1, m2):
    # check for two moonrise/moonset events on the same day & latitude
    dbl = False
    for i in range(len(m1)):
        if m2[i] != '--:--':
            dbl = True
    return dbl


def twilighttab(date):
    # returns the twilight and moonrise tables

# Twilight tables ...........................................
    #lat = [72,70,68,66,64,62,60,58,56,54,52,50,45,40,35,30,20,10,0, -10,-20,-30,-35,-40,-45,-50,-52,-54,-56,-58,-60]
    latNS = [72, 70, 58, 40, 10, -10, -50, -60]
#    tab = r'''\begin{tabular*}{0.72\textwidth}[t]{@{\extracolsep{\fill}}|r|ccc|ccc|cc|}
    tab = r'''\begin{tabular}[t]{|r|ccc|ccc|cc|}
%%%\multicolumn{9}{c}{\normalsize{}}\\
'''

    ondate = ephem.date(date).datetime().strftime("%d %B %Y")
    tab = tab + r'''\hline
\multicolumn{{9}}{{|c|}}{{\rule{{0pt}}{{2.4ex}}{{\textbf{{{}}}}}}}\\
'''.format(ondate)

    tab = tab + r'''\hline
\multicolumn{1}{|c|}{\rule{0pt}{2.4ex}\multirow{2}{*}{\textbf{Lat.}}} & 
\multicolumn{2}{c}{\textbf{Twilight}} & 
\multicolumn{1}{|c|}{\multirow{2}{*}{\textbf{Sunrise}}} & 
\multicolumn{1}{c|}{\multirow{2}{*}{\textbf{Sunset}}} & 
\multicolumn{2}{c|}{\textbf{Twilight}} & 
\multicolumn{1}{c|}{\multirow{2}{*}{\textbf{Moonrise}}} & 
\multicolumn{1}{c|}{\multirow{2}{*}{\textbf{Moonset}}}\\
\multicolumn{1}{|c|}{} & 
\multicolumn{1}{c}{Naut.} & 
\multicolumn{1}{c}{Civil} & 
\multicolumn{1}{|c|}{} & 
\multicolumn{1}{c|}{} & 
\multicolumn{1}{c}{Civil} & 
\multicolumn{1}{c|}{Naut.} & 
\multicolumn{1}{c|}{} & 
\multicolumn{1}{c|}{}\\
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
        twi = twilight(date, i, hemisph, True)      # True = round to seconds
        moon, moon2 = moonrise_set2(date,i)
        if not(double_events_found(moon,moon2)):
            line = r'''\textbf{{{}}}'''.format(hs) + r''' {}$^\circ$'''.format(abs(i))
            line = line + r''' & {} & {} & {} & {} & {} & {} & {} & {} \\
'''.format(twi[0],twi[1],twi[2],twi[4],twi[5],twi[6],moon[0],moon[1])
        else:
            # print a row with two moonrise/moonset events on the same day & latitude
            line = r'''\multirow{{2}}{{*}}{{\textbf{{{}}} {}$^\circ$}}'''.format(hs,abs(i))
            line = line + r''' & \multirow{{2}}{{*}}{{{}}}'''.format(twi[0])
            line = line + r''' & \multirow{{2}}{{*}}{{{}}}'''.format(twi[1])
            line = line + r''' & \multirow{{2}}{{*}}{{{}}}'''.format(twi[2])
            line = line + r''' & \multirow{{2}}{{*}}{{{}}}'''.format(twi[4])
            line = line + r''' & \multirow{{2}}{{*}}{{{}}}'''.format(twi[5])
            line = line + r''' & \multirow{{2}}{{*}}{{{}}}'''.format(twi[6])

# top row...
            for k in range(len(moon)):
                if moon2[k] != '--:--':
                    line = line + r''' & \colorbox{{khaki!45}}{{{}}}'''.format(moon[k])
                else:
                    line = line + r''' & \multirow{{2}}{{*}}{{{}}}'''.format(moon[k])
            line = line + r'''\\
'''	# terminate top row
# bottom row...
            line = line + r'''& & & & & & '''
            for k in range(len(moon)):
                if moon2[k] != '--:--':
                    line = line + r''' & \colorbox{{khaki!45}}{{{}}}'''.format(moon2[k])
                else:
                    line = line + r'''&'''
            line = line + r''' \\
'''	# terminate bottom row

        tab = tab + line
        j += 1
    # add space between tables...
    tab = tab + r'''\hline\multicolumn{9}{c}{}\\
'''
    tab = tab + r'''\end{tabular}
'''
    return tab


def meridiantab(date):
    # returns a table with ephemerieds for the navigational stars
    # LaTeX SPACING: \enskip \quad \qquad
    out = r'''\quad
\begin{tabular*}{0.25\textwidth}[t]{@{\extracolsep{\fill}}|rrr|}
%%%\multicolumn{3}{c}{\normalsize{}}\\
'''
    m = ""
    # returns a table with SHA & Mer.pass for Venus, Mars, Jupiter and Saturn
    dt = ephem.date(date).datetime()
    datestr = r'''{} {}'''.format(dt.strftime("%b"), dt.strftime("%d"))
#        datestr = r'''{} {} {}'''.format(dt.strftime("%b"), dt.strftime("%d"), dt.strftime("%a"))
    m = m + r'''\hline
& & \multicolumn{{1}}{{r|}}{{}}\\[-2.0ex]
\textbf{{{}}} & \textbf{{SHA}} & \textbf{{Mer.pass}}\\
\hline\multicolumn{{3}}{{|r|}}{{}}\\[-2.0ex]
'''.format(datestr)
    p = planetstransit(date, True)      # True = round to seconds
    m = m + r'''Venus & {} & {} \\
'''.format(p[0],p[1])
    m = m + r'''Mars & {} & {} \\
'''.format(p[2],p[3])
    m = m + r'''Jupiter & {} & {} \\
'''.format(p[4],p[5])
    m = m + r'''Saturn & {} & {} \\
'''.format(p[6],p[7])
    m = m + r'''\hline\multicolumn{3}{c}{}\\
'''
    out = out + m

    out = out + r'''\end{tabular*}
\par    % put next table below here
'''
    return out


def equationtab(date):
    # returns the Equation of Time section for 'date' and 'date+1'

    tab = r'''\begin{tabular}[t]{|r|ccc|ccc|}
%\multicolumn{7}{c}{\normalsize{}}\\
\cline{1-7}
\multicolumn{1}{|c|}{\rule{0pt}{2.4ex}\multirow{4}{*}{\textbf{Day}}} & 
\multicolumn{3}{c|}{\textbf{Sun}} & \multicolumn{3}{c|}{\textbf{Moon}}\\
\multicolumn{1}{|c|}{} & \multicolumn{2}{c}{Eqn.of Time} & \multicolumn{1}{|c|}{Mer.} & \multicolumn{2}{c}{Mer.Pass.} & \multicolumn{1}{|c|}{}\\
\multicolumn{1}{|c|}{} & \multicolumn{1}{c}{00\textsuperscript{h}} & \multicolumn{1}{c}{12\textsuperscript{h}} & \multicolumn{1}{|c|}{Pass} & \multicolumn{1}{c}{Upper} & \multicolumn{1}{c}{Lower} &\multicolumn{1}{|c|}{Age}\\
\multicolumn{1}{|c|}{} & \multicolumn{1}{c}{mm:ss} & \multicolumn{1}{c}{mm:ss} & \multicolumn{1}{|c|}{hh:mm:ss} & \multicolumn{1}{c}{hh:mm:ss} & \multicolumn{1}{c}{hh:mm:ss} &\multicolumn{1}{|c|}{}\\
\cline{1-7}\rule{0pt}{3.0ex}\noindent
'''

    for k in range(2):
        d = ephem.date(date+k)
        eq = equation_of_time(d, True)      # True = round to seconds
        tab = tab + r'''{} & {} & {} & {} & {} & {} & {}({}\%) \\
'''.format(d.datetime().strftime("%d"),eq[0],eq[1],eq[2],eq[3],eq[4],eq[5],eq[6])

    tab = tab + r'''\cline{1-7}
\end{tabular}'''
    return tab


def doublepage(date, page1):
    # creates a doublepage (2 days) of tables
    page = ''

    leftindent = ""
    rightindent = ""
    str1 = r'''
% ------------------ N E W   P A G E ------------------
\newpage
\sffamily
\noindent
\begin{{flushright}}
\textbf{{{} to {}}}{}%
\end{{flushright}}\par
\begin{{scriptsize}}
'''.format(ephem.date(date).datetime().strftime("%Y %B %d"),ephem.date(date+1).datetime().strftime("%b. %d"),rightindent)
    page = page + str1

    page = page + twilighttab(date)
    page = page + meridiantab(date)
    page = page + twilighttab(date+1)
    page = page + meridiantab(date+1)
    page = page + equationtab(date)
    page = page + r'''

\end{scriptsize}'''
    # to avoid "Overfull \hbox" messages, leave a paragraph end before the end of a size change. (See lines above)
    return page


def pages(date, p):
    # make 'p' doublepages beginning with date
    out = ''
    page1 = True
    for i in range(p):
        out = out + doublepage(date,page1)
        page1 = False
        date += 2
    return out


def maketables(first_day, pagenum):
    # make tables starting from first_day
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
        lm = "16mm"
        rm = "16mm"
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

    alm = r'''\documentclass[10pt, twoside, {}]{{report}}'''.format(paper)

    alm = alm + r'''
%\usepackage[utf8]{inputenc}
\usepackage[english]{babel}
\usepackage{fontenc}'''

    # to troubleshoot add "showframe, verbose," below:
    alm = alm + r'''
\usepackage[nomarginpar, top={}, bottom={}, left={}, right={}]{{geometry}}'''.format(tm,bm,lm,rm)

    # Note: \DeclareUnicodeCharacter is not compatible with some versions of pdflatex
    alm = alm + r'''
\usepackage{xcolor}  % highlight double moon events on same day
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

    alm = alm + r'''
% for the title page only...
\newgeometry{{nomarginpar, top={}, bottom={}, left={}, right={}}}'''.format(tm1,bm1,lm1,rm1)

    alm = alm + r'''
    \begin{titlepage}
    \begin{center}
    \textsc{\Large Generated using Ephem}\\[0.7cm]
    % TRIM values: left bottom right top
    \includegraphics[clip, trim=5mm 8cm 5mm 21mm, width=0.8\textwidth]{./A4chartNorth_P.pdf}\\'''

    alm = alm + r'''[{}]
    \textsc{{\huge Event Time Tables}}\\[{}]'''.format(vsep1,vsep2)

    if pagenum == 183:
        alm = alm + r'''
    \HRule \\[0.5cm]
    {{ \Huge \bfseries {}}}\\[0.2cm]
    \HRule \\'''.format(year)
    else:
        alm = alm + r'''
    \HRule \\[0.5cm]
    {{ \Huge \bfseries from {}.{}.{}}}\\[0.2cm]
    \HRule \\'''.format(day,mth,year)

    alm = alm + r'''
    \begin{center}\begin{tabular}[t]{rl}
    \large\emph{Author:} & \large Andrew \textsc{Bauer}\\
    \end{tabular}\end{center}'''

    alm = alm + r'''
    {\large \today}
    \HRule \\[0.2cm]
    \end{center}
    \begin{description}\footnotesize
    \item[Disclaimer:] These are computer generated tables. They focus on times of rising and setting events and are rounded to the second... primarily intended for comparison with other astronomical algorithms (not for navigation). Meridian Passage times of the sun, moon and four planets are included.
    \end{description}
\end{titlepage}
\restoregeometry    % so it does not affect the rest of the pages'''

    first_day = r'''{}/{}/{}'''.format(year,mth,day)
    date = ephem.Date(first_day)    # date to float
    alm = alm + pages(date,pagenum)
    alm = alm + '''
\end{document}'''
    return alm