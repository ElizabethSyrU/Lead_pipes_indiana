# -*- coding: utf-8 -*-
"""
Created on Sat May  8 21:44:00 2021

@author: Elizabeth
"""

import pandas as pd
import geopandas
from shapely.geometry import Point

#files needed to run this script
#file outputs from this script

lsl = pd.read_csv('lsl.csv')

geometry = [Point(xy) for xy in zip(lsl['long'],lsl['lat'])]

crs = {'init':'epsg:2965'}

lsl_geo = geopandas.GeoDataFrame(lsl,crs=crs,geometry=geometry)

lsl_geo.to_file('joined.gpkg',layer='IndianaPipes',driver='GPKG')#maybe have a different name

#%%

#county geodataframe, make sure to set crs

counties = geopandas.read_file('zip://tl_2017_us_county.zip')

counties = counties.query('STATEFP == "18"')
#this selects the counties in Indiana; there sould now be 92 entries in the counties geodataframe

#counties = counties['COUNTYFP','GEOID','NAME','INTPTLAT','INTPTLON','geometry']
#figure out how to drop extra columns in geodataframe

#census_data = geopandas.read_file('census_data.csv')

#counties = counties.merge(census_data,how='left',left_on='COUNTYFP',right_on='county',indicator=True,validate='1:1')
#appear to be having trouble merging dataframe onto geodataframe, do this in QGIS?
#print(counties['_merge'].value_counts())
#all 92 values should be in the 'both' category
#drop some columns

counties = counties.to_crs(epsg='2965')

#counties.to_file('joined.gpkg',layer='counties',drive='GPKG')
#get this into the geopackage as a layer somehow?

#%%

pipes_by_county = geopandas.overlay(counties,lsl_geo,how='contains')

pipes_by_county.to_file('pipes_by_county.gpkg',layer='Lead_Pipes_Census',driver='GPKG')

#read this out to a file and see if you can load it into QGIS

#join with block groups? better for scatter? (would need block group level data in census data api)

#%%

#geopackage files with layers for pipes and counties
#what other work do I need to do for 
#adj for pop density, not just total pop
