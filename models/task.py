from library.decorator import postgres_cursor_connection_class,postgres_cursor_class
from library.config    import standar_response

import datetime


class Task:

    def __init__(self,
                id=None,
                id_subtask=None,
                id_process=None,
                name=None,
                detail=None,
                start_date=None,
                end_date=None,
                real_end_date=None,
                creator_id=None,
                asignee=None,
                status=None,
                subtask=None):
            self.id=id
            self.id_subtask=id_subtask
            self.id_process=id_process
            self.name=name
            self.detail=detail
            self.start_date=start_date
            self.end_date=end_date
            self.real_end_date=real_end_date
            self.creator_id=creator_id
            self.asignee=asignee
            self.status=status
            self.subtask=subtask
    
    @postgres_cursor_class
    def add_task(self,cursor,connection):
        #TODO Validar existencia de proceso

        #TODO: Validar fecha finalizacion

        #Insertar tupla en base de datos
        query = """INSERT INTO tarea(id_proceso, nombre, detalle, fecha_inicio, fecha_estimada, id_usuario_creador, estado_tarea) VALUES () RETURNING id"""
        cursor.execute(query,(self.id_process,self.name,self.detail, self.start_date, self.end_date, self.creator_id, 0))
    

    @postgres_cursor_class
    def assign_task(self,cursor,connection):
        #Insertar tupla en base de datos
        query = """INSERT INTO asignacion_tarea(id_usuario, id_tarea, id_subtarea) VALUES ( %s, %s, %s)"""
        cursor.execute(query,(self.asignee,self.id,self.id_subtask))
        
        connection.commit()

        return {
            'status':200,
            'msg':'Tarea asignada con exito',
            'data': []
        }
    
    @postgres_cursor_class
    def unassign_task(self,cursor,connection):
        #eliminar tupla en base de datos
        query = """DELETE FROM asignacion_tarea WHERE id_usuario = %s, id_tarea = %s, id_subtarea = %s"""
        cursor.execute(query,(self.asignee,self.id,self.id_subtask))
        
        connection.commit()

        return {
            'status':200,
            'msg':'Tarea desasignada con exito',
            'data': []
        }

    @postgres_cursor_class
    def finish_task(self,cursor,connection):
        #Actualizar tupla en base de datos
        query = """UPDATE tarea set id_usuario = %s, estado_tarea = 1, fecha_finalizada = current_timestamp"""
        cursor.execute(query,(self.asignee,self.id))
        
        connection.commit()

        return {
            'status':200,
            'msg':'Tarea finalizada con exito',
            'data': []
        }
    
    @postgres_cursor_class
    def get_tasks(self,cursor,connection):
        #Actualizar tupla en base de datos
        query = """SELECT tsk.id, tsk.nombre, tsk.detalle, tsk.fecha_inicio, tsk.fecha_estimada, tsk.fecha_finalizada, tsk.id_usuario_creador, tsk.id_quien_finaliza, tsk.estado_tarea FROM tarea tsk, asignacion_tarea asig WHERE asig.id_usuario = %s AND tsk.id = asig.id_tarea"""
        cursor.execute(query,(self.asignee))
        
        data = cursor.fetchall()

        for k in data:
            


        

        return {
            'status':200,
            'msg':'Tarea finalizada con exito',
            'data': []
        }

