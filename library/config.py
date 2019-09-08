#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Enviroment config
from os import environ
from dotenv import load_dotenv
from os.path import join, dirname
load_dotenv(join(dirname(__file__), './.env'))

# Postgres library
import psycopg2


# Server route
SERVER_PATH = environ.get('SERVER_PATH')

# Postgres credentials 
POSTGRE_HOST = environ.get('POSTGRE_HOST')
POSTGRE_DB = environ.get('POSTGRE_DB')
POSTGRE_USER = environ.get('POSTGRE_USER')
POSTGRE_PASS = environ.get('POSTGRE_PASS')


def postgres_connect():
    connect_str = "dbname='{}' user='{}' host='{}' password='{}' ".format(
            POSTGRE_DB, POSTGRE_USER, POSTGRE_HOST, POSTGRE_PASS)
    return psycopg2.connect(connect_str)