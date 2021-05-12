# -*- coding: utf-8 -*-
"""
Created on Thu May  6 11:43:37 2021

@author: Elizabeth
"""

import pandas as pd

lsl = pd.read_csv('lead_service_lines.csv')

rename = {'Responded to State Survey?':'respondent',
          '# with Lead Service Line':'num_lsl',#want spread, not value counts. do a scatter plot or some other plot
          '% with Lead Service Line':'pct_lsl',#use to map? Indiana already did that
          'Data Source':'data_source',
          'Full Address':'full_addr',#do I actually need this column?
          'Latitude':'lat',
          'Longitude':'long',
          'SDWIS Total # of Service Connections':'tot_num_serv_connects_sdwis',#scatter with pct lsl or #lsl or both!
          'SDWIS LCR 90th Percentile Sample (ppm)':'LCR_90thpctile',#not sure what this one means
          'System Name':'sys_name',#do I need this? different case but same as column water system
          'Total Number of Service Connections':'tot_num_serv_connects',#is this the same as tot_num_serv_connects_sdwis?
          'Total Number of Service Lines with Lead Portions':'tot_num_sl_w_lead',#box and whisker or histogram
          'No Lead Portion - Number of Service Connections':'no_lead_serv_connects',#do some kind of ratio and match it to the lat/long and map with pie charts?
          'Service Line Material is Unknown - Number of Service Connection':'unk_mat_serv_connects',
          'Lead Gooseneck Only - Number of Service Connections':'lead_gooseneck_serv_connects',#what is the gooseneck
          'Entire Service Line is Lead - Number of Service Connections':'lead_serv_line_serv_connects',
          'Lead only from Water Main to Property line, Curb or Shut-Off':'lead_btwn_watermain_shutoff',
          'Lead Only from the External Shut-off valve to home':'lead_btwn_shutoff_house',
          'Ownership from water main to external shut-off, curb or property':'owner_btwn_watermain_shutoff',
          'Ownership from curb, propertly line, or shut-off to home':'owner_btwn_shutoff_house',
          'E or R - No Lead Portion':'e_r_leadportion',#E means estimated and R means reported
          'E or R - Service line material is unknown':'e_r_slmat',
          'E or R - Lead goosneck only':'e_r_lead_gooseneck',
          'E or R - Entire Service Line is Lead from the Water Main to home':'e_r_lead_watermain',
          'E or R - Lead Only from Main to External Shut-off, curb or prope':'e_r_lead_maintoshutoff',
          'E or R - Lead Only from External Shut-off valve to home':'e_r_shutofftohouse',
          'E or R - Total Number of Service Connections':'e_r_num_serv_connects',
          'E or R - Total Number of Service lines with lead portions':'e_r_tot_sl_w_lead',
          'Confidence in Records - No Lead Portion':'conf_rec_no_lead',
          'Confidence in Records - Service line material is unknown':'conf_rec_mat_unk',
          'Confidence in Records - Lead gooseneck only':'conf_rec_lead_gooseneck',
          'Confidence in Records - Entire Service line is lead':'conf_rec_lead_servline',
          'Confidence in Records - Lead only from water main to property line or external shut-off':'conf_rec_lead_btwn_watermain_shutoff',
          'Confidence in Records - Lead only from external shut-off to home':'conf_rec_lead_btw_shutoff_house',
          'Confidence in Records - Total Number of Service Connection':'conf_rec_tot_num_serv_connects',
          'Confidence in Records - Total Number of service lines with lead':'conf_rec_tot_num_serv_lines_w_lead'}
#set index to ID#?
lsl = lsl.rename(rename,axis='columns')# makes columns easier to work with

lsl = lsl.drop('Unnamed: 0',axis='columns') #why is there an extra column?

#lsl.apply(pd.Series.value_counts) prints all value counts for all columns, is there a way to select certain columns?

#%%

select_cols = ['respondent','pct_lsl','unk_mat_serv_connects','lead_gooseneck_serv_connects',
               'lead_serv_line_serv_connects','lead_btwn_watermain_shutoff',
               'lead_btwn_shutoff_house','owner_btwn_watermain_shutoff','owner_btwn_shutoff_house',
               'e_r_leadportion','e_r_slmat','e_r_lead_gooseneck','e_r_lead_watermain',
               'e_r_lead_maintoshutoff','e_r_shutofftohouse','e_r_num_serv_connects',
               'e_r_tot_sl_w_lead','conf_rec_no_lead','conf_rec_mat_unk','conf_rec_lead_gooseneck',
               'conf_rec_lead_servline','conf_rec_lead_btwn_watermain_shutoff',
               'conf_rec_lead_btw_shutoff_house','conf_rec_tot_num_serv_connects',
               'conf_rec_tot_num_serv_lines_w_lead']

#%%

for c in select_cols:
    print(lsl[c].value_counts())#some of these value counts might be better as lengths, check this (actually, I just want to know how many are not 0, go through hw to figure out how to do that?)
#this for loop helps establish values and ranges which inform future decisions in analysis
#print(lsl['pct_lsl'].value_counts())
for c in lsl.columns:
    print(lsl[c].count())#figure out how to print column names along with this, make a dictionary or dataframe and print that (index of dataframe the column names)

#%%

#lsl = lsl['pct_lsl'].to_replace('unknown')
lsl['pct_lsl_calc'] = (100*lsl['tot_num_sl_w_lead']/lsl['tot_num_serv_connects']).round(2)
#used these because they are from the same data set (Indiana survey, not EPA survey); also these were integers
#did this because reported percent is a string and I didn't want to deal with it 
    #(some numbers, some strings, even the numbers are strings because they include % (fix this in the excel sheet?))
#reported and calculated percents similar
#get percent of pipes that are lead
#check variation in reporting number of pipes from EPA vs Indiana survey
print(lsl['pct_lsl_calc'])

#%%

owner_agg_watermain = lsl['lead_btwn_watermain_shutoff'].groupby(lsl['owner_btwn_watermain_shutoff']).sum()#this did work but now it's funky, not sure what's up
owner_agg_house = lsl['lead_btwn_shutoff_house'].groupby(lsl['owner_btwn_shutoff_house']).sum()


lsl.to_csv('lsl.csv')

#%%

response = lsl.groupby(lsl['respondent'])#now what can I do with this?
yes = 449 #figure out how to do this in a way that is not 
#response = lsl['respondent'].query('respondent == "Yes"')
pct_response = 100 * yes/lsl['respondent'].count()
print('The percentage of untilities that responded:',pct_response.round(2))


by_response = lsl['tot_num_serv_connects_sdwis'].groupby(lsl['respondent']).sum()
#total = lsl['tot_num_serv_connects_sdwis'].sum() #TypeError: can only concatenate str (not "int") to str
num_connections = by_response['Yes'] #/ (by_response['Yes']+by_response['No'])#number too big?
#drop SDWIS PWS ID, better done in merge


#%%

lsl_layer = lsl[['lat','long','tot_num_serv_connects_sdwis','tot_num_serv_connects',
                 'tot_num_sl_w_lead','no_lead_serv_connects','unk_mat_serv_connects',
                 'pct_lsl_calc']]
lsl_layer.to_csv('lsl_layer.csv')



#next step: response for rate for utilities vs response as % of total number of service connections
#maybe also get % of types of ownership, % of 