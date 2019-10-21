from library.decorator import postgres_cursor_connection_class,postgres_cursor_class
from library.config    import standar_response

import datetime


class Task:

    def __init__(self,id,id_process,name,detail,start_date,end_date,real_end_date,status):
        