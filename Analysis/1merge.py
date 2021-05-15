# -*- coding: utf-8 -*-
"""
Created on Wed May  5 21:30:06 2021

@author: Elizabeth
"""

import pandas as pd

survey = pd.read_csv('Indiana-LSL-Data-for-Interactive-Map_EDF.csv')
survey.columns = survey.iloc[0]
survey = survey.drop(survey.index[0])

#%%

mapping_data = pd.read_csv('EDF_Mapping_data.csv')
mapping_data.columns = mapping_data.iloc[0]
mapping_data = mapping_data.drop(mapping_data.index[0])

#%%

lsl = mapping_data.merge(survey,
                         how='outer',
                         left_on='SDWIS PWS ID',
                         right_on='PWSID',
                         indicator=True)
#not 1:1, is this a concern?
#LSL has one more line than mapping data when left join is used, is this a concern?

print(lsl['_merge'].value_counts())

lsl = lsl.drop(['Full Address','SDWIS PWS ID','PWSID','System Name','_merge'],axis='columns')
#drops columns that will not be used later

lsl.to_csv('lead_service_lines.csv',index=False)
#right only = 6 for outer join
#figure out what data is different between joined data and original data