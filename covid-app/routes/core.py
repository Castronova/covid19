#!/usr/bin/env python3

import env
import utils
from . import routes
from utils import collectdata
from flask import render_template, redirect, request



states = {'Alabama': 'alabama',
          'Alaska': 'alaska',
          'Arizona': 'arizona',
          'Arkansas': 'arkansas',
          'California': 'california',
          'Colorado': 'colorado',
          'Connecticut': 'connecticut',
          'Delaware': 'delaware',
          'Florida': 'florida',
          'Georgia': 'georgia',
          'Hawaii': 'hawaii',
          'Idaho': 'idaho',
          'Illinois': 'illinois',
          'Indiana': 'indiana',
          'Iowa': 'iowa',
          'Kansas': 'kansas',
          'Kentucky': 'kentucky',
          'Louisiana': 'louisiana',
          'Maine': 'maine',
          'Maryland': 'maryland',
          'Massachusetts': 'massachusetts',
          'Michigan': 'michigan',
          'Minnesota': 'minnesota',
          'Mississippi': 'mississippi',
          'Missouri': 'missouri',
          'Montana': 'montana',
          'Nebraska': 'nebraska',
          'Nevada': 'nevada',
          'New Hampshire': 'new_hampshire',
          'New Jersey': 'new_jersey',
          'New Mexico': 'new_mexico',
          'New York': 'new_york',
          'North Carolina': 'north_carolina',
          'North Dakota': 'north_dakota',
          'Ohio': 'ohio',
          'Oklahoma': 'oklahoma',
          'Oregon': 'oregon',
          'Pennsylvania': 'pennsylvania',
          'Rhode Island': 'rhode_island',
          'South Carolina': 'south_Carolina',
          'South Dakota': 'south_Dakota',
          'Tennessee': 'tennessee',
          'Texas': 'texas',
          'Utah': 'utah',
          'Vermont': 'vermont',
          'Virginia': 'virginia',
          'Washington': 'washington',
          'West Virginia': 'west_virginia',
          'Wisconsin': 'wisconsin',
          'Wyoming': 'wyoming'}

@routes.route('/deaths')
def index():
    prefix = None
    base_url = request.host
    if 'proxy' in base_url:
        prefix = f'/proxy/{base_url.split("proxy")[-1]}'
    return render_template("index.html", data=states, prefix=prefix)

@routes.route('/collect-data')
def collectdata():
    utils.collectdata.collect(env.data_path)
    return redirect('/deaths')

