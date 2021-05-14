# -*- coding: utf-8 -*-
"""
Created on Thu May  6 11:43:37 2021

@author: Elizabeth
"""
#This script examines some aspects of the Indiana survey data and simplifies the
#lsl.csv file so it is easier to use for the purpose of finding the 
import pandas as pd

lsl = pd.read_csv('lead_service_lines.csv')
#read in the merged data

rename = {'Responded to State Survey?':'respondent',
          '# with Lead Service Line':'num_lsl',
          '% with Lead Service Line':'pct_lsl',
          'Data Source':'data_source',
          'Latitude':'lat',
          'Longitude':'long',
          'SDWIS Total # of Service Connections':'tot_num_serv_connects_sdwis',
          'SDWIS LCR 90th Percentile Sample (ppm)':'LCR_90thpctile',
          'Total Number of Service Connections':'tot_num_serv_connects',
          'Total Number of Service Lines with Lead Portions':'tot_num_sl_w_lead',
          'No Lead Portion - Number of Service Connections':'no_lead_serv_connects',
          'Service Line Material is Unknown - Number of Service Connection':'unk_mat_serv_connects',
          'Lead Gooseneck Only - Number of Service Connections':'lead_gooseneck_serv_connects',
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
#selects columns of interest

#%%

for c in select_cols:
    print(lsl[c].value_counts())
#this for loop helps establish values and ranges which inform future decisions in analysis
#For example, we can see how many utilities responded to the survey, that most of
#the pipes between the watermain and shut off are owned by a public water system or municipality
#while most of the pipes between the shut off and the house are owned by the resident, and that
#most of the locations of pipes containg lead are estimates instead of records but utilites
#still generally have high confidence in those estimates.
    #note: for ownership: P - Public Water System; M - Muninicipality, R - Resident, U - Unknown
    #note 2: there is some data clean up to do before we use these for analysis; for example
    # there is one confidence level of 16 despite it being a 1-10 scale. Also, there are
    #a variety of ways of reporting that some information is based on estimates while some is based
    #on records. Since analyzing this further is beyond the scope of this project, these 
    #adjustments are not made here

#%%

lsl['pct_lsl_calc'] = (100*lsl['tot_num_sl_w_lead']/lsl['tot_num_serv_connects']).round(2)
#used the values I did to calculate the percent of service lines that contain lead
#because they are from the same data set (Indiana survey, not EPA survey); also these were integers
#did this because reported percent is a string
#reported and calculated percents similar; discrepancies are probably due to different numbers between
#the different data sets used

print(lsl['pct_lsl_calc'])

#%%

owner_agg_watermain = lsl['lead_btwn_watermain_shutoff'].groupby(lsl['owner_btwn_watermain_shutoff']).sum()
owner_agg_house = lsl['lead_btwn_shutoff_house'].groupby(lsl['owner_btwn_shutoff_house']).sum()

print('The number of pipes owned by Muninicipalites, Residents,and Public Water Systems between the watermain and the water shut off is:')
print(owner_agg_watermain)

print('The number of pipes owned by Muninicipalites, Residents,and Public Water Systems between the water shut off and the house is:')
print(owner_agg_house)

lsl.to_csv('lsl.csv')#creats a csv the entire dataframe

#%%

response = lsl.groupby(lsl['respondent'])#now what can I do with this?
yes = 449 #figure out how to do this in a way that is not 
#response = lsl['respondent'].query('respondent == "Yes"')
pct_response = 100 * yes/lsl['respondent'].count()
print('The percentage of utilities that responded:',pct_response.round(2))


#%%

lsl_layer = lsl[['lat','long','tot_num_serv_connects_sdwis','tot_num_serv_connects',
                 'tot_num_sl_w_lead','no_lead_serv_connects','unk_mat_serv_connects',
                 'pct_lsl_calc']]
lsl_layer.to_csv('lsl_layer.csv')
#writes a csv file with only the data used in the geographic analysis
