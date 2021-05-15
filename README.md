# Lead_pipes_indiana
Lead Pipes and Poverty in Indiana

Summary of Project:

Inputs:
Mapping of lead pipes in Indiana from https://www.edf.org/health/mapping-lead-pipes-water-utility
Download excel file from the above link and convert 'EDF_Mapping_data' and 
'Indiana-LSL-Data-for-Interactive-Map_EDF' spread sheets into .csv files
The spreadsheets combine information from the EPA Safe Drinking Water Information
System (SDWIS) and and a voluntary state survey conducted in 2017. The survey
asked utilities about the location of service lines containg lead in their system.
As the survey was voluntary, only about 57.7% of utilities responded however the 
responses represented 92% of the service lines in the state.

This project also uses the census tiger line file for the county lines which can
be downloaded from the census website. The file is 'tl_2017_us_county.zip'

This project also uses data downloaded from the census API.

Outputs:

File structure/Order:
1 merge.py; outputs: lead_service_lines.csv (.csv file of the merged survey data)
2 analyze_indiana.py; inputs: lead_service_lines.csv; outputs: lsl.csv, lsl_layer.csv
3 census_data.py; inputs: none; outputs: 
4 QGIS analysis: inputs: lsl_layer.csv, census_data.csv, tl_2017_us_county.zip;
    outputs: 
    To conduct QGIS analysis: import all files; filter tl_2017_us_county so that only
        counties in Indiana appear (FIPS code: 18)
        join census_data to tl_2017_us_county on 'GEOID' (use custom name and shorten census_data_ to census_)
        Join lsl_layer to tl_2017_us_county and save new layer as lsl_county
        export lsl_county as csv file of same name
        set tl_2017_us_county layer styling to graduated with a value of census_pov_rate using natural breaks
        set lsl_layer styling to graduated with a value of pct_lsl_calc using natural breaks
            this image was exported as 'pov_rate_pct_lead_sl.png'
        set add pie charts using attributes 'tot_num_sl_w_lead' colored gray, 'no_lead_serv_connects' colored green,
            and 'unk_mat_serv_connects' colored orange
                this map exported as 'pov_rate_pie_chart.png' shows the poverty rate of each county
                    and the percentage of service lines reported as containing lead, no lead, or unknown
        remove pie charts
        set tl_2017_us_county layer styling to the value 'med_income' using pretty breaks
            this map exported as 'med_income_pct_lead_sl.png' shows the median income and the percent of service
                lines that contain lead
5 analyze_counties.py; inputs: lsl_county.csv, census_data.csv

Results:
The number of lead pipes in a county correlates with the level poverty in the county
and the relationship is likely not linear (take that into account if running a
regression)

Further analysis:

More granular data (challenge, utilities given as latitude and longitude make it
difficult to determine the extent )

ownership of pipes

confidence in record or estimate
