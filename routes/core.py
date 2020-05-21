#!/usr/bin/env python3

from . import routes
from flask import render_template


@routes.route('/')
def index():
    return render_template("index.html")
