#!/usr/bin/python3
"""
Creates a Flask blueprint for API endpoints with a URL prefix.
"""
from flask import Blueprint


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *