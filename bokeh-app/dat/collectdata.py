#!/usr/bin/env python3

import pdb
import os
import wget
import shutil
import pandas


def download_file(f):
    fname = os.path.basename(f)
    if os.path.exists(fname):
        os.remove(fname)
    wget.download(f)


def collect(outpath='.'):
    # download the latest data
    baseUrl = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series'
    deaths = 'time_series_covid19_deaths_US.csv'
    confirmed = 'time_series_covid19_confirmed_US.csv'

    for fname in [deaths, confirmed]:
        print(f'processing {fname}')

        # get file
        download_file(f'{baseUrl}/{fname}')

        # load data
        df = pandas.read_csv(fname)

        # ignore extra columns
        reg_filter = 'Province_State|[0-9]?[0-9]\\/[0-9]?[0-9]\\/[0-9][0-9]'
        df = df.filter(regex=(reg_filter))

        # group data by state
        df = df.groupby('Province_State').sum()

        # clean state names, i.e. remove spaces
        df.index.str.replace(' ', '_')

        # transpose the data
        df = df.T

        # name the index
        df.index.rename('date', inplace=True)
        df.index = pandas.to_datetime(df.index)

        # save to csv
        df.to_csv(f'{outpath}/covid-{fname.split("_")[-2]}.tsv', sep='\t',
                  date_format='%Y%m%d')

        # remove the raw data
        os.remove(fname)


if __name__ == '__main__':
    collect()
