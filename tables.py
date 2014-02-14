#! /usr/bin/python
# -*- coding: utf-8 -*-

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

#import ephem
#import math
from alma_ephem import *


def planetstab(date):
    """generates a latex table for the navigational plantets"""
    tab = r'''\noindent
    \begin{tabular*}{0.75\textwidth}[t]{@{\extracolsep{\fill}}|c|r|rr|rr|rr|rr|}
    \multicolumn{1}{c}{\normalsize{}} & \multicolumn{1}{c}{\normalsize{Aries}} &  \multicolumn{2}{c}{\normalsize{Venus}}& \multicolumn{2}{c}{\normalsize{Mars}} & \multicolumn{2}{c}{\normalsize{Jupiter}} & \multicolumn{2}{c}{\normalsize{Saturn}}\\ 
    '''
    d = 0
    while d < 3:
        da = date+d
        tab = tab + r'''\hline
        \hline
        \textbf{%s} & \multicolumn{1}{c|}{\textbf{GHA}} & \multicolumn{1}{c}{\textbf{GHA}} & \multicolumn{1}{c|}{\textbf{Dec}} & \multicolumn{1}{c}{\textbf{GHA}} & \multicolumn{1}{c|}{\textbf{Dec}}& \multicolumn{1}{c}{\textbf{GHA}} & \multicolumn{1}{c|}{\textbf{Dec}}& \multicolumn{1}{c}{\textbf{GHA}} & \multicolumn{1}{c|}{\textbf{Dec}} \\ 
        \hline 
        ''' %(ephem.date(da).datetime().strftime("%a"))
        h = 0
        while h < 24:
            eph = planets(da)
            line = "%s & %s & %s & %s & %s & %s & %s & %s & %s & %s\\\ \n" %(h,eph[0],eph[1],eph[2],eph[3],eph[4],eph[5],eph[6],eph[7],eph[8])
            tab = tab + line
            h += 1
            da = da+ephem.hour
        vd = vdmean(date+d)
        tab = tab + r"""\hline 
        \multicolumn{2}{|c|}{Mer.pass.:%s}&  \multicolumn{2}{c|}{v%s d%s m%s}& \multicolumn{2}{c|}{v%s d%s m%s} & \multicolumn{2}{c|}{v%s d%s m%s} & \multicolumn{2}{c|}{v%s d%s m%s}\\ 
        \hline
        \multicolumn{10}{c}{}\\
        """ %(ariestransit(date+d),vd[3],vd[4],vd[5],vd[6],vd[7],vd[8],vd[9],vd[10],vd[11],vd[12],vd[13],vd[14])
        d = d + 1
    tab = tab+r"""\end{tabular*}
    """
    return tab

def starstab(date):
    """returns a table with ephemerieds for the navigational stars
    """
    out = r"""\begin{tabular*}{0.25\textwidth}[t]{@{\extracolsep{\fill}}|rrr|}
    \multicolumn{3}{c}{\normalsize{Stars}}  \\ 
    \hline
    \hline
    & \multicolumn{1}{c}{SHA} & \multicolumn{1}{c|}{Dec} \\ 
    \hline
    """
    stars = stellar(date+1)
    for i in range(len(stars)):
        out = out + r"""%s & %s & %s \\""" %(stars[i][0],stars[i][1],stars[i][2])
        out = out + '\n'
    m = '\\hline\n'
    for i in range(3):
        datex = str(ephem.date(date + i))
        m = m + '\\hline \n'
        m = m + ' %s & SHA & Mer.pass \\\ \n' %datex[0:8]
        p = planetstransit(datex)
        m = m + 'Venus & %s & %s \\\ \n' %(p[0],p[1])
        m = m + 'Mars & %s & %s \\\ \n' %(p[2],p[3])
        m = m + 'Jupiter & %s & %s \\\ \n' %(p[4],p[5])
        m = m + 'Saturn & %s & %s \\\ \n' %(p[6],p[7])
        m = m + '\\hline \n'
    out = out + m
    out = out + r'\end{tabular*}'
    return out

def sunmoontab(date):
    """generates LaTeX table for sun and moon
    """
    tab = r'''\noindent
    \begin{tabular*}{0.55\textwidth}[t]{@{\extracolsep{\fill}}|c|rr|rrrrr|}
    \multicolumn{1}{c}{\normalsize{h}}& \multicolumn{2}{c}{\normalsize{Sun}} & \multicolumn{5}{c}{\normalsize{Moon}} \\ 
    '''
    d = 0
    while d < 3:
        tab = tab + r'''\hline 
        \hline 
        \multicolumn{1}{|c|}{\textbf{%s}} &\multicolumn{1}{c}{\textbf{GHA}} & \multicolumn{1}{c|}{\textbf{Dec}}  & \multicolumn{1}{c}{\textbf{GHA}} & \multicolumn{1}{c}{\textbf{\(\nu\)}} & \multicolumn{1}{c}{\textbf{Dec}} & \multicolumn{1}{c}{\textbf{d}} & \multicolumn{1}{c|}{\textbf{HP}} \\ 
        \hline
        ''' %(ephem.date(date+d).datetime().strftime("%a"))
        da = date+d
        h = 0
        while h < 24:
            eph = sunmoon(da)
            line = "%s & %s & %s & %s & %s & %s & %s & %s \\\ \n" %(h,eph[0],eph[1],eph[2],eph[3],eph[4],eph[5],eph[6])
            tab = tab + line
            h += 1
            da = da+ephem.hour
        vd = vdmean(date+d)
        tab = tab + r"""\hline
        & \multicolumn{1}{c}{SD.=%s} & \multicolumn{1}{c|}{d=%s} & \multicolumn{5}{c|}{S.D.=%s} \\
        \hline
        \multicolumn{7}{c}{}\\
        """ %(vd[0],vd[1],vd[2])
        d = d + 1
    tab = tab+r"""\end{tabular*}"""
    return tab
    
def twilighttab(date):
    """returns the twilight and moonristables"""
    lat = [72,70,68,66,64,62,60,58,56,54,52,50,45,40,35,30,20,10,0,-10,-20,-30,-35,-40,-45,-50,-52,-54,-56,-58,-60]
    tab = r'''\begin{tabular*}{0.45\textwidth}[t]{@{\extracolsep{\fill}}|c|ccc|ccc|}
    \multicolumn{7}{c}{\normalsize{}} \\
    \hline
    \hline
    \multicolumn{1}{|c|}{} & \multicolumn{2}{c}{\textbf{Twilight}} & \multicolumn{1}{c|}{} & \multicolumn{1}{c}{} & \multicolumn{2}{c|}{\textbf{Twilight}} \\ 
    \multicolumn{1}{|c|}{\textbf{Lat.}} &\multicolumn{1}{c}{Naut.} & \multicolumn{1}{c}{Civil} & \multicolumn{1}{c|}{Sunrise} & \multicolumn{1}{c}{Sunset} & \multicolumn{1}{c}{Civil} &\multicolumn{1}{c|}{Naut.}\\ 
    \hline
    '''
    for i in lat:
        twi = twilight(date+1,i)
        line = "%s & %s & %s & %s & %s & %s & %s \\\ \n" %(i,twi[0],twi[1],twi[2],twi[4],twi[5],twi[6])
        tab = tab+line
    weekday = [ephem.date(date).datetime().strftime("%a"),ephem.date(date+1).datetime().strftime("%a"),ephem.date(date+2).datetime().strftime("%a")]
    tab = tab + r"""\hline
    \multicolumn{7}{c}{}\\
    \hline
    \hline
    \multicolumn{1}{|c|}{} & \multicolumn{3}{c|}{\textbf{Moonrise}}  & \multicolumn{3}{c|}{\textbf{Moonset}} \\ 
    \multicolumn{1}{|c|}{\textbf{Lat.}} &\multicolumn{1}{c}{%s} & \multicolumn{1}{c}{%s} & \multicolumn{1}{c|}{%s} & \multicolumn{1}{c}{%s} & \multicolumn{1}{c}{%s} &\multicolumn{1}{c|}{%s} \\ 
    \hline
    """ %(weekday[0],weekday[1],weekday[2],weekday[0],weekday[1],weekday[2],)
    moon = [0,0,0,0,0,0]
    for j in lat:
        moon = moonrise(date,j)
        tab=tab+"%s & %s & %s & %s & %s & %s & %s \\\ \n" %(j,moon[0],moon[1],moon[2],moon[3],moon[4],moon[5])
    tab = tab + r"""\hline
    \multicolumn{7}{c}{}\\
    \hline
    \hline
    \multicolumn{1}{|c|}{} & \multicolumn{3}{c|}{\textbf{Sun}}  & \multicolumn{3}{c|}{\textbf{Moon}} \\ 
    \multicolumn{1}{|c|}{\textbf{Day}} &\multicolumn{2}{c}{Eqn.of Time} & \multicolumn{1}{c|}{Mer.} & \multicolumn{2}{c}{Mer.Pass.} & \multicolumn{1}{c|}{Age} \\ 
    \multicolumn{1}{|c|}{} &\multicolumn{1}{c}{00\textsuperscript{h}} & \multicolumn{1}{c}{12\textsuperscript{h}} & \multicolumn{1}{c|}{Pass} & \multicolumn{1}{c}{Upper} & \multicolumn{1}{c}{Lower} &\multicolumn{1}{c|}{} \\ 
    \hline
    """
    for k in range(3):
        d = ephem.date(date+k)
        eq = equation_of_time(d)
        tab = tab + "%s & %s & %s & %s & %s & %s & %s(%s\\%%) \\\ \n" %(d.tuple()[2],eq[0],eq[1],eq[2],eq[3],eq[4],eq[5],eq[6])
    tab = tab + r"""\hline
    \end{tabular*}
    """
    return tab

def dobblepage(date):
    """creates a dobblepage(3 days) of the nautical almanac
    """
    page = r"""\sffamily
    \noindent
    \textbf{%s, %s ,%s   (%s.,  %s.,  %s.)}
    
    \begin{scriptsize}
    """ %(ephem.date(date).datetime().strftime("%B %d"),ephem.date(date+1).datetime().strftime("%d"),ephem.date(date+2).datetime().strftime("%d"),ephem.date(date).datetime().strftime("%a"),ephem.date(date+1).datetime().strftime("%a"),ephem.date(date+2).datetime().strftime("%a"))
    page = page + planetstab(date)
    page = page + starstab(date)
    page = page + r""" \end{scriptsize}
    \newpage
    
    
    
    \begin{flushright}
    \textbf{%s to %s}
    \end{flushright}
    
    \begin{scriptsize}
    """ %(ephem.date(date).datetime().strftime("%Y %B %d"),ephem.date(date+2).datetime().strftime("%b. %d"))
    page = page + sunmoontab(date)
    page = page + twilighttab(date)
    page = page + r"""\end{scriptsize}
    \newpage
    
    
    
    """
    return page
    
    
def pages(date,p):
    """make i dobblepages beginning with date"""
    d = ephem.date(date)
    out = ''
    for i in range(p):
        out = out + dobblepage(d)
        d = d +3
    return out
        
def almanac(year):
    """make almanak from date til date"""
    alm = r"""\documentclass[10pt, twoside, a4paper]{report}
    \usepackage[utf8x]{inputenc}
    \usepackage[english]{babel}
    \usepackage{fontenc}
    \usepackage[ top=25mm, bottom=25mm, left=18mm, right=8mm]{geometry}

    \newcommand{\HRule}{\rule{\linewidth}{0.5mm}}
    \usepackage[pdftex]{graphicx}

    \begin{document}

    \begin{titlepage}
     
    \begin{center}
     
    \textsc{\Large Generated by PyAlmanac}\\[1.5cm]

    \includegraphics[width=0.4\textwidth]{./Navigational-stars-north}\\[1cm]

     
    \textsc{\huge The Nautical Almanac}\\[0.7cm]
     
    \HRule \\[0.6cm]
    { \Huge \bfseries %s}\\[0.4cm]
     
    \HRule \\[1.5cm]
     
    \begin{center} \large
    \emph{Author:}\\
    Enno \textsc{Rodegerdts}
    \end{center}


     
    \vfill
     
    {\large \today}
    \HRule \\[0.6cm]
    \end{center}
    
    \begin{description}\tiny
    
	\item[Disclaimer:] These are computer generated tables. Use on your own risk. 
    The accuracy has been checked as good as possible but can not be guaranteed. 
    This means, if you get lost on the oceans because of errors in this publication I can not be held liable. 
    For security relevant applications you should buy an official version of the nautical almanac. You need one anyway since this publication only contains the daily pages of the Nautical Almanac
	
	\end{description}
     
     
    \end{titlepage}""" %(year)
    y = ephem.date(str(year))
    alm = alm + pages(y,122)
    alm = alm + '\end{document}'
    return alm

