#!/usr/bin/env python3

import os
import env
import argparse
from routes import *
from flask import Flask


app = Flask('CUAHSI SELFIE',
            template_folder=env.template_dir,
            static_folder=env.static_dir,
            static_url_path='/static')


app.register_blueprint(routes)

if __name__ == '__main__':

    app.run(debug=True, port=5030)

