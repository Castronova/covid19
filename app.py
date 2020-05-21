#!/usr/bin/env python3

import os
from routes import *
from flask import Flask


template_dir = os.path.abspath('templates')
static_dir = os.path.abspath('static')

app = Flask('CUAHSI SELFIE',
            template_folder=template_dir,
            static_folder=static_dir,
            static_url_path='/static')

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
