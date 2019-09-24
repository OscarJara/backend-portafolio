
# -*- coding: utf-8 -*-

import logging
import functools
import traceback

import psycopg2.extras


from library.config import postgres_connect

def postgres_cursor(f):
    def with_connection_(*args, **kwargs):
        # or use a pool, or a factory function...
        cnn = postgres_connect()
        
        try:
            with cnn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.itersize = 1000
                rv = f(cursor, *args, **kwargs)

        except Exception as e:
            cnn.rollback()
            err = f.__name__
            err += ' ERROR: ' + str(e)
            desc = str(err) + ", problema: " + str(e)
            rv =  (
                {
                    'status':500,
                    'msg':'Unexpected error',
                    'data':[],
                    'error':desc
                }
            )
        else:
            cnn.commit() # or maybe not
        finally:
            cnn.close()
        return rv
    return with_connection_

def postgres_cursor_connection(f):
    def with_connection_(*args, **kwargs):
        # or use a pool, or a factory function...
        connection = postgres_connect()
        
        try:
            with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.itersize = 1000
                return f(cursor,connection,*args, **kwargs)

        except Exception as e:

            connection.rollback()
            err = f.__name__
            err += ' ERROR: ' + str(e)
            desc = str(err) + ", problema: " + str(e)
            return (
                {
                    'status':500,
                    'msg':'Unexpected error',
                    'data':[],
                    'error':desc

                }
            )
        else:
            connection.commit() # or maybe not
        finally:
            connection.close()
    return with_connection_

def postgres_cursor_class(function):
    def with_connection_(self,*args, **kwargs):
        connection = postgres_connect()

        try:
            with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.itersize = 1000
                return function(self,cursor,*args, **kwargs)

        except Exception as e:

            connection.rollback()
            err = function.__name__
            err += ' ERROR: ' + str(e)
            desc = str(err) + ", problema: " + str(e)
            return (
                {
                    'status':500,
                    'msg':'Unexpected error',
                    'data':[],
                    'error':desc

                }
            )
        else:
            connection.commit() # or maybe not
        finally:
            connection.close()
    return with_connection_

def postgres_cursor_connection_class(function):
    def with_connection_(self,*args,**kwargs):
        connection = postgres_connect()

        try:
            with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.itersize = 1000
                return function(self,cursor,connection,*args, **kwargs)

        except Exception as e:
            print (traceback.format_exc())
            connection.rollback()
            err = function.__name__
            err += ' ERROR: ' + str(e)
            desc = str(err) + ", problema: " + str(e)
            return (
                {
                    'status':500,
                    'msg':'Unexpected error',
                    'data':[],
                    'error':desc

                }
            )
        else:
            connection.commit() # or maybe not
        finally:
            connection.close()
    return with_connection_