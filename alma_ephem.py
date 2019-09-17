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


# List of navigational stars with data from Hipparcos, e.g.:
# http://vizier.u-strasbg.fr/viz-bin/VizieR-5?-source=I/311&-out.all&-out.max=10&HIP==677
# The format corresponds to an XEphem database file:
# http://www.clearskyinstitute.com/xephem/help/xephem.html#mozTocId468501

db = """
Alpheratz,f|S|B9,0:08:23.26|137.46,29:05:25.55|-163.44,2.04,2000,0
Ankaa,f|S|K0,0:26:17.05|233.05,-42:18:21.55|-356.30,2.55,2000,0
Schedar,f|S|K0,0:40:30.44|50.88,56:32:14.39|-32.13,2.41,2000,0
Diphda,f|S|G9,0:43:35.37|232.55,-17:59:11.78|31.99,2.21,2000,0
Achernar,f|S|B3,1:37:42.85|87.00,-57:14:12.31|-38.24,0.42,2000,0
Hamal,f|S|K2,2:07:10.41|188.55,23:27:44.70|-148.08,2.17,2000,0
Polaris,f|S|F7,2:31:49.09|44.48,89:15:50.79|-11.85,2.11,2000,0
Acamar,f|S|A4,2:58:15.68|-52.89,-40:18:16.85|21.98,2.94,2000,0
Menkar,f|S|M2,3:02:16.77|-10.41,4:05:23.06|-76.85,2.62,2000,0
Mirfak,f|S|F5,3:24:19.37|23.75,49:51:40.25|-26.23,1.90,2000,0
Aldebaran,f|S|K5,4:35:55.24|63.45,16:30:33.49|-188.94,1.00,2000,0
Rigel,f|S|B8,5:14:32.27|1.31,-8:12:05.90|0.50,0.19,2000,0
Capella,f|S|M1,5:16:41.36|75.25,45:59:52.77|-426.89,0.24,2000,0
Bellatrix,f|S|B2,5:25:07.86|-8.11,6:20:58.93|-12.88,1.55,2000,0
Elnath,f|S|B7,5:26:17.51|22.76,28:36:26.83|-173.58,1.62,2000,0
Alnilam,f|S|B0,5:36:12.81|1.44,-1:12:06.91|-0.78,1.62,2000,0
Betelgeuse,f|S|M2,5:55:10.31|27.54,7:24:25.43|11.30,0.50,2000,0
Canopus,f|S|F0,6:23:57.11|19.93,-52:41:44.38|23.24,-0.55,2000,0
Sirius,f|S|A0,6:45:08.92|-546.01,-16:42:58.02|-1223.07,-1.09,2000,0
Adhara,f|S|B2,6:58:37.55|3.24,-28:58:19.51|1.33,1.42,2000,0
Procyon,f|S|F5,7:39:18.12|-714.59,5:13:29.96|-1036.80,0.46,2000,0
Pollux,f|S|K0,7:45:18.95|-626.55,28:01:34.32|-45.80,1.29,2000,0
Avior,f|S|K3,8:22:30.84|-25.52,-59:30:34.14|22.06,2.00,2000,0
Suhail,f|S|K4,9:07:59.76|-24.01,-43:25:57.33|13.52,2.34,2000,0
Miaplacidus,f|S|A2,9:13:11.98|-156.47,-69:43:01.95|108.95,1.66,2000,0
Alphard,f|S|K3,9:27:35.24|-15.23,-8:39:30.96|34.37,2.14,2000,0
Regulus,f|S|B7,10:08:22.31|-248.73,11:58:01.95|5.59,1.32,2000,0
Dubhe,f|S|F7,11:03:43.67|-134.11,61:45:03.72|-34.70,1.95,2000,0
Denebola,f|S|A3,11:49:03.58|-497.68,14:34:19.41|-114.67,2.16,2000,0
Gienah,f|S|B8,12:15:48.37|-158.61,-17:32:30.95|21.86,2.55,2000,0
Acrux,f|S|B0,12:26:35.90|-35.83,-63:05:56.73|-14.86,0.67,2000,0
Gacrux,f|S|M4,12:31:09.96|28.23,-57:06:47.57|-265.08,1.63,2000,0
Alioth,f|S|A0,12:54:01.75|111.91,55:57:35.36|-8.24,1.75,2000,0
Spica,f|S|B1,13:25:11.58|-42.35,-11:09:40.75|-30.67,0.89,2000,0
Alkaid,f|S|B3,13:47:32.44|-121.17,49:18:47.76|-14.91,1.80,2000,0
Hadar,f|S|B1,14:03:49.41|-33.27,-60:22:22.93|-23.16,0.54,2000,0
Menkent,f|S|K0,14:06:40.95|-520.53,-36:22:11.84|-518.06,2.22,2000,0
Arcturus,f|S|K2,14:15:39.67|-1093.39,19:10:56.67|-2000.06,0.11,2000,0
Rigil Kent.,f|S|G2,14:39:36.49|-3679.25,-60:50:02.37|473.67,0.14,2000,0
Kochab,f|S|K4,14:50:42.33|-32.61,74:09:19.81|11.42,2.20,2000,0
Zuben'ubi,f|S|A3,14:50:52.71|-105.68,-16:02:30.40|-68.40,2.79,2000,0
Alphecca,f|S|A0,15:34:41.27|120.27,26:42:52.89|-89.58,2.22,2000,0
Antares,f|S|M1,16:29:24.46|-12.11,-26:25:55.21|-23.30,0.98,2000,0
Atria,f|S|K2,16:48:39.90|17.99,-69:01:39.76|-31.58,2.07,2000,0
Sabik,f|S|A2,17:10:22.69|40.13,-15:43:29.66|99.17,2.44,2000,0
Shaula,f|S|B1,17:33:36.52|-8.53,-37:06:13.76|-30.80,1.52,2000,0
Rasalhague,f|S|A5,17:34:56.07|108.07,12:33:36.13|-221.57,2.13,2000,0
Eltanin,f|S|K5,17:56:36.37|-8.48,51:29:20.02|-22.79,2.36,2000,0
Kaus Aust.,f|S|B9,18:24:10.32|-39.42,-34:23:04.62|-124.20,1.80,2000,0
Vega,f|S|A0,18:36:56.34|200.94,38:47:01.28|286.23,0.09,2000,0
Nunki,f|S|B2,18:55:15.93|15.14,-26:17:48.21|-53.43,2.01,2000,0
Altair,f|S|A7,19:50:47.00|536.23,8:52:05.96|385.29,0.83,2000,0
Peacock,f|S|B2,20:25:38.86|6.90,-56:44:06.32|-86.02,1.86,2000,0
Deneb,f|S|A2,20:41:25.92|2.01,45:16:49.22|1.85,1.30,2000,0
Enif,f|S|K2,21:44:11.16|26.92,9:52:30.03|0.44,2.55,2000,0
Al Na'ir,f|S|B7,22:08:13.98|126.69,-46:57:39.51|-147.47,1.70,2000,0
Fomalhaut,f|S|A3,22:57:39.05|328.95,-29:37:20.05|-164.67,1.18,2000,0
Scheat,f|S|M2,23:03:46.46|187.65,28:04:58.03|136.93,2.49,2000,0
Markab,f|S|B9,23:04:45.65|60.40,15:12:18.96|-41.30,2.48,2000,0
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

    out = [0,0,0,0,0,0,0]
    obs = ephem.Observer()
    latitude = ephem.degrees('%s:00:00.0' %lat)
    obs.lat = latitude
    d = ephem.date(date - 30 * ephem.second)    # search from 30 seconds before midnight
    obs.date = d
    obs.pressure = 0
    s = ephem.Sun(obs)
    s.compute(d)
    r = s.radius

    obs.horizon = ephem.degrees('-12')+r	# Nautical twilight ...
    try:
        out[0] = time(obs.next_rising(s))	# begin
    except:
        out[0] = '--:--'
    obs.date = d
    try:
        out[6] = time(obs.next_setting(s))	# end
    except:
        out[6] = '--:--'
#-----------------------------------------------------------
    obs.horizon = ephem.degrees('-6')+r		# Civil twilight...
    obs.date = d
    try:
        out[1] = time(obs.next_rising(s))	# begin
    except:
        out[1] = '--:--'
    obs.date = d
    try:
        out[5] = time(obs.next_setting(s))	# end
    except:
        out[5] = '--:--'
#-----------------------------------------------------------
    obs.horizon = '-0:34'
    obs.date = d
    try:
        out[2] = time(obs.next_rising(s))	# sunrise
    except:
        out[2] = '--:--'
    obs.date = d
    try:
        out[4] = time(obs.next_setting(s))	# sunset
    except:
        out[4] = '--:--'
#-----------------------------------------------------------
    obs.date = d
    out[3] = time(obs.next_transit(s))
    
    return out

def moonrise(date,lat):
    # returns moonrise and moonset for the given date and latitude plus next 2 days:
    #    rise day 1, rise day 2, rise day 3, set day 1, set day 2, set day 3

    out  = ['--:--','--:--','--:--','--:--','--:--','--:--']	# first event
    out2 = ['--:--','--:--','--:--','--:--','--:--','--:--']	# second event on same day (rare)
    obs = ephem.Observer()
    latitude = ephem.degrees('%s:00:00.0' %lat)
    obs.lat = latitude
    obs.pressure = 0
    m = ephem.Moon(obs)
    obs.horizon = '-0:34'

    d = ephem.date(date - 30 * ephem.second)
    obs.date = d
    m.compute(d)

    # Moonrise/Moonset on 1st. day ...
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
    # Moonrise/Moonset on 2nd. day ...
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
    # Moonrise/Moonset on 3rd. day ...
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

