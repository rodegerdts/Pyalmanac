#! /usr/bin/python
# -*- coding: UTF-8 -*-




def degmin(deg):
    #changes decimal degrees to the format usually used in the nautical almanac. (dddÂ°mm.m')
    g = int(deg)
    m = (deg-g)*60
    gm = "%s°%04.1f" %(g,abs(m))
    return gm

def decdeg(d,min):
	d=d*1.0
	min=min*1.0
	deg=d+(min/60)
	return deg

def suninc(m,s):
	min= m*1.0
	sec=s/60.0
	hour=(sec+min)/60
	inc=degmin(15*hour)
	return inc

def ariesinc(m,s):
	min= m*1.0
	sec=s/60.0
	hour=(sec+min)/60
	inc=degmin(decdeg(15,2.46)*hour)
	return inc

def mooninc(m,s):
	min= m*1.0
	sec=s/60.0
	hour=(sec+min)/60
	inc=degmin(decdeg(14,19.0)*hour)
	return inc
	
def vcorr(m,v):
	h=(m+0.5)/60.0
	corr=round(v*h,1)
	return corr


def inctab(min):
    """generates a latex table for increments"""
    tab = r'''\noindent
    \begin{tabular*}{0.33\textwidth}[t]{@{\extracolsep{\fill}}|>{\bfseries}p{0.3cm}|>{\hspace{-3pt}}r|>{\hspace{-3pt}}r|>{\hspace{-3pt}}r||>{\hspace{-3pt}}c>{\hspace{-3pt}}c>{\hspace{-3pt}}c<{\hspace{-3pt}}|}
    \hline
    {\tiny m} \textbf{'''
    
    tab = tab+"%s" %(int(min))
    
    tab=tab+ r'''} & \multicolumn{1}{p{0.5cm}|}{\textbf{Sun Plan.}} & \multicolumn{1}{c|}{\textbf{Aries}} & \multicolumn{1}{c||}{\textbf{Moon}} & \multicolumn{3}{c|}{\textit{\textbf{c and d corr}}}\\ 
    \hline'''
   
    sec = 0
    while sec < 60:
        line = "%s & %s & %s & %s & %s - %s & %s - %s & %s - %s \\\ \n" %(sec,suninc(min,sec),ariesinc(min,sec),mooninc(min,sec),str(round(0.1*sec,1)),vcorr(min,0.1*sec),str(round(6+0.1*sec,1)),vcorr(min,6+0.1*sec),str(round(12+0.1*sec,1)),vcorr(min,12+0.1*sec))
        tab = tab + line
        sec += 1
        
    tab = tab+r"""\hline \end{tabular*}
    """
    return tab

def allinctabs():
	min=0
	tab=""
	while min < 60:
		tab = tab + inctab(min)
		min += 1
	return tab
	
def makelatex():
	lx = r"""\documentclass[ 10pt, twoside, a4paper]{scrreprt}
	\usepackage[automark]{scrpage2}
	\pagestyle{scrheadings}
	\clearscrheadfoot
	\chead{\large \textbf{Increments and Corrections}}
    \usepackage[utf8x]{inputenc}
    \usepackage[english]{babel}
    \usepackage{fontenc}
    \usepackage{array}
    \usepackage[landscape,headsep=0mm, headheight=5mm, top=15mm, bottom=15mm, left=8mm, right=8mm]{geometry}
	\newcommand{\HRule}{\rule{\linewidth}{0.5mm}}
	\usepackage[pdftex]{graphicx}
\begin{document}
\begin{scriptsize}"""
	lx = lx + allinctabs()
	lx = lx + '\end{scriptsize} \end{document}'
	return lx
    
outfile = open("inc.tex", 'w')
outfile.write(makelatex())
outfile.close()
	