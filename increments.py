#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#   Copyright (C) 2014  Enno Rodegerdts

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
from math import pi as pi
from math import cos as cos
from math import tan as tan
from math import sqrt as sqrt

def degmin(deg):
    #changes decimal degrees to the format usually used in the nautical almanac. (ddd°mm.m')
    theminus = ""
    if deg < 0:
        theminus = "-"
    deg = abs(deg)
    di = int(deg)		# degrees (integer)
    # note: round() uses "Rounding Half To Even" strategy
    mf = round((deg-di)*60, 1)	# minutes (float), rounded to 1 decimal place
    mi = int(mf)			# minutes (integer)
    if mi == 60:
        mf -= 60
        di += 1
        if di == 360:
            di = 0
    gm = "{}{}$^\circ${:04.1f}".format(theminus,di,mf)
    return gm

def decdeg(d,min):
	# returns decimal degrees from deg. and min.
	d=d*1.0
	min=min*1.0
	deg=d+(min/60)
	return deg
	
def rad(d,min):
	#returns radiands from deg. and min.
	rad=decdeg(d,min)/180*pi
	return rad

def suninc(m,s):
	# returns the increment for the sun.
	min=m*1.0
	sec=s/60.0
	hour=(sec+min)/60
	inc=degmin(15*hour)
	return inc

def ariesinc(m,s):
	# returns the increment for aries
	min= m*1.0
	sec=s/60.0
	hour=(sec+min)/60
	inc=degmin(decdeg(15,2.46)*hour)
	return inc

def mooninc(m,s):
	# returns the increment for the Moon
	min= m*1.0
	sec=s/60.0
	hour=(sec+min)/60
	inc=degmin(decdeg(14,19.0)*hour)
	return inc
	
def vcorr(m,v):
	# returns the v correction for a given minute and tabular v.
	h=(m+0.5)/60.0
	corr=round(v*h,1)
	return corr

def inctab(min):
    """generates a latex table for increments"""
    tab = r'''\noindent
    \begin{tabular*}{0.33\textwidth}[t]{@{\extracolsep{\fill}}|>{\bfseries}p{0.3cm}|>{\hspace{-3pt}}r|>{\hspace{-3pt}}r|>{\hspace{-3pt}}r||>{\hspace{-3pt}}c>{\hspace{-3pt}}c>{\hspace{-3pt}}c<{\hspace{-3pt}}|}
    \hline
    {\tiny m} \textbf{'''
    
    tab = tab+"{}".format(int(min))
    
    tab=tab+ r'''} & \multicolumn{1}{p{0.5cm}|}{\textbf{Sun Plan.}} & \multicolumn{1}{c|}{\textbf{Aries}} & \multicolumn{1}{c||}{\textbf{Moon}} & \multicolumn{3}{c|}{\textit{\textbf{v and d corr}}}\\ 
    \hline'''
   
    sec = 0
    while sec < 60:
        line = "{} & {} & {} & {} & {} - {} & {} - {} & {} - {} \\\ \n".format(sec,suninc(min,sec),ariesinc(min,sec),mooninc(min,sec),str(round(0.1*sec,1)),vcorr(min,0.1*sec),str(round(6+0.1*sec,1)),vcorr(min,6+0.1*sec),str(round(12+0.1*sec,1)),vcorr(min,12+0.1*sec))
        tab = tab + line
        sec += 1
        
    tab = tab+r"""\hline \end{tabular*}
    """
    return tab

def allinctabs():
	# iterates throu 60 minutes
	min=0
	tab=""
	while min < 60:
		tab = tab + inctab(min)
		min += 1
	return tab

def dip(meter):
	dip=60*0.0293*sqrt(meter)
	return dip

def diptab():
	meter=1
	tab = r'''\noindent 
	\begin{tabular}[t]{|c c c|} 
	\multicolumn{3}{c}{\textbf{DIP}}\\
	\hline 
	\textit{m} & \textit{dip} & \textit{ft}\\ 
	\hline
	'''
	while meter < 25.5:
		line = "{} &  {:.1f} & {:.1f}\\\ \n".format(meter, dip(meter), meter/0.3084)
		tab = tab + line
		meter += 0.5
	tab = tab + r"""\hline
	\end{tabular}
	"""
	
	return tab

def refrac(h):
	r = 1/tan((h+7.31/(h+4.4))/180*pi)
	return r

def refractab():
	ho=5
	tab = r'''\noindent 
	\begin{tabular}[t]{|c c|} 
	\multicolumn{2}{c}{\textbf{Refract.}}\\
	\hline 
	\textit{$H_{a}$} & \textit{ref} \\ 
	\hline
	'''
	while ho < 20:
		line = "{}$^\circ$ &  {:.1f}\\\ \n".format(ho, refrac(ho))
		tab = tab + line
		ho += 0.5
	while ho < 40:
		line = "{}$^\circ$ &  {:.1f}\\\ \n".format(ho, refrac(ho))
		tab = tab + line
		ho += 1
	while ho < 90:
		line = "{}$^\circ$ &  {:.1f}\\\ \n".format(ho, refrac(ho))
		tab = tab + line
		ho += 5
	tab = tab + r"""\hline
	\end{tabular}
	"""
	return tab

def parallax(hp, deg, min):
	#returns parallax in dec minutes from horizontal parallax, and Ha
	p = rad(0, hp) * cos(rad(deg, min)) * 180/pi *60
	return p 
	
def parallaxtab():
	Hdeg=0 
	
	HP=54.0
	tab = r'''\noindent 
	\begin{tabular}[t]{|c|rrrrrrrrrrrrrrrrrr|}
	\multicolumn{19}{c}{\textbf{Parallax of the Moon}}\\
	\hline
	'''
	d = 0
	line = r"\textbf{$H_{a}$} "
	while d<90:
		line += r"& \multicolumn{{1}}{{>{{\hspace{{-4pt}}}}c<{{\hspace{{-4pt}}}}|}}{{\textbf{{{}-{}$^\circ$}}}}".format(d, d+5)
		d+= 5
	line += " \\\ \n \\hline"
	tab += line
	
	while Hdeg < 5 :
		#line = " \u0027 "        # DOCKER ONLY
		line = " $'$ "
		dd = Hdeg
		while dd < 90:
			line += r"& \multicolumn{{1}}{{l}}{{\textbf{{{}$^\circ$}}}}".format(dd)
			dd += 5
		line += "\\vline \\\ \n"
		tab = tab + line
		Hmin=0
		while Hmin < 60:
			dd = Hdeg
			line = r"\textbf{{{}}} ".format(Hmin)
			while dd < 90:
				line += " & {:.1f} ".format(parallax(HP,dd,Hmin))
				dd += 5
			line += "\\\ \n"
			tab = tab + line
			Hmin += 10	
		Hdeg += 1
		
	tab += r"""\hline 
	\multicolumn{1}{|c|}{\textbf{HP}} & \multicolumn{18}{c|}{correction for HP per column}\\
	\hline
	"""
	hp = 54.3
	while hp<61.5:
		line = r"\textbf{{ {:.1f}}} ".format(hp)
		d = 2
		while d<90:
			line += "& {:.1f} ".format(parallax(hp, d, 30) - parallax(54, d, 30))
			d += 5
		line += "\\\ \n"
		tab += line
		hp += 0.3
			
		
	tab = tab + r"""\hline
	\end{tabular}
	"""
	return tab
	
def venparallax():
	Hdeg=10 
	
	tab = r'''\noindent 
	\begin{tabular}[t]{|c|cccccc|}
	\multicolumn{7}{c}{\textbf{Parallax of Venus and Mars}}\\
	'''
	tab += r"""\hline 
	$H_{a}$ HP & \textbf{.1$'$} & \textbf{.2$'$} & \textbf{.3$'$} & \textbf{.4$'$} & \textbf{.5$'$} & \textbf{.6$'$} \\
	\hline
	"""
	while Hdeg<90:
		hp = 0.1
		line = r"\textbf{{ {}$^\circ$}} ".format(Hdeg)
		while hp < 0.7:
			line += "& {:.1f} ".format(parallax(hp, Hdeg, 0))
			hp += 0.1
		line += "\\\ \n"
		tab += line
		Hdeg += 10		
	tab = tab + r"""\hline
	\end{tabular}
	"""
	return tab

# >>>>>>>>>>>>>>>>>>>>>>>>
def makelatex():
	lx = r"""\documentclass[ 10pt, a4paper]{scrreprt}
	\usepackage[automark]{scrlayer-scrpage}
	\pagestyle{scrheadings}
	\clearpairofpagestyles
	\chead{\large \textbf{Increments and Corrections}}
    %\usepackage[utf8]{inputenc}
    \usepackage[english]{babel}
    \usepackage{fontenc}
    %\usepackage{upquote}
    \usepackage{array, multicol, blindtext}
    \usepackage[landscape,headsep=0mm, headheight=5mm, top=15mm, bottom=15mm, left=8mm, right=8mm]{geometry}
	\newcommand{\HRule}{\rule{\linewidth}{0.9mm}}
	\usepackage[pdftex]{graphicx}
    %\DeclareUnicodeCharacter{00B0}{\ensuremath{{}^\circ}}
\begin{document}
% ----------------------
% CAUTION: the next 2 lines suppress Overfull \hbox (badness 10000) messages
\hbadness=10000
\newcount\hbadness
% CAUTION: the next 2 lines suppress Overfull \hbox (too wide) messages below 6.5Pt
\hfuzz=6.5Pt
\newdimen\hfuzz
% ----------------------
\begin{scriptsize}"""
	lx = lx + allinctabs()
	lx = lx + refractab()
	lx = lx + parallaxtab()
	lx = lx + diptab()
	lx += r''' \end{scriptsize} \newpage
	\begin{multicols}{2} \begin{scriptsize}
	'''
	lx = lx + venparallax()
	lx = lx + r'''\end{scriptsize} \newpage
	\section*{About these tables}
	The preceding static tables are independent from the year. They differ from the tables found in the official paper versions of the Nautical almanac in two important considerations. 
\begin{itemize}
      \item My tables are not arranged as \textit{critical} tables. So chose the value that fits best to your value and interpolate in the rare cases where this should be necessary.
      \item My tables do not combine multiple corrections as some tables in the paper Nautical Almanac do. Each correction has to be applied separately. 
    \end{itemize}
All tables that are specific for a year are contained in the Nautical Almanac daily pages for the corresponding year.
\subsubsection*{Increments}
The large increment table is is nothing but a linear interpolation between the tabulated values in the daily pages of the Nautical almanac. This table is basically identical with the official one.
\subsubsection*{DIP}
The DIP table corrects for height of eye over the surface. This value has to be subtracted from the sextant altitude ($H_s$). The  correction in degrees for height of eye in meters is given by the following formula: 
\[d=0.0293\sqrt{m}\]
This is the first correction (apart from index error) that has to be applied to the measured altitude.
\subsubsection*{Refraction}
The next correction is for refraction in the earth's atmosphere. As usual this table is correct for 10$^\circ$C and a pressure of 1010 hPa. This correction has to be applied to apparent altitude ($H_a$). The exact values can be calculated by the following formula.
\[R_0=\cot \left( H_a + \frac{7.31}{H_a+4.4}\right)\]
For other than standard conditions, calculate a correction factor for $R_0$ by: \[f=\frac{0.28P}{T+273}\] where $P$ is the pressure in hectopascal and $T$ is the temperature in $^\circ$C. No table is given for this correction so far.
\subsubsection*{Parallax}
For moon sight (and if necessary for Mars and Venus) a parallax correction is necessary. For Mars and Venus the horizontal parallax ($HP$) is never more than 0.5' and can be omitted if this kind of precision is not necessary. The parallax ($P$) can be calculated from horizontal parallax ($HP$) and apparent altitude $H_a$ with the following formula:
\[P={HP} \times \cos(H_a)\]
The table for the moon gives the parallax for a horizontal parallax of 54' which is the lowest value for the moon. For all other values, the value in the lower half of the table has to be added. Note that this table is only for parallax and does not correct for refraction and semidiameter. For all moon and sun sights, semidiameter has to be added for lower limb sights and subtracted for upper limb sights. The value for HP and semidiameter is tabulated in the daily pages. The smaller parallax table is for parallax of Venus and Mars.
\subsubsection*{Altitude correction}
To correct your sextant altitude $H_s$ do the following:
Calculate $H_a$ by
 \[H_a= H_s+I-d\] 
Where $I$ is the sextant's index error and $d$ is DIP. Then calculate the observed altitude $H_o$ by
\[H_o= H_a-R+P\pm SD\]
where $R$ is refraction, $P$ is parallax and $SD$ is the semidiameter.
\subsubsection*{Sight reduction}
Sight reduction tables can be downloaded from the US government's internet pages. Search for HO-229 or HO-249.  These values can also be calculated with two, relatively simple, formulas:
\[ \sin H_c= \sin L \sin d + \cos L \cos d \cos LHA\]
and
\[\cos A = \frac{\sin d - \sin L \sin H_c}{\cos L \cos H_c}\]
where $A$ is the azimuth angle, $L$ is the latitude, $d$ is the declination and $LHA$ is the local hour angle. The azimuth ($Z_n$) is given by the following rule:
\begin{itemize}
      \item if the $LHA$ is greater than $180^\circ$,\quad$Z_n=A$
      \item if the $LHA$ is less than $180^\circ$,\quad$Z_n = 360^\circ - A$
\end{itemize}

	\end{multicols} \end{document}'''
	return lx

#if sys.version_info[0] != 3:
#    raise Exception("This runs with Python 3")

#fn = "inc"
#filename = fn + ".tex"
#outfile = open(filename, mode="w", encoding="utf8")
#outfile.write(makelatex())
#outfile.close()
#command = 'pdflatex {}'.format(filename)
#os.system(command)
#print("finished")
#os.remove(fn + ".tex")
#os.remove(fn + ".log")
#os.remove(fn + ".aux")