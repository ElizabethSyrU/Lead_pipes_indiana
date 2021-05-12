# -*- coding: utf-8 -*-
"""
Created on Sat May  8 15:00:19 2021

@author: Elizabeth
"""

import pandas as pd
import requests

api= 'https://api.census.gov/data/2017/acs/acs5'
#get census data from 5 year estimates for 2017 to match the year for the Indiana pipe data.
#5 year data is more accurate and the pipes have been there for a while so there's no reason to use 1 year data.

var_string = 'NAME,B02001_001E,B06011_001E,B17020_001E,B17020_002E'
#B02001_002E,B05010_001E,B05010_003E,B06012_001E,B06012_002E' (may use these variables in later anaysis, but cutting them for convenience now)
for_clause = 'county:*'
in_clause = 'state:18'
key_value = '2515f19444d8d046ca99087260217e11d73c37f1'

payload = {'get':var_string,
           'for':for_clause,
           'in':in_clause,
           'key':key_value}

response = requests.get(api,payload)

if response.status_code == 200:
    print('Request Successful')
else:
    print(response.status_code)
    print(response.text)
    assert False

row_list = response.json()

colnames = row_list[0]
datarows = row_list[1:]

census_data = pd.DataFrame(columns=colnames,data=datarows)

#%%

census_data = census_data.rename({'B02001_001E':'tot_pop',#'B02001_002E':'white',
                                  #'B05010_001E':'tot_pov_ratio','B05010_003E':'pov_ratio_under_1',
                                  #'B06012_001E':'tot_pov_prev_yr','B06012_002E':'under_pov_line_prev_yr'
                                  'B06011_001E':'med_income','B17020_001E':'pov_stat_pop',
                                  'B17020_002E':'below_pov_line_prev_yr'},
                                 axis='columns')

#explain what data was pulled by explaining the column names
census_data[['med_income','tot_pop','pov_stat_pop','below_pov_line_prev_yr']] = census_data[['med_income','tot_pop','pov_stat_pop','below_pov_line_prev_yr']].astype(int)

census_data['pov_rate'] = (100*census_data['below_pov_line_prev_yr']/census_data['pov_stat_pop']).round(2)
print(census_data['pov_rate'])

census_data['GEOID'] = census_data['state']+census_data['county']
#makes it easier to join in QGIS

#census_data = census_data.drop(['state','county'],axis='columns')

census_data.set_index('NAME') #do I actually want this as the index? or do I want a GEOID, GEOID would probably be better for mapping later
census_data.to_csv("census_data.csv")
