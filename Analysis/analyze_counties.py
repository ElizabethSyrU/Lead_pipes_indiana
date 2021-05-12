# -*- coding: utf-8 -*-
"""
Created on Tue May 11 20:19:38 2021

@author: Elizabeth
"""

import pandas as pd
import matplotlib.pyplot as plt

pipes_by_county = pd.read_csv('pipes_by_county.csv')

pipes_by_county = pipes_by_county[['NAMELSAD','GEOID','stats_tot_pop','stats_med_income',
                                   'stats_pov_stat_pop','stats_below_pov_line_prev_yr',
                                   'stats_pov_rate','tot_num_serv_connects_sdwis',
                                   'tot_num_serv_connects','tot_num_sl_w_lead',
                                   'no_lead_serv_connects','unk_mat_serv_connects']]

#%%

num_pipes_by_county = pipes_by_county[['tot_num_serv_connects','tot_num_sl_w_lead','unk_mat_serv_connects']].groupby(pipes_by_county['GEOID']).sum()
#gets the number of pipes by county
num_pipes_by_county['pct_lead'] = 100*pipes_by_county['tot_num_sl_w_lead']/pipes_by_county['tot_num_serv_connects']
#this isn't working, only returns nan, why?

#merge = num_pipes_by_county.merge(pipes_by_county,how='left',on='GEOID',indicator=True)

#%%

census = pd.read_csv('census_data.csv')
merge = num_pipes_by_county.merge(census,on='GEOID',indicator=True)

#%%

plt.figure()
ax = merge.plot.scatter('tot_num_sl_w_lead','pov_rate')
ax.set_title('Lead Pipes vs. Poverty Rate')
ax.set_xlabel('Number of Lead Pipes')
ax.set_ylabel('Poverty Rate')
ax.figure.savefig('lead_pov_rate')
#not very interesting result

#%%

to_drop = merge[merge['tot_num_sl_w_lead'] > 10000].index
#identify counties with less than 10000 lead pipes

to_scatter = merge.drop(to_drop,inplace=True)#not sure why inplace=True
#drop the values you don't want

to_drop = merge[merge['tot_num_sl_w_lead'] == 0].index
#remove 0 values

to_scatter = merge.drop(to_drop,inplace=True)

plt.figure()
ax = merge.plot.scatter('tot_num_sl_w_lead','pov_rate')
ax.set_title('Lead Pipes vs. Poverty Rate')#setting labels and such isn't working
ax.set_xlabel('Number of Lead Pipes')
ax.set_ylabel('Poverty Rate')

ax.figure.savefig('lead_pov_rate_lead_less_than_10k')
#this graph is for visualization only, as are the following plots


#%%
to_drop = merge[merge['tot_num_sl_w_lead'] > 2000].index
#identify counties with less than 10000 lead pipes

to_scatter = merge.drop(to_drop,inplace=True)#not sure why inplace=True
#drop the values you don't want

plt.figure()
ax = merge.plot.scatter('tot_num_sl_w_lead','pov_rate')
ax.set_title('Lead Pipes vs. Poverty Rate')#setting labels and such isn't working
ax.set_xlabel('Number of Lead Pipes')
ax.set_ylabel('Poverty Rate')

ax.figure.savefig('lead_pov_rate_lead_less_than_2k')

#%%

to_drop = merge[merge['tot_num_sl_w_lead'] > 500].index
#identify counties with less than 10000 lead pipes

to_scatter = merge.drop(to_drop,inplace=True)#not sure why inplace=True
#drop the values you don't want

plt.figure()
ax = merge.plot.scatter('tot_num_sl_w_lead','pov_rate')
ax.set_title('Lead Pipes vs. Poverty Rate')#setting labels and such isn't working
ax.set_xlabel('Number of Lead Pipes')
ax.set_ylabel('Poverty Rate')

ax.figure.savefig('lead_pov_rate_lead_less_than_500')
