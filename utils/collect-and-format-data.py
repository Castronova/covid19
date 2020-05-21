#!/usr/bin/env python3

import pdb
import os
import wget
import shutil
import pandas

# download the latest data
p = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
fname = os.path.basename(p)
if os.path.exists(fname):
    os.remove(fname)
wget.download(p)

# load data
df = pandas.read_csv('time_series_covid19_deaths_US.csv')

# remove extra columns
df = df.drop(['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2',
         'Country_Region', 'Lat', 'Long_', 'Combined_Key', 'Population'],
         axis=1)

# group data by state
df = df.groupby('Province_State').sum()

# clean state names, i.e. remove spaces
df.index.str.replace(' ','_')

# transpose the data
df = df.T

# name the index 
df.index.rename('date', inplace=True)
df.index = pandas.to_datetime(df.index)

# save to csv
df.to_csv('covid-deaths.tsv', sep='\t', date_format='%Y%m%d')
