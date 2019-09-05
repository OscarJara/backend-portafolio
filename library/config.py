#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import environ
from dotenv import load_dotenv
from os.path import join, dirname
load_dotenv(join(dirname(__file__), '../.env'))


# Server route
SERVER_PATH = environ.get('SERVER_PATH')

# Postgres credentials 
POSTGRE_HOST = environ.get('POSTGRE_HOST')
POSTGRE_DB = environ.get('POSTGRE_DB')
POSTGRE_USER = environ.get('POSTGRE_USER')
POSTGRE_PASS = environ.get('POSTGRE_PASS')