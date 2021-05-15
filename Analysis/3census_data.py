# -*- coding: utf-8 -*-
"""
Created on Sat May  8 15:00:19 2021

@author: Elizabeth
"""
#The purpose of this script is to obtain census data to that will be used to 
#identify the poverty rate of people most affected by lead in the service pipes
#
import pandas as pd
import requests

api= 'https://api.census.gov/data/2017/acs/acs5'
#get census data from 5 year estimates for 2017 to match the year for the Indiana pipe data.
#5 year data is more accurate and the pipes have been there for a while so there's no reason to use 1 year data.

var_string = 'B06011_001E,B17020_001E,B17020_002E'
#variables retrieved from the census describe later in this script
for_clause = 'county:*' #retrieve data for all counties in the state
in_clause = 'state:18'#retrieve data only for state of Indiana
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

census_data = census_data.rename({'B06011_001E':'med_income','B17020_001E':'pov_stat_pop',
                                  'B17020_002E':'below_pov_line_prev_yr'},
                                 axis='columns')
#med_income is the median income for the county
#pov_stat_pop is the total population of the county as recorded for the poverty status variable
#below_pov_line_prev_yr is the number of people who had income below the poverty line in the previous year

census_data[['med_income','pov_stat_pop','below_pov_line_prev_yr']] = census_data[['med_income','pov_stat_pop','below_pov_line_prev_yr']].astype(int)
#sets all columns listed to integers

census_data['pov_rate'] = (100*census_data['below_pov_line_prev_yr']/census_data['pov_stat_pop']).round(2)
print(census_data['pov_rate'])
#calculates and prints the poverty rate for each county

census_data['GEOID'] = census_data['state']+census_data['county']
#creating this GEOID makes it easier to join to the tiger line file in QGIS
census_data = census_data.set_index('GEOID')#GEOID functions better as an index for our purposes

census_data.to_csv("census_data.csv")
