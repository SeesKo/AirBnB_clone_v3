#!/usr/bin/python3
from flask import Blueprint

# Create the blueprint with the specified URL prefix
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Wildcard import everything from `api.v1.views.index`
# (PEP 8 may complain about this, but it's required for Flask blueprints)
from api.v1.views.index import *
