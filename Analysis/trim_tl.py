# -*- coding: utf-8 -*-
"""
Created on Fri May 14 19:32:36 2021

@author: Elizabeth
"""
#this script selects only the data necessary for the QGIS portion of the project
import geopandas

counties = geopandas.read_file('zip://tl_2017_us_county.zip')

counties = counties.query('STATEFP == "18"')

counties_gis = counties[['GEOID','NAME','INTPTLAT','INTPTLON','geometry']]

#need to read this out to something?