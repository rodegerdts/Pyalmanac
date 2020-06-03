#!/usr/bin/env python3
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

ephem_sun     = ephem.Sun()
ephem_moon    = ephem.Moon()
ephem_venus   = ephem.Venus()
ephem_mars    = ephem.Mars()
ephem_jupiter = ephem.Jupiter()
ephem_saturn  = ephem.Saturn()
#degree_sign= u'\N{DEGREE SIGN}'

#----------------------
#   internal methods
#----------------------

def hhmm(date):
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
    time = '{:02d}:{:02d}'.format(hr,min)    # time = "%02d:%02d" %(hr,min)
#    return time, nextday
    # NOTE: this function could easily return the information that rounding
    #       flipped into the next day, however this is not required here.
    return time

def nadeg(rad, fixedwidth=1):
    # changes ephem.angle (rad) to the format usually used in the nautical almanac (ddd°mm.m) and returns a string object.
	# the optional argument specifies the minimum width for degrees (only)
    theminus = ""
    if rad < 0:
    	theminus = '-'
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
        gm = "{}{:02d}$^\circ${:04.1f}".format(theminus,di,mf)
    else:
        if fixedwidth == 3:
            gm = "{}{:03d}$^\circ${:04.1f}".format(theminus,di,mf)
        else:
            gm = "{}{}$^\circ${:04.1f}".format(theminus,di,mf)
    return gm

def flag_msg(msg):
    if config.logfileopen:
        # if open - write to log file
        config.writeLOG(msg + '\n')
    else:
        # otherwise - print to console
        print(msg)
    return

#-------------------------------
#   Sun and Moon calculations
#-------------------------------

def sunmoon(date):          # used in suntab(m), sunmoontab(m)
    # returns ephemrerids for sun and moon.
    
    #Sun        gha dec
    #Moon       gha v dec d hp

    obs = ephem.Observer()
    obs.date = date
    
    #Sun
    ephem_sun.compute(date,epoch=date)
    deg = ephem.degrees(obs.sidereal_time()-ephem_sun.g_ra).norm
    ghas = nadeg(deg)
    degs = ephem_sun.g_dec
    decs = nadeg(degs,2)
    
    #Moon
    ephem_moon.compute(date,epoch=date)
    deg = ephem.degrees(obs.sidereal_time()-ephem_moon.g_ra).norm
    gham = nadeg(deg)
    degm = ephem_moon.g_dec
    decm = nadeg(degm,2)
    
    #calculate the moons horizontal paralax
    deg = ephem.degrees(ephem_moon.radius/0.272805950305)
    hp = "{:0.1f}'".format(deg*360*30/ephem.pi)
    
    #calculate v and d by advancing the time with one hour.
    ephem_moon.compute(date-0.5*ephem.hour,epoch=date-0.5*ephem.hour)
    obs.date = date - 0.5 * ephem.hour
    rgha = ephem.degrees(obs.sidereal_time()-ephem_moon.g_ra).norm
    rdec = ephem_moon.g_dec
    ephem_moon.compute(date+0.5*ephem.hour,epoch=date+0.5*ephem.hour)
    obs.date = date + 0.5 * ephem.hour
    rghap = ephem.degrees(obs.sidereal_time()-ephem_moon.g_ra).norm
    deg = ephem.degrees(ephem.degrees(rghap-rgha).norm-ephem.degrees('14:19:00'))
    vm = "{:0.1f}'".format(deg*360*30/ephem.pi)
    deg = ephem.degrees(ephem_moon.g_dec-rdec)
    dm = "{:0.1f}'".format(deg*360*30/ephem.pi)
    
    # degs, degm have been added for the sunmooontab function
    return ghas,decs,gham,vm,decm,dm,hp,degs,degm

##NEW##
def sun_moon_SD(date):      # used in suntab(m), sunmoontab(m)
    obs = ephem.Observer()
    obs.date = date
    
    #Sun
    # compute semi-diameter of sun and sun's declination change per hour (in minutes)
    ephem_sun.compute(date)
    dec = ephem_sun.g_dec
    ephem_sun.compute(date+ephem.hour)
    obs.date = date+ephem.hour
    deg = ephem.degrees(ephem_sun.g_dec-dec)
    ds = "{:0.1f}".format(deg*360*30/ephem.pi)
    sds = "{:0.1f}".format(ephem_sun.radius*360*30/ephem.pi)
    
    #Moon
    # compute semi-diameter of moon (in minutes)
    ephem_moon.compute(date)
    sdm = "{:0.1f}".format(ephem_moon.radius*360*30/ephem.pi)
    
    return ds,sds,sdm

#------------------------------------------------
#   Venus, Mars, Jupiter & Saturn calculations
#------------------------------------------------

def planetsGHA(date):       # used in planetstab(m)
    # this function returns a tuple of strings with ephemerids in the format used by the nautical almanac.
    
    # following are objects and their values:
    #Aries      gha
    #Venus      gha dec
    #Mars       gha dec
    #Jupiter    gha dec
    #Saturn     gha dec

    obs = ephem.Observer()
    obs.date = date
    
    #Aries, First Point of
    deg = ephem.degrees(obs.sidereal_time()).norm
    ghaa = nadeg(deg)
    
    #Venus
    ephem_venus.compute(date,epoch=date)
    deg = ephem.degrees(obs.sidereal_time()-ephem_venus.g_ra).norm
    ghav = nadeg(deg)
    degv = ephem_venus.g_dec
    decv = nadeg(degv,2)
    
    #Mars
    ephem_mars.compute(date,epoch=date)
    deg = ephem.degrees(obs.sidereal_time()-ephem_mars.g_ra).norm
    ghamars = nadeg(deg)
    degmars = ephem_mars.g_dec
    decmars = nadeg(degmars,2)
    
    #Jupiter
    ephem_jupiter.compute(date,epoch=date)
    deg = ephem.degrees(obs.sidereal_time()-ephem_jupiter.g_ra).norm
    ghaj = nadeg(deg)
    degj = ephem_jupiter.g_dec
    decj = nadeg(degj,2)
    
    #Saturn
    ephem_saturn.compute(date,epoch=date)
    deg = ephem.degrees(obs.sidereal_time()-ephem_saturn.g_ra).norm
    ghasat = nadeg(deg)
    degsat = ephem_saturn.g_dec
    decsat = nadeg(degsat,2)

    # degv, degmars, degj, degsat have been added for the planetstab function
    return ghaa,ghav,decv,ghamars,decmars,ghaj,decj,ghasat,decsat,degv,degmars,degj,degsat

def vdm_planets(date):      # used in planetstab(m)
    # compute v (GHA correction), d (Declination correction), m (magnitude of planet)

    obs = ephem.Observer()
    obs.date = date
    
    #Venus
    obs.date = date
    ephem_venus.compute(date)
    gha = ephem.degrees(obs.sidereal_time()-ephem_venus.g_ra).norm
    dec = ephem_venus.g_dec
    ephem_venus.compute(date+ephem.hour)
    obs.date = date+ephem.hour
    ghap = ephem.degrees(obs.sidereal_time()-ephem_venus.g_ra).norm
    deg = ephem.degrees(ghap-gha).norm-ephem.degrees('15:00:00')
    vvenus = "{:0.1f}".format(deg*360*30/ephem.pi)
    deg = ephem.degrees(ephem_venus.g_dec-dec)
    dvenus = "{:0.1f}".format(deg*360*30/ephem.pi)
    mvenus = "{:0.1f}".format(ephem_venus.mag)
    
    #Mars
    obs.date = date
    ephem_mars.compute(date)
    gha = ephem.degrees(obs.sidereal_time()-ephem_mars.g_ra).norm
    dec = ephem_mars.g_dec
    ephem_mars.compute(date+ephem.hour)
    obs.date = date+ephem.hour
    ghap = ephem.degrees(obs.sidereal_time()-ephem_mars.g_ra).norm
    deg = ephem.degrees(ephem.degrees(ghap-gha).norm-ephem.degrees('15:00:00'))
    vmars = "{:0.1f}".format(deg*360*30/ephem.pi)
    deg = ephem.degrees(ephem_mars.g_dec-dec)
    dmars = "{:0.1f}".format(deg*360*30/ephem.pi)
    mmars = "{:0.1f}".format(ephem_mars.mag)
    
    #Jupiter
    obs.date = date
    ephem_jupiter.compute(date)
    gha = ephem.degrees(obs.sidereal_time()-ephem_jupiter.g_ra).norm
    dec = ephem_jupiter.g_dec
    ephem_jupiter.compute(date+ephem.hour)
    obs.date = date+ephem.hour
    ghap = ephem.degrees(obs.sidereal_time()-ephem_jupiter.g_ra).norm
    deg = ephem.degrees(ephem.degrees(ghap-gha).norm-ephem.degrees('15:00:00'))
    vjup = "{:0.1f}".format(deg*360*30/ephem.pi)
    deg = ephem.degrees(ephem_jupiter.g_dec-dec)
    djup = "{:0.1f}".format(deg*360*30/ephem.pi)
    mjup = "{:0.1f}".format(ephem_jupiter.mag)
    
    #Saturn
    obs.date = date
    ephem_saturn.compute(date)
    gha = ephem.degrees(obs.sidereal_time()-ephem_saturn.g_ra).norm
    dec = ephem_saturn.g_dec
    ephem_saturn.compute(date+ephem.hour)
    obs.date = date+ephem.hour
    ghap = ephem.degrees(obs.sidereal_time()-ephem_saturn.g_ra).norm
    deg = ephem.degrees(ephem.degrees(ghap-gha).norm-ephem.degrees('15:00:00'))
    vsat = "{:0.1f}".format(deg*360*30/ephem.pi)
    deg = ephem.degrees(ephem_saturn.g_dec-dec)
    dsat = "{:0.1f}".format(deg*360*30/ephem.pi)
    msat = "{:0.1f}".format(ephem_saturn.mag)
    
    return vvenus,dvenus,mvenus,vmars,dmars,mmars,vjup,djup,mjup,vsat,dsat,msat

#-----------------------------------------
#   Aries & planet transit calculations
#-----------------------------------------

def ariestransit(date):     # used in planetstab(m)
    # returns transit time of aries for given date

    obs = ephem.Observer()
    obs.date = ephem.date(date)+1
    sid = obs.sidereal_time()
    trans = ephem.hours(2*math.pi-sid/1.00273790935)
#    obs.date = date + trans/(2*math.pi) #turns ephem.angle (time) into ephem date
    hhmm = str(trans)[0:5]	# can return "h:mm:"
    if hhmm[1:2] == ':':	# check if single digit hours
        hhmm = '0' + hhmm[0:4]
    return hhmm
    
def planetstransit(date):   # used in starstab
    #returns SHA and meridian passage for the navigational planets

    obs = ephem.Observer()
    
    obs.date = date
    ephem_venus.compute(date)
    vsha = nadeg(2*math.pi-ephem.degrees(ephem_venus.g_ra).norm)
    vtrans = hhmm(obs.next_transit(ephem_venus))
    hpvenus = "{:0.1f}".format((math.tan(6371/(ephem_venus.earth_distance*149597870.7)))*60*180/math.pi)
    
    obs.date = date
    ephem_mars.compute(date)
    marssha = nadeg(2*math.pi-ephem.degrees(ephem_mars.g_ra).norm)
    marstrans = hhmm(obs.next_transit(ephem_mars))
    hpmars = "{:0.1f}".format((math.tan(6371/(ephem_mars.earth_distance*149597870.7)))*60*180/math.pi)

    obs.date = date
    ephem_jupiter.compute(date)
    jsha = nadeg(2*math.pi-ephem.degrees(ephem_jupiter.g_ra).norm)
    jtrans = hhmm(obs.next_transit(ephem_jupiter))
    
    obs.date = date
    ephem_saturn.compute(date)
    satsha = nadeg(2*math.pi-ephem.degrees(ephem_saturn.g_ra).norm)
    sattrans = hhmm(obs.next_transit(ephem_saturn))
    
    return [vsha,vtrans,marssha,marstrans,jsha,jtrans,satsha,sattrans,hpmars,hpvenus]

#-----------------------
#   star calculations
#-----------------------

def stellar(date):          # used in starstab
    # returns a list of lists with name, SHA and Dec for all navigational stars for epoch of date.
    out = []
    for line in db.strip().split('\n'):
        st = ephem.readdb(line)
        st.compute(date+0.5)    # calculate at noon
        out.append([st.name,nadeg(2*math.pi-ephem.degrees(st.g_ra).norm),nadeg(st.g_dec)])
    return out

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

#--------------------
#   TWILIGHT table
#--------------------

# create a list of 'sun above/below horizon' states per Latitude per Normal/Civil/Naut...
#sunvisible = [[None]*3 for i in range(31)]	# sunvisible[0][0] up to sunvisible[30][2]

def twilight(date, lat, hemisph):   # used in twilighttab (section 1)
    # Returns for given date and latitude(in full degrees):
    # naut. and civil twilight (before sunrise), sunrise, meridian passage, sunset, civil and nautical twilight (after sunset).
    # NOTE: 'twilight' is only called for every third day in the Full Almanac...
    #       ...therefore daily tracking of the sun state is impossible.

    mth = ephem.date(date).triple()[1]
    out = [0,0,0,0,0,0,0]
    obs = ephem.Observer()
    latitude = ephem.degrees('{}:00:00.0'.format(lat))
    obs.lat = latitude
    d = ephem.date(date - 30 * ephem.second)    # search from 30 seconds before midnight
    obs.date = d
    obs.pressure = 0
    s = ephem.Sun(obs)
    s.compute(d)
    r = s.radius

    obs.horizon = ephem.degrees('-12')+r	# Nautical twilight ...
    try:
        out[0] = hhmm(obs.next_rising(s))	# begin
    except:
        out[0] = '--:--'
    obs.date = d
    try:
        out[6] = hhmm(obs.next_setting(s))	# end
    except:
        out[6] = '--:--'
    if out[0] == '--:--' and out[6] == '--:--':	# if neither begin nor end...
        if config.search_next_rising_sun:
            yn = getsunstate(date, lat, 2)      # ... get the sun state
        else:
            yn = midnightsun(mth, hemisph)
        out[0] = yn
        out[6] = yn
#-----------------------------------------------------------
    obs.horizon = ephem.degrees('-6')+r		# Civil twilight...
    obs.date = d
    try:
        out[1] = hhmm(obs.next_rising(s))	# begin
    except:
        out[1] = '--:--'
    obs.date = d
    try:
        out[5] = hhmm(obs.next_setting(s))	# end
    except:
        out[5] = '--:--'
    if out[1] == '--:--' and out[5] == '--:--':	# if neither begin nor end...
        if config.search_next_rising_sun:
            yn = getsunstate(date, lat, 1)      # ... get the sun state
        else:
            yn = midnightsun(mth, hemisph)
        out[1] = yn
        out[5] = yn
#-----------------------------------------------------------
    obs.horizon = '-0:34'
    obs.date = d
    try:
        out[2] = hhmm(obs.next_rising(s))	# sunrise
    except:
        out[2] = '--:--'
    obs.date = d
    try:
        out[4] = hhmm(obs.next_setting(s))	# sunset
    except:
        out[4] = '--:--'
    if out[2] == '--:--' and out[4] == '--:--':	# if neither sunrise nor sunset...
        if config.search_next_rising_sun:
            yn = getsunstate(date, lat, 0)      # ... get the sun state
        else:
            yn = midnightsun(mth, hemisph)
        out[2] = yn
        out[4] = yn
#-----------------------------------------------------------
    obs.date = d
    out[3] = hhmm(obs.next_transit(s))
    
    return out

##NEW##
def getsunstate(d, lat, h):
    # populate the sun state (visible or not) for the specified date & latitude
    # note: the first parameter 'd' is an ephem date at midnight
    # note: getsunstate is called when there is neither a sunrise nor a sunset on 'd'
    i = config.lat.index(lat)
    latitude = ephem.degrees('{}:00:00.0'.format(lat))
    obs = ephem.Observer()
    #d = ephem.date(date - 30 * ephem.second)
    obs.pressure = 0
    s = ephem.Sun(obs)
    err = False
    obs.date = d
    obs.lat = latitude
    s.compute(d)
    sunup = False

    if h == 0:
        obs.horizon = '-0:34'					# sunrise/sunset
    if h == 1:
        r = s.radius
        obs.horizon = ephem.degrees('-6')+r		# Civil twilight...
    if h == 2:
        r = s.radius
        obs.horizon = ephem.degrees('-12')+r	# Nautical twilight...
        
    nextrising = d + 100.0	# in case sunset but no next sunrise
    nextsetting = d + 100.0	# in case sunrise but no next sunset

    try:
        nextrising  = obs.next_rising(s)
    except ephem.NeverUpError:
        err = True
        #print("nr NeverUp",i,h,d)
        sunup = False
        #sunvisible[i][h] = False
    except ephem.AlwaysUpError:
        err = True
        #print("nr AlwaysUp",i,h,d)
        sunup = True
        #sunvisible[i][h] = True
    except Exception:
        flag_msg("Oops! sun nextR {}: {} occured, line: {}".format(i,sys.exc_info()[1],sys.exc_info()[2].tb_lineno))
        #sys.exc_clear()		# only in Python 2

    obs.date = d
    if not(err):	# note - 'nextrising' above *should* fail
        try:
            nextsetting = obs.next_setting(s)
        except ephem.NeverUpError:
            err = True
            #print("ns NeverUp",i,h,d)
            sunup = False
            #sunvisible[i][h] = False
        except ephem.AlwaysUpError:
            err = True
            #print("ns AlwaysUp",i,h,d)
            sunup = True
            #sunvisible[i][h] = True
        except Exception:
            flag_msg("Oops! sun nextS {}: {} occured, line: {}".format(i,sys.exc_info()[1],sys.exc_info()[2].tb_lineno))
            #sys.exc_clear()		# only in Python 2

    if not(err):	# note - "err == True" *is* expected...
        # however if we found both, which occured first?
        sunup = False
        #sunvisible[i][h] = False
        if nextrising > nextsetting:
            sunup = True
            #sunvisible[i][h] = True
        #print("{}".format(i), nextrising, nextsetting, sunvisible[i][h])

    # return the current sunstate
    out = '--:--'
    if sunup == True:
        out = r'\begin{tikzpicture}\draw (0,0) rectangle (12pt,4pt);\end{tikzpicture}'
    else:
        out = r'\rule{12Pt}{4Pt}'
    return out

##NEW##
def midnightsun(mth, hemisph):
    # simple way to fudge whether the sun is up or down when there's no
    # sunrise or sunset on a day depending on the month and hemisphere only.
    # Note: this works for the chosen latitudes to be calculated.

    sunup = False
    if mth > 3 and mth < 10:    # if April to September inclusive
        sunup = True
    if hemisph == 'S':
        sunup = not(sunup)
    if sunup == True:
        out = r'''\begin{tikzpicture}\draw (0,0) rectangle (12pt,4pt);\end{tikzpicture}'''
    else:
        out = r'''\rule{12Pt}{4Pt}'''
    return out

#-------------------------
#   MOONRISE/-SET table
#-------------------------

# create a list of 'moon above/below horizon' states per Latitude...
#    None = unknown; True = above horizon (visible); False = below horizon (not visible)
moonvisible = [None] * 31       # moonvisible[0] up to moonvisible[30]

def moonrise_set(date, lat):    # used in twilighttab (section 2)
    # returns moonrise and moonset for the given date and latitude plus next 2 days:
    #    rise day 1, rise day 2, rise day 3, set day 1, set day 2, set day 3
    # Additionally it also tracks the current state of the moon (above or below horizon)

    i = config.lat.index(lat)
    out  = ['--:--','--:--','--:--','--:--','--:--','--:--']	# first event
    out2 = ['--:--','--:--','--:--','--:--','--:--','--:--']	# second event on same day (rare)

    obs = ephem.Observer()
    latitude = ephem.degrees('{}:00:00.0'.format(lat))
    obs.lat = latitude
    obs.pressure = 0
    obs.horizon = '-0:34'
    d = ephem.date(date - 30 * ephem.second)    # search from 30 seconds before midnight
    obs.date = d
    m = ephem.Moon(obs)
    m.compute(d)
#-----------------------------------------------------------
    # Moonrise/Moonset on 1st. day ...
    try:
        firstrising = obs.next_rising(m)
        if firstrising-obs.date >= 1:
            raise ValueError('event next day')
        out[0] = hhmm(firstrising)		# note: overflow to 00:00 next day is correct here
        lastevent = firstrising
        moonvisible[i] = True
    except Exception:                   # includes NeverUpError and AlwaysUpError
        out[0] = '--:--'
        lastevent = 0

    if out[0] != '--:--':
        try:
            nextr = obs.next_rising(m, start=firstrising)
            if nextr-obs.date < 1:
                out2[0] = hhmm(nextr)   # note: overflow to 00:00 next day is correct here
                lastevent = nextr
        except UnboundLocalError:
            pass
        except ephem.NeverUpError:
            pass
        except ephem.AlwaysUpError:
            pass
        except Exception:
            flag_msg("Oops! {} occured, line: {}".format(sys.exc_info()[1],sys.exc_info()[2].tb_lineno))
            #sys.exc_clear()		# only in Python 2

    obs.date = d
    try:
        firstsetting = obs.next_setting(m)
        if firstsetting-obs.date >= 1:
            raise ValueError('event next day')
        out[3] = hhmm(firstsetting)		# note: overflow to 00:00 next day is correct here
        if firstsetting > lastevent:
            lastevent = firstsetting
            moonvisible[i] = False
    except Exception:                   # includes NeverUpError and AlwaysUpError
        out[3] = '--:--'

    if out[3] != '--:--':
        try:
            nexts = obs.next_setting(m, start=firstsetting)
            if nexts-obs.date < 1:
                out2[3] = hhmm(nexts)	# note: overflow to 00:00 next day is correct here
            if nexts > lastevent:
                moonvisible[i] = False
        except UnboundLocalError:
            pass
        except ephem.NeverUpError:
            pass
        except ephem.AlwaysUpError:
            pass
        except Exception:
            flag_msg("Oops! {} occured, line: {}".format(sys.exc_info()[1],sys.exc_info()[2].tb_lineno))
            #sys.exc_clear()		# only in Python 2

    if out[0] == '--:--' and out[3] == '--:--':	# if neither moonrise nor moonset...
        if moonvisible[i] == None:
            getmoonstate(d, lat)			# ...get moon state if unknown
        out[0] = moonstate(i)
        out[3] = moonstate(i)
#-----------------------------------------------------------
    # Moonrise/Moonset on 2nd. day ...
    d = ephem.date(date + 1 - 30 * ephem.second)
    obs.date = d
    m.compute(d)
    try:
        firstrising = obs.next_rising(m)
        if firstrising-obs.date >= 1:
            raise ValueError('event next day')
        out[1] = hhmm(firstrising)		# note: overflow to 00:00 next day is correct here
        lastevent = firstrising
        moonvisible[i] = True
    except Exception:                   # includes NeverUpError and AlwaysUpError
        out[1] = '--:--'
        lastevent = 0

    if out[1] != '--:--':
        try:
            nextr = obs.next_rising(m, start=firstrising)
            if nextr-obs.date < 1:
                out2[1] = hhmm(nextr)	# note: overflow to 00:00 next day is correct here
                lastevent = nextr
        except UnboundLocalError:
            pass
        except ephem.NeverUpError:
            pass
        except ephem.AlwaysUpError:
            pass
        except Exception:
            flag_msg("Oops! {} occured, line: {}".format(sys.exc_info()[1],sys.exc_info()[2].tb_lineno))
            #sys.exc_clear()		# only in Python 2

    obs.date = d
    try:
        firstsetting = obs.next_setting(m)
        if firstsetting-obs.date >= 1:
            raise ValueError('event next day')
        out[4] = hhmm(firstsetting)		# note: overflow to 00:00 next day is correct here
        if firstsetting > lastevent:
            lastevent = firstsetting
            moonvisible[i] = False
    except Exception:                   # includes NeverUpError and AlwaysUpError
        out[4] = '--:--'

    if out[4] != '--:--':
        try:
            nexts = obs.next_setting(m, start=firstsetting)
            if nexts-obs.date < 1:
                out2[4] = hhmm(nexts)	# note: overflow to 00:00 next day is correct here
            if nexts > lastevent:
                moonvisible[i] = False
        except UnboundLocalError:
            pass
        except ephem.NeverUpError:
            pass
        except ephem.AlwaysUpError:
            pass
        except Exception:
            flag_msg("Oops! {} occured, line: {}".format(sys.exc_info()[1],sys.exc_info()[2].tb_lineno))
            #sys.exc_clear()		# only in Python 2

    if out[1] == '--:--' and out[4] == '--:--':	# if neither moonrise nor moonset...
        if moonvisible[i] == None:
            getmoonstate(d, lat)			# ...get moon state if unknown
        out[1] = moonstate(i)
        out[4] = moonstate(i)
#-----------------------------------------------------------
    # Moonrise/Moonset on 3rd. day ...
    d = ephem.date(date + 2 - 30 * ephem.second)
    obs.date = d
    m.compute(d)
    try:
        firstrising = obs.next_rising(m)
        if firstrising-obs.date >= 1:
            raise ValueError('event next day')
        out[2] = hhmm(firstrising)		# note: overflow to 00:00 next day is correct here
        lastevent = firstrising
        moonvisible[i] = True
    except Exception:                   # includes NeverUpError and AlwaysUpError
        out[2] = '--:--'
        lastevent = 0

    if out[2] != '--:--':
        try:
            nextr = obs.next_rising(m, start=firstrising)
            if nextr-obs.date < 1:
                out2[2] = hhmm(nextr)	# note: overflow to 00:00 next day is correct here
                lastevent = nextr
        except UnboundLocalError:
            pass
        except ephem.NeverUpError:
            pass
        except ephem.AlwaysUpError:
            pass
        except Exception:
            flag_msg("Oops! {} occured, line: {}".format(sys.exc_info()[1],sys.exc_info()[2].tb_lineno))
            #sys.exc_clear()		# only in Python 2

    obs.date = d
    try:
        firstsetting = obs.next_setting(m)
        if firstsetting-obs.date >= 1:
            raise ValueError('event next day')
        out[5] = hhmm(firstsetting)		# note: overflow to 00:00 next day is correct here
        if firstsetting > lastevent:
            lastevent = firstsetting
            moonvisible[i] = False
    except Exception:                   # includes NeverUpError and AlwaysUpError
        out[5] = '--:--'

    if out[5] != '--:--':
        try:
            nexts = obs.next_setting(m, start=firstsetting)
            if nexts-obs.date < 1:
                out2[5] = hhmm(nexts)	# note: overflow to 00:00 next day is correct here
            if nexts > lastevent:
                moonvisible[i] = False
        except UnboundLocalError:
            pass
        except ephem.NeverUpError:
            pass
        except ephem.AlwaysUpError:
            pass
        except Exception:
            flag_msg("Oops! {} occured, line: {}".format(sys.exc_info()[1],sys.exc_info()[2].tb_lineno))
            #sys.exc_clear()		# only in Python 2

    if out[2] == '--:--' and out[5] == '--:--':	# if neither moonrise nor moonset...
        if moonvisible[i] == None:
            getmoonstate(d, lat)			# ...get moon state if unknown
        out[2] = moonstate(i)
        out[5] = moonstate(i)

    return out, out2

##NEW##
def getmoonstate(d, lat):
    # populate the moon state (visible or not) for the specified date & latitude
    # note: the first parameter 'd' is already an ephem date 30 seconds before midnight
    # note: getmoonstate is called when there is neither a moonrise nor a moonset on 'd'

    i = config.lat.index(lat)
    latitude = ephem.degrees('{}:00:00.0'.format(lat))
    obs = ephem.Observer()
    #d = ephem.date(date - 30 * ephem.second)
    obs.pressure = 0
    obs.horizon = '-0:34'
    m = ephem.Moon(obs)
    err = False
    obs.date = d
    obs.lat = latitude
    m.compute(d)
    nextrising = d + 100.0	# in case moonset but no next moonrise
    nextsetting = d + 100.0	# in case moonrise but no next moonset

    try:
        nextrising  = obs.next_rising(m)
    except ephem.NeverUpError:
        err = True
        #print("nr NeverUp")
        moonvisible[i] = False
    except ephem.AlwaysUpError:
        err = True
        #print("nr AlwaysUp")
        moonvisible[i] = True
    except Exception:
        flag_msg("Oops! moon nextR {}: {} occured, line: {}".format(i,sys.exc_info()[1],sys.exc_info()[2].tb_lineno))
        #sys.exc_clear()		# only in Python 2

    obs.date = d
    if not(err):	# note - 'nextrising' above *should* fail
        try:
            nextsetting = obs.next_setting(m)
        except ephem.NeverUpError:
            err = True
            #print("ns NeverUp")
            moonvisible[i] = False
        except ephem.AlwaysUpError:
            err = True
            #print("ns AlwaysUp")
            moonvisible[i] = True
        except Exception:
            flag_msg("Oops! moon nextS {}: {} occured, line: {}".format(i,sys.exc_info()[1],sys.exc_info()[2].tb_lineno))
            #sys.exc_clear()		# only in Python 2

    if not(err):	# note - "err == True" *is* expected...
        # however if we found both, which occured first?
        moonvisible[i] = False
        if nextrising > nextsetting:
            moonvisible[i] = True
        #print("{}".format(i), nextrising, nextsetting, moonvisible[i])
    return

##NEW##
def moonstate(ndx):
    # return the current moonstate (if known)
    out = '--:--'
    if moonvisible[ndx] == True:
        #out = 'UP'
        #out = r'\framebox(12,4){}'
        #out = r'{\setlength{\fboxrule}{0.8pt}\setlength{\fboxsep}{0pt}\fbox{\makebox(12,4){}}}'
        #out = r'{\setlength{\fboxrule}{0.8pt}\fbox{\parbox[c][0pt]{0pt}{ }}}'
        #out = r'\includegraphics[scale=1.0]{./moonup.jpg}'
        out = r'\begin{tikzpicture}\draw (0,0) rectangle (12pt,4pt);\end{tikzpicture}'
    if moonvisible[ndx] == False:
        #out = 'DOWN'
        out = r'\rule{12Pt}{4Pt}'
    return out

#------------------------------
#   Equation of Time section
#------------------------------

def equation_of_time(date): # used in twilighttab (section 3)
    # returns equation of time, the sun's transit time, 
    # the moon's transit-, antitransit-time, age and percent illumination.
    # (Equation of Time = Mean solar time - Apparent solar time)

    py_date = date.tuple()
    py_obsdate = datetime.date(py_date[0], py_date[1], py_date[2])
    d = ephem.date(date - 30 * ephem.second)
    obs = ephem.Observer()
    obs.date = d
    ephem_sun.compute(d)
    ephem_moon.compute(d)
    transs = '--:--'
    antim  = '--:--'
    transm = '--:--'

    next_s_tr = obs.next_transit(ephem_sun,start=d)
    if next_s_tr - obs.date < 1:
        transs = hhmm(next_s_tr)

    next_m_atr = obs.next_antitransit(ephem_moon,start=d)
    if next_m_atr - obs.date < 1:
        antim = hhmm(next_m_atr)

    next_m_tr = obs.next_transit(ephem_moon,start=d)
    if next_m_tr - obs.date < 1:
        transm = hhmm(next_m_tr)

#-----------------------------
    obs = ephem.Observer()
    obs.date = date
    
    ephem_moon.compute(date+0.5)
    pct = int(round(ephem_moon.phase))   # percent of moon surface illuminated
    age = int(round((date+0.5)-ephem.previous_new_moon(date+0.5)))
    phase = ephem_moon.elong.norm+0.0    # moon phase as float (0:new to π:full to 2π:new)
    
    ephem_sun.compute(date-0.1)
    obs.date = date-0.1

    # round to the second; convert back to days
    x = round((obs.next_antitransit(ephem_sun)-date)*86400)*2*math.pi/86400
    eqt00 = ephem.hours(x)
    eqt00 = str(eqt00)[-8:-3]
    if x >= 0:
        eqt00 = r"\colorbox{{lightgray!80}}{{{}}}".format(eqt00)

    y = round((obs.next_transit(ephem_sun)-(date+0.5))*86400)*2*math.pi/86400
    eqt12 = ephem.hours(y)
    eqt12 = str(eqt12)[-8:-3]
    if y >= 0:
        eqt12 = r"\colorbox{{lightgray!80}}{{{}}}".format(eqt12)

    return eqt00,eqt12,transs,transm,antim,age,pct
