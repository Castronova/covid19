#!/usr/bin/env python3

import pdb
import pandas

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

#df = df.pivot_table(columns='Province_State', fill_value=0)

df.to_csv('covid-deaths.tsv', sep='\t')
print('done')


