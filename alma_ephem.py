#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# contains all functions that calculate values for the nautical almanac

#	Copyright (C) 2014  Enno Rodegerdts
#   Copyright (C) 2019  Andrew Bauer

#  	This program is free software; you can redistribute it and/or modify
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

import ephem
import math
import datetime
import config
import sys

def time(date): 
    # turn an ephem.date (float) into a time string formatted hh:mm
    tup = date.tuple()
    hr = tup[-3]
    # round >=30 seconds to next minute
    min = tup[-2] + int(round((tup[-1]/60)+0.00001))
#    nextday = False
    if min == 60:
        min = 0
        hr += 1
        if hr == 24:
            hr = 0
#            nextday = True	# time rounded up into next day
    time = '%02d:%02d' %(hr,min)
#    return time, nextday
    # NOTE: this function could easily return the information that rounding
    #       flipped into the next day, however this is not required here.
    return time


def nadeg(rad,fixedwidth=1):
    # changes ephem.angle (rad) to the format usually used in the nautical almanac (ddd°mm.m) and returns a string object.
	# the optional argument specifies the minimum width for degrees (only)
    theminus = ""
    if rad < 0:
    	theminus = "-"
    df = abs(math.degrees(rad))	# convert radians to degrees (float)
    di = int(df)			# degrees (integer)
    # note: round() uses "Rounding Half To Even" strategy
    mf = round((df-di)*60, 1)	# minutes (float), rounded to 1 decimal place
    mi = int(mf)			# minutes (integer)
    if mi == 60:
        mf -= 60
        di += 1
        if di == 360:
            di = 0
    if fixedwidth == 2:
        gm = "%s%02i°%04.1f" %(theminus,di,mf)
    else:
        if fixedwidth == 3:
            gm = "%s%03i°%04.1f" %(theminus,di,mf)
        else:
            gm = "%s%s°%04.1f" %(theminus,di,mf)
    return gm


#List of navigational stars from PyEphem 3.7.6
db = """\
Alpheratz,f|S|B9,0:08:23.2|135.68,29:05:27|-162.95,2.07,2000,0
Ankaa,f|S|K0,00:26:17.1|232.75,-42:18:21.5|-353.62,2.37,2000,0
Schedar,f|S|K0,0:40:30.4|50.36,56:32:15|-32.17,2.24,2000,0
Diphda,f|S|G9,00:43:35.8|232.79,-17:59:11.8|32.71,2.04,2000,0
Achernar,f|S|B3,1:37:42.8|88.02,-57:14:12|-40.08,0.45,2000,0
Hamal,f|S|K2,2:07:10.3|190.73,23:27:46|-145.77,2.01,2000,0
Polaris,f|S|F7,2:31:47.1|44.22,89:15:51|-11.74,1.97,2000,0
Acamar,f|S|A3,02:58:15.696|-44.6,-40:18:16.97|19.0,3.2,2000,0
Menkar,f|S|M2,3:02:16.8|-11.81,4:05:24|-78.76,2.54,2000,0
Mirfak,f|S|F5,03:24:19.37|24.11,49:51:40.25|-26.01,1.8,2000,0
Aldebaran,f|S|K5,4:35:55.2|62.78,16:30:35|-189.36,0.87,2000,0
Rigel,f|S|B8,5:14:32.3|1.87,-8:12:06|-0.56,0.18,2000,0
Capella,f|S|M1,5:16:41.3|75.52,45:59:57|-427.13,0.08,2000,0
Bellatrix,f|S|B2,5:25:07.9|-8.75,6:20:59|-13.28,1.64,2000,0
Elnath,f|S|B7,5:26:17.5|23.28,28:36:28|-174.22,1.65,2000,0
Alnilam,f|S|B0,5:36:12.8|1.49,-1:12:07|-1.06,1.69,2000,0
Betelgeuse,f|S|M2,5:55:10.3|27.33,7:24:25|10.86,0.45,2000,0
Canopus,f|S|F0,6:23:57.1|19.99,-52:41:45|23.67,-0.62,2000,0
Sirius,f|S|A0,6:45:09.3|-546.01,-16:42:47|-1223.08,-1.44,2000,0
Adhara,f|S|B2,6:58:37.6|2.63,-28:58:20|2.29,1.50,2000,0
Procyon,f|S|F5,7:39:18.5|-716.57,5:13:39|-1034.58,0.40,2000,0
Pollux,f|S|K0,7:45:19.4|-625.69,28:01:35|-45.95,1.16,2000,0
Avior,f|S|K3,08:22:30.8|-25.34,-59:30:34.1|22.72,1.9,2000,0
Suhail,f|S|K4,09:07:59.8|-23.21,-43:25:57.3|14.28,2.2,2000,0
Miaplacidus,f|S|A2,09:13:11.9|-157.66,-69:43:01.9|108.91,1.7,2000,0
Alphard,f|S|K3,9:27:35.3|-14.49,-8:39:31|33.25,1.99,2000,0
Regulus,f|S|B7,10:08:22.5|-249.4,11:58:02|4.91,1.36,2000,0
Dubhe,f|S|F7,11:03:43.8|-136.46,61:45:04|-35.25,1.81,2000,0
Denebola,f|S|A3,11:49:03.9|-499.02,14:34:20|-113.78,2.14,2000,0
Gienah,f|S|B8,12:15:48.5|-159.58,-17:32:31|22.31,2.58,2000,0
Acrux,f|S|B0,12:26:35.9|-35.3,-63:05:56.58|-12.0,1.4,2000,0
Gacrux,f|S|M3,12:31:09.95|27.94,-57:06:47.56|-264.33,1.6,2000,0
Alioth,f|S|A0,12:54:01.6|111.74,55:57:35|-8.99,1.76,2000,0
Spica,f|S|B1,13:25:11.6|-42.5,-11:09:40|-31.73,0.98,2000,0
Alkaid,f|S|B3,13:47:32.5|-121.23,49:18:48|-15.56,1.85,2000,0
Hadar,f|S|B1,14:03:49.4|-33.96,-60:22:23|-25.06,0.61,2000,0
Menkent,f|S|,14:06:40.9|-519.30,-36:22:11.8|-517.86,2.06,2000,0
Arcturus,f|S|K2,14:15:40.3|-1093.45,19:11:14|-1999.4,-0.05,2000,0
Rigil Kent.,f|S|G2,14:39:36.5|-3679.26,-60:50:02.3|483.03,-0.01,2000,0
Kochab,f|S|K4,14:50:42.4|-32.29,74:09:20|11.91,2.07,2000,0
Zuben'ubi,f|S|,14:50:52.7|-105.69,-16:02:30.4|-69.0,2.7,2000,0
Alphecca,f|S|A0,15:34:41.2|120.38,26:42:54|-89.44,2.22,2000,0
Antares,f|S|M1,16:29:24.5|-10.16,-26:25:55|-23.21,1.06,2000,0
Atria,f|S|K2,16:48:39.9|17.85,-69:01:39.8|-32.92,1.9,2000,0
Sabik,f|S|A2,17:10:22.7|41.16,-15:43:29.7|97.65,2.4,2000,0
Shaula,f|S|B1,17:33:36.5|-8.9,-37:06:13|-29.95,1.62,2000,0
Rasalhague,f|S|A5,17:34:56.0|110.08,12:33:38|-222.61,2.08,2000,0
Eltanin,f|S|K5,17:56:36.4|-8.52,51:29:20|-23.05,2.24,2000,0
Kaus Aust.,f|S|B9,18:24:10.4|-39.61,-34:23:04|-124.05,1.79,2000,0
Vega,f|S|A0,18:36:56.2|201.02,38:46:59|287.46,0.03,2000,0
Nunki,f|S|B2,18:55:15.9|13.87,-26:17:48|-52.65,2.05,2000,0
Altair,f|S|A7,19:50:46.7|536.82,8:52:03|385.54,0.76,2000,0
Peacock,f|S|B2,20:25:38.9|7.71,-56:44:06|-86.15,1.94,2000,0
Deneb,f|S|A2,20:41:25.9|1.56,45:16:49|1.55,1.25,2000,0
Enif,f|S|K2,21:44:11.1|30.02,9:52:30|1.38,2.38,2000,0
Al Na'ir,f|S|B7,22:08:13.9|127.6,-46:57:38|-147.91,1.73,2000,0
Fomalhaut,f|S|A3,22:57:38.8|329.22,-29:37:19|-164.22,1.17,2000,0
Scheat,f|S|M2,23:03:46.3|187.76,28:04:57|137.61,2.44,2000,0
Markab,f|S|B9,23:04:45.6|61.1,15:12:19|-42.56,2.49,2000,0
"""


def stellar(date):
    # returns a list of lists with name, SHA and Dec for all navigational stars for epoch of date.
    out = []
    for line in db.strip().split('\n'):
        st = ephem.readdb(line)
        st.compute(date+0.5)    # calculate at noon
        out.append([st.name,nadeg(2*math.pi-ephem.degrees(st.g_ra).norm),nadeg(st.g_dec)])
    return out


def planets(date):
    # this function returns a tuple of strings with ephemerids in the format used by the nautical almanac.
    
    # following are objects and their values:
    #Aries      gha
    #Venus      gha dec
    #Mars       gha dec
    #Jupiter    gha dec
    #Saturn     gha dec

    v = ephem.Venus()
    mars = ephem.Mars()
    j = ephem.Jupiter()
    sat = ephem.Saturn()
    obs = ephem.Observer()
    obs.date = date
    
    #Aries, First Point of
    deg = ephem.degrees(obs.sidereal_time()).norm
    ghaa = nadeg(deg)
    
    #Venus
    v.compute(date,epoch=date)
    deg = ephem.degrees(obs.sidereal_time()-v.g_ra).norm
    ghav = nadeg(deg)
    degv = v.g_dec
    decv = nadeg(degv,2)
    
    #Mars
    mars.compute(date,epoch=date)
    deg = ephem.degrees(obs.sidereal_time()-mars.g_ra).norm
    ghamars = nadeg(deg)
    degmars = mars.g_dec
    decmars = nadeg(degmars,2)
    
    #Jupiter
    j.compute(date,epoch=date)
    deg = ephem.degrees(obs.sidereal_time()-j.g_ra).norm
    ghaj = nadeg(deg)
    degj = j.g_dec
    decj = nadeg(degj,2)
    
    #Saturn
    sat.compute(date,epoch=date)
    deg = ephem.degrees(obs.sidereal_time()-sat.g_ra).norm
    ghasat = nadeg(deg)
    degsat = sat.g_dec
    decsat = nadeg(degsat,2)

    # degv, degmars, degj, degsat have been added for the planetstab function
    return ghaa,ghav,decv,ghamars,decmars,ghaj,decj,ghasat,decsat,degv,degmars,degj,degsat


def sunmoon(date):
    # returns ephemrerids for sun and moon.
    
    #Sun        gha dec
    #Moon       gha v dec d hp

    s = ephem.Sun()
    m = ephem.Moon()
    obs = ephem.Observer()
    obs.date = date
    
    #Sun
    s.compute(date,epoch=date)
    deg = ephem.degrees(obs.sidereal_time()-s.g_ra).norm
    ghas = nadeg(deg)
    degs = s.g_dec
    decs = nadeg(degs,2)
    
    #Moon
    m.compute(date,epoch=date)
    deg = ephem.degrees(obs.sidereal_time()-m.g_ra).norm
    gham = nadeg(deg)
    degm = m.g_dec
    decm = nadeg(degm,2)
    
    #calculate the moons horizontal paralax
    deg = ephem.degrees(m.radius/0.272805950305)
    hp = "%0.1f'" %(deg*360*30/ephem.pi)
    
    #calculate v and d by advancing the time with one hour.
    m.compute(date-0.5*ephem.hour,epoch=date-0.5*ephem.hour)
    obs.date = date-0.5*ephem.hour
    rgha = ephem.degrees(obs.sidereal_time()-m.g_ra).norm
    rdec = m.g_dec
    m.compute(date+0.5*ephem.hour,epoch=date+0.5*ephem.hour)
    obs.date = date+0.5*ephem.hour
    rghap = ephem.degrees(obs.sidereal_time()-m.g_ra).norm
    deg = ephem.degrees(ephem.degrees(rghap-rgha).norm-ephem.degrees('14:19:00'))
    vm = "%0.1f'" %(deg*360*30/ephem.pi)
    deg = ephem.degrees(m.g_dec-rdec)
    dm = "%0.1f'" %(deg*360*30/ephem.pi)
    
    # degs, degm have been added for the sunmooontab function
    return ghas,decs,gham,vm,decm,dm,hp,degs,degm


def vdmean(date):
    # returns  v and d and magitude for the navigational planets. (mm.m difference from 15°)
    
    # for the sun it computes semidiameter(SD) and d
    # ...just SD for the moon

    s = ephem.Sun()
    m = ephem.Moon()
    v = ephem.Venus()
    mars = ephem.Mars()
    j = ephem.Jupiter()
    sat = ephem.Saturn()
    obs = ephem.Observer()
    obs.date = date
    
    #Sun
    s.compute(date)
    dec = s.g_dec
    s.compute(date+ephem.hour)
    obs.date = date+ephem.hour
    deg = ephem.degrees(s.g_dec-dec)
    ds = "%0.1f" %(deg*360*30/ephem.pi)
    sds = "%0.1f" %(s.radius*360*30/ephem.pi)
    
    #Moon
    m.compute(date)
    sdm = "%0.1f" %(m.radius*360*30/ephem.pi)
    
    #Venus
    obs.date = date
    v.compute(date)
    gha = ephem.degrees(obs.sidereal_time()-v.g_ra).norm
    dec = v.g_dec
    v.compute(date+ephem.hour)
    obs.date = date+ephem.hour
    ghap = ephem.degrees(obs.sidereal_time()-v.g_ra).norm
    deg = ephem.degrees(ghap-gha).norm-ephem.degrees('15:00:00')
    vv = "%0.1f" %(deg*360*30/ephem.pi)
    deg = ephem.degrees(v.g_dec-dec)
    dv = "%0.1f" %(deg*360*30/ephem.pi)
    mv = "%0.1f" %(v.mag)
    
    #Mars
    obs.date = date
    mars.compute(date)
    gha = ephem.degrees(obs.sidereal_time()-mars.g_ra).norm
    dec = mars.g_dec
    mars.compute(date+ephem.hour)
    obs.date = date+ephem.hour
    ghap = ephem.degrees(obs.sidereal_time()-mars.g_ra).norm
    deg = ephem.degrees(ephem.degrees(ghap-gha).norm-ephem.degrees('15:00:00'))
    vmars = "%0.1f" %(deg*360*30/ephem.pi)
    deg = ephem.degrees(mars.g_dec-dec)
    dmars = "%0.1f" %(deg*360*30/ephem.pi)
    mmars = "%0.1f" %(mars.mag)
    
    #Jupiter
    obs.date = date
    j.compute(date)
    gha = ephem.degrees(obs.sidereal_time()-j.g_ra).norm
    dec = j.g_dec
    j.compute(date+ephem.hour)
    obs.date = date+ephem.hour
    ghap = ephem.degrees(obs.sidereal_time()-j.g_ra).norm
    deg = ephem.degrees(ephem.degrees(ghap-gha).norm-ephem.degrees('15:00:00'))
    vj = "%0.1f" %(deg*360*30/ephem.pi)
    deg = ephem.degrees(j.g_dec-dec)
    dj = "%0.1f" %(deg*360*30/ephem.pi)
    mj = "%0.1f" %(j.mag)
    
    #Saturn
    obs.date = date
    sat.compute(date)
    gha = ephem.degrees(obs.sidereal_time()-sat.g_ra).norm
    dec = sat.g_dec
    sat.compute(date+ephem.hour)
    obs.date = date+ephem.hour
    ghap = ephem.degrees(obs.sidereal_time()-sat.g_ra).norm
    deg = ephem.degrees(ephem.degrees(ghap-gha).norm-ephem.degrees('15:00:00'))
    vsat = "%0.1f" %(deg*360*30/ephem.pi)
    deg = ephem.degrees(sat.g_dec-dec)
    dsat = "%0.1f" %(deg*360*30/ephem.pi)
    msat = "%0.1f" %(sat.mag)
    
    return ds,sds,sdm,vv,dv,mv,vmars,dmars,mmars,vj,dj,mj,vsat,dsat,msat


def twilight(date, lat):
    # Returns for given date and latitude(in full degrees):
    # naut. and civil twilight (before sunrise), sunrise, meridian passage, sunset, civil and nautical twilight (after sunset).
    # NOTE: 'twilight' is only called for every third day in the Full Almanac...
    #       ...therefore daily tracking of the sun state is impossible.

    latitude = ephem.degrees('%s:00:00.0' %lat)
    out = [0,0,0,0,0,0,0]
    obs = ephem.Observer()
    obs.lat = latitude
    obs.date = date
    obs.pressure = 0
    s = ephem.Sun(obs)
    s.compute(date)
    r = s.radius

    obs.horizon = ephem.degrees('-12')+r	# Nautical twilight ...
    try:
        out[0] = time(obs.next_rising(s))	# begin
    except:
        out[0] = '--:--'
    obs.date = date
    try:
        out[6] = time(obs.next_setting(s))	# end
    except:
        out[6] = '--:--'
#-----------------------------------------------------------
    obs.horizon = ephem.degrees('-6')+r		# Civil twilight...
    obs.date = date
    try:
        out[1] = time(obs.next_rising(s))	# begin
    except:
        out[1] = '--:--'
    obs.date = date
    try:
        out[5] = time(obs.next_setting(s))	# end
    except:
        out[5] = '--:--'
#-----------------------------------------------------------
    obs.horizon = '-0:34'
    obs.date = date
    try:
        out[2] = time(obs.next_rising(s))	# sunrise
    except:
        out[2] = '--:--'
    obs.date = date
    try:
        out[4] = time(obs.next_setting(s))	# sunset
    except:
        out[4] = '--:--'
    obs.date = date
    out[3] = time(obs.next_transit(s))
    
    return out

def moonrise(date,lat):
    # returns moonrise and moonset for the given date and latitude plus next 2 days:
    #    rise day 1, rise day 2, rise day 3, set day 1, set day 2, set day 3

    latitude = ephem.degrees('%s:00:00.0' %lat)
    out  = ['--:--','--:--','--:--','--:--','--:--','--:--']	# first event
    out2 = ['--:--','--:--','--:--','--:--','--:--','--:--']	# second event on same day (rare)
    obs = ephem.Observer()
    obs.lat = latitude
    obs.pressure = 0
    m = ephem.Moon(obs)
    obs.horizon = '-0:34'

    d = ephem.date(date - 30 * ephem.second)
    obs.date = d
    m.compute(d)
    try:
        firstrising = obs.next_rising(m)
        if firstrising-obs.date >= 1:
            raise ValueError, 'event next day'
        out[0] = time(firstrising)		# note: overflow to 00:00 next day is correct here
    except Exception:
        out[0] = '--:--'
    try:
        nextr = obs.next_rising(m, start=firstrising)
        if nextr-obs.date < 1:
            out2[0] = time(nextr)		# note: overflow to 00:00 next day is correct here
    except UnboundLocalError:
        pass
    except ephem.NeverUpError:
        pass
    except ephem.AlwaysUpError:
        pass
    except Exception:
        flag_msg("Oops! %s occured, line: %s" %(sys.exc_info()[1],sys.exc_info()[2].tb_lineno))
        sys.exc_clear()		# only in Python 2

    obs.date = d
    try:
        firstsetting = obs.next_setting(m)
        if firstsetting-obs.date >= 1:
            raise ValueError, 'event next day'
        out[3] = time(firstsetting)		# note: overflow to 00:00 next day is correct here
    except Exception:
        out[3] = '--:--'
    try:
        nexts = obs.next_setting(m, start=firstsetting)
        if nexts-obs.date < 1:
            out2[3] = time(nexts)		# note: overflow to 00:00 next day is correct here
    except UnboundLocalError:
        pass
    except ephem.NeverUpError:
        pass
    except ephem.AlwaysUpError:
        pass
    except Exception:
        flag_msg("Oops! %s occured, line: %s" %(sys.exc_info()[1],sys.exc_info()[2].tb_lineno))
        sys.exc_clear()		# only in Python 2
#-----------------------------------------------------------
    d = ephem.date(date + 1 - 30 * ephem.second)
    obs.date = d
    m.compute(d)
    try:
        firstrising = obs.next_rising(m)
        if firstrising-obs.date >= 1:
            raise ValueError, 'event next day'
        out[1] = time(firstrising)		# note: overflow to 00:00 next day is correct here
    except Exception:
        out[1] = '--:--'
    try:
        nextr = obs.next_rising(m, start=firstrising)
        if nextr-obs.date < 1:
            out2[1] = time(nextr)		# note: overflow to 00:00 next day is correct here
    except UnboundLocalError:
        pass
    except ephem.NeverUpError:
        pass
    except ephem.AlwaysUpError:
        pass
    except Exception:
        flag_msg("Oops! %s occured, line: %s" %(sys.exc_info()[1],sys.exc_info()[2].tb_lineno))
        sys.exc_clear()		# only in Python 2

    obs.date = d
    try:
        firstsetting = obs.next_setting(m)
        if firstsetting-obs.date >= 1:
            raise ValueError, 'event next day'
        out[4] = time(firstsetting)		# note: overflow to 00:00 next day is correct here
    except Exception:
        out[4] = '--:--'
    try:
        nexts = obs.next_setting(m, start=firstsetting)
        if nexts-obs.date < 1:
            out2[4] = time(nexts)		# note: overflow to 00:00 next day is correct here
    except UnboundLocalError:
        pass
    except ephem.NeverUpError:
        pass
    except ephem.AlwaysUpError:
        pass
    except Exception:
        flag_msg("Oops! %s occured, line: %s" %(sys.exc_info()[1],sys.exc_info()[2].tb_lineno))
        sys.exc_clear()		# only in Python 2
#-----------------------------------------------------------
    d = ephem.date(date + 2 - 30 * ephem.second)
    obs.date = d
    m.compute(d)
    try:
        firstrising = obs.next_rising(m)
        if firstrising-obs.date >= 1:
            raise ValueError, 'event next day'
        out[2] = time(firstrising)		# note: overflow to 00:00 next day is correct here
    except Exception:
        out[2] = '--:--'
    try:
        nextr = obs.next_rising(m, start=firstrising)
        if nextr-obs.date < 1:
            out2[2] = time(nextr)		# note: overflow to 00:00 next day is correct here
    except UnboundLocalError:
        pass
    except ephem.NeverUpError:
        pass
    except ephem.AlwaysUpError:
        pass
    except Exception:
        flag_msg("Oops! %s occured, line: %s" %(sys.exc_info()[1],sys.exc_info()[2].tb_lineno))
        sys.exc_clear()		# only in Python 2

    obs.date = d
    try:
        firstsetting = obs.next_setting(m)
        if firstsetting-obs.date >= 1:
            raise ValueError, 'event next day'
        out[5] = time(firstsetting)		# note: overflow to 00:00 next day is correct here
    except Exception:
        out[5] = '--:--'
    try:
        nexts = obs.next_setting(m, start=firstsetting)
        if nexts-obs.date < 1:
            out2[5] = time(nexts)		# note: overflow to 00:00 next day is correct here
    except UnboundLocalError:
        pass
    except ephem.NeverUpError:
        pass
    except ephem.AlwaysUpError:
        pass
    except Exception:
        flag_msg("Oops! %s occured, line: %s" %(sys.exc_info()[1],sys.exc_info()[2].tb_lineno))
        sys.exc_clear()		# only in Python 2

    return out, out2

def flag_msg(msg):
    if config.logfileopen:
        # if open - write to log file
        config.writeLOG(msg + '\n')
    else:
        # otherwise - print to console
        print(msg)
    return

def ariestransit(date):
    # returns transit time of aries for given date

    obs = ephem.Observer()
    obs.date = ephem.date(date)+1
    sid = obs.sidereal_time()
    trans = ephem.hours(2*math.pi-sid/1.00273790935)
#    obs.date = date + trans/(2*math.pi) #turns ephem.angle (time) into ephem date
    hhmm = str(trans)[0:5]	# can return "h:mm:"
    if hhmm[1:2] == ":":	# check if single digit hours
        hhmm = "0" + hhmm[0:4]
    return hhmm
    
def planetstransit(date):
    #returns SHA and meridian passage for the navigational planets

    v = ephem.Venus()
    mars = ephem.Mars()
    j = ephem.Jupiter()
    sat = ephem.Saturn()
    obs = ephem.Observer()
    
    obs.date = date
    v.compute(date)
    vsha = nadeg(2*math.pi-ephem.degrees(v.g_ra).norm)
    vtrans = time(obs.next_transit(v))
    hpvenus = "%0.1f" %((math.tan(6371/(v.earth_distance*149597870.7)))*60*180/math.pi)
    
    obs.date = date
    mars.compute(date)
    marssha = nadeg(2*math.pi-ephem.degrees(mars.g_ra).norm)
    marstrans = time(obs.next_transit(mars))
    hpmars = "%0.1f" %((math.tan(6371/(mars.earth_distance*149597870.7)))*60*180/math.pi)

    obs.date = date
    j.compute(date)
    jsha = nadeg(2*math.pi-ephem.degrees(j.g_ra).norm)
    jtrans = time(obs.next_transit(j))
    
    obs.date = date
    sat.compute(date)
    satsha = nadeg(2*math.pi-ephem.degrees(sat.g_ra).norm)
    sattrans = time(obs.next_transit(sat))
    
    return [vsha,vtrans,marssha,marstrans,jsha,jtrans,satsha,sattrans,hpmars,hpvenus]

def equation_of_time(date):
    # returns equation of time, the sun's transit time, 
    # the moon's transit-, antitransit-time, age and percent illumination.
    # (Equation of Time = Mean solar time - Apparent solar time)

    py_date = date.tuple()
    py_obsdate = datetime.date(py_date[0], py_date[1], py_date[2])
    d = ephem.date(date - 30 * ephem.second)
    obs = ephem.Observer()
    obs.date = d
    s = ephem.Sun()
    m = ephem.Moon()
    s.compute(d)
    m.compute(d)
    transs = '--:--'
    antim  = '--:--'
    transm = '--:--'

    next_s_tr = obs.next_transit(s,start=d)
    if next_s_tr - obs.date < 1:
        transs = time(next_s_tr)

    next_m_atr = obs.next_antitransit(m,start=d)
    if next_m_atr - obs.date < 1:
        antim = time(next_m_atr)

    next_m_tr = obs.next_transit(m,start=d)
    if next_m_tr - obs.date < 1:
        transm = time(next_m_tr)

#-----------------------------
    obs = ephem.Observer()
    obs.date = date
    
    m.compute(date+0.5)
    pct = int(round(m.phase))   # percent of moon surface illuminated
    age = int(round((date+0.5)-ephem.previous_new_moon(date+0.5)))
    phase = m.elong.norm+0.0    # moon phase as float (0:new to π:full to 2π:new)
    
    s.compute(date-0.1)
    obs.date = date-0.1

    eqt00 = ephem.hours(round((obs.next_antitransit(s)-date)*86400)/86400*2*math.pi)
    eqt00 = str(eqt00)[-8:-3]

    eqt12 = ephem.hours(round((obs.next_transit(s)-(date+0.5))*86400)/86400*2*math.pi)
    eqt12 = str(eqt12)[-8:-3]

    return eqt00,eqt12,transs,transm,antim,age,pct

