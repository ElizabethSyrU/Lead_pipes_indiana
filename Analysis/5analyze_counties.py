# -*- coding: utf-8 -*-
"""
Created on Tue May 11 20:19:38 2021

@author: Elizabeth
"""

import pandas as pd
import matplotlib.pyplot as plt

pipes_by_county = pd.read_csv('lsl_county.csv')

#%%

num_pipes_by_county = pipes_by_county[['tot_num_serv_connects','tot_num_sl_w_lead','unk_mat_serv_connects']].groupby(pipes_by_county['GEOID']).sum()
#gets the number of pipes by county
num_pipes_by_county['pct_lead'] = (num_pipes_by_county['tot_num_sl_w_lead']/num_pipes_by_county['tot_num_serv_connects'])*100
#calculates the percent of service lines that contain lead by county

#%%

census = pd.read_csv('census_data.csv')
merge = num_pipes_by_county.merge(census,on='GEOID',indicator=True)
#merges the census data onto the number of pipes by county dataframe

#%%

plt.figure()
ax = merge.plot.scatter('tot_num_sl_w_lead','pov_rate')
ax.set_title('Lead Pipes vs. Poverty Rate')
ax.set_xlabel('Number of Lead Pipes in the County')
ax.set_ylabel('Poverty Rate')
ax.figure.savefig('lead_pov_rate')
#not very interesting result, the counties with over 10,000 pipes take up most of
#the space and so the relationship between povery rate and lead pipes is unclear

#%%

to_drop = merge[merge['tot_num_sl_w_lead'] > 10000].index
#identify counties with less than 10000 lead pipes

to_scatter = merge.drop(to_drop)
#drop the counties with more than 10,000 pipes per county

to_drop = merge[merge['tot_num_sl_w_lead'] == 0].index
#remove 0 values to make graph more readable; non response rates, unknown materials, and utilities
    #mean there are many counties with no lead pipes which makes it difficult to read the graph

to_scatter = to_scatter.drop(to_drop)

plt.figure()
ax = to_scatter.plot.scatter('tot_num_sl_w_lead','pov_rate')
ax.set_title('Lead Pipes vs. Poverty Rate, counties with less than 10k pipes with lead')
ax.set_xlabel('Number of Lead Pipes in the County')
ax.set_ylabel('Poverty Rate')

ax.figure.savefig('lead_pov_rate_lead_less_than_10k')
#this graph is for visualization only, as are the following plots
#poverty rate appears to be correlated with the number of lead pipes per county


#%%

plt.figure()
ax = merge.plot.scatter('pct_lead','pov_rate')
ax.set_title('Lead Pipes vs. Poverty Rate')
ax.set_xlabel('Percent of Service Lines that Contain Lead')
ax.set_ylabel('Poverty Rate')

ax.figure.savefig('lead_pov_pct_lead')
#relationship between poverty rate and percent of service lines containg lead is
    #less clear than the relationship between number of pipes and poverty rate

#%%

to_drop = merge[merge['tot_num_sl_w_lead'] > 10000].index
#identify counties with less than 10000 lead pipes

to_scatter = merge.drop(to_drop)
#drop the counties with more than 10,000 pipes per county

to_drop = merge[merge['tot_num_sl_w_lead'] == 0].index
#remove 0 values to make graph more readable; non response rates, unknown materials, and utilities
    #mean there are many counties with no lead pipes which makes it difficult to read the graph

to_scatter = to_scatter.drop(to_drop)

plt.figure()
ax = to_scatter.plot.scatter('pct_lead','pov_rate')
ax.set_title('Lead Pipes vs. Poverty Rate, counties with less than 10k pipes with lead')
ax.set_xlabel('Percent of Pipes that Contain Lead')
ax.set_ylabel('Poverty Rate')

ax.figure.savefig('lead_pov_rate_pct_lead_less_than_10k')
#relationship between percent of pipes reported to contain lead and poverty rate
    #seems more in line with the relationship between number of pipes containing lead and
    #the poverty rate after similar adjustments were made

#%%

merge['per_capita'] = merge['tot_num_sl_w_lead']/merge['pov_stat_pop']
#this calculates the number of lead pipes per capita for each county

plt.figure()
ax = merge.plot.scatter('per_capita','pov_rate')
ax.set_title('Lead Pipes per Capita vs. Poverty Rate')
ax.set_xlabel('Number of Lead Pipes per Capita')
ax.set_ylabel('Poverty Rate')

ax.figure.savefig('lead_pov_rate_lead_per_capita')

#%%

to_drop = merge[merge['tot_num_sl_w_lead'] > 10000].index
#identify counties with less than 10000 lead pipes

to_scatter = merge.drop(to_drop)
#drop the counties with more than 10,000 pipes per county

to_drop = merge[merge['tot_num_sl_w_lead'] == 0].index
#remove 0 values to make graph more readable; non response rates, unknown materials, and utilities
    #mean there are many counties with no lead pipes which makes it difficult to read the graph

to_scatter = to_scatter.drop(to_drop)

plt.figure()
ax = to_scatter.plot.scatter('per_capita','pov_rate')
ax.set_title('Lead Pipes per Capita vs. Poverty Rate, counties with less than 10k pipes with lead')
ax.set_xlabel('Lead Pipes per Capita')
ax.set_ylabel('Poverty Rate')

ax.figure.savefig('lead_pov_rate_lead_per_capita_less_than_10k')
#this graph does not change much when the same adjustments are made as they were to the other graphs

#%%

#let's remove the outlier from the previous graph

to_drop = merge[merge['per_capita'] > 0.3].index
#selects the county with a high number of lead pipes per capita

to_scatter = merge.drop(to_drop)

to_drop = merge[merge['tot_num_sl_w_lead'] == 0].index
#remove 0 values to make graph more readable; non response rates, unknown materials, and utilities
    #mean there are many counties with no lead pipes which makes it difficult to read the graph

to_scatter = to_scatter.drop(to_drop)

plt.figure()
ax = to_scatter.plot.scatter('per_capita','pov_rate')
ax.set_title('Lead Pipes per Capita vs. Poverty Rate, counties with fewer than 0.3 lead pipes per capita')
ax.set_xlabel('Lead Pipes per Capita')
ax.set_ylabel('Poverty Rate')

ax.figure.savefig('lead_pov_rate_lead_per_capita_low_per_capita')
#poverty rate does appear to be associated with an increas in the number of lead pipes per capita