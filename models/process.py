from library.decorator import postgres_cursor_connection_class,postgres_cursor_class
from library.config    import standar_response

import datetime

class Process:

    
    def __init__(self,
            id=None,name=None,company=None,
            detail=None,start_date=None,end_date=None):
        
        self.id = id
        self.name = name
        self.company = company
        self.detail = detail
        self.start_date = start_date
        self.end_date = end_date

    def __validate_company(self,cursor):
        query = """SELECT * FROM empresa where id = %s """
        cursor.execute(query,(self.company,))

        return cursor.fetchall()
    @postgres_cursor_connection_class
    def add_process(self,cursor,cnn):
        
        if not self.__validate_company(cursor):

            return standar_response(400,'Empresa inexistente',{})

        query = """INSERT INTO proceso (nombre,id_empresa,detalle,fecha_inicio,fecha_termino) VALUES (%s,%s,%s,%s,%s) RETURNING id """
        cursor.execute(query,(self.name,self.company,self.detail,self.start_date,self.end_date))
        cnn.commit()
        self.id = cursor.fetchone()['id']

        return standar_response(
            200,
            'Se ha creado proceso con exito',
            {
                'id':self.id,
                'nombre':self.name,
                'detalle':self.detail,
                'fecha_inicio':self.start_date,
                'fecha_termino':self.end_date,
                'estado':0
            }
        )

    @postgres_cursor_connection_class
    def delete_process(self,cursor,cnn):
        if not self.__validate_company(cursor):

            return standar_response(400,'Empresa inexistente',{})

        query_tareas = """SELECT id FROM tarea where id_proceso = %s """ 
        cursor.execute(query_tareas,(self.id,))
        id_tareas = cursor.fetchall()
        if id_tareas:
            query_delete_subtareas = """DELETE FROM sub_tarea where id_tarea in %s """
            cursor.execute(query_delete_subtareas,(tuple(id_tareas),))
            query_delete_tareas = """DELETE FROM tarea where id_proceso = %s """
            cursor.execute(query_delete_tareas,(self.id,))
        query_delete_proceso = """DELETE FROM proceso where id = %s """
        cursor.execute(query_delete_proceso,(self.id,))
        cnn.commit()

        return standar_response(
            200,
            'Se ha eliminado procesos y tareas con Éxito',
            {}
        )
    @postgres_cursor_connection_class
    def update_process(self,cursor,cnn):
        if not self.__validate_company(cursor):

            return standar_response(400,'Empresa inexistente',{})
        query_update = """UPDATE proceso set nombre = %s,detalle=%s,fecha_inicio=%s,fecha_termino=%s where id = %s"""
        cursor.execute(query_update,(self.name,self.detail,self.start_date,self.end_date,self.id))
        cnn.commit()

        return standar_response(
            200,
            'Se modifico con Éxito',
            {
                'id':self.id,
                'nombre':self.name,
                'detalle':self.detail,
                'fecha_inicio':self.start_date,
                'fecha_termino':self.end_date,
                'estado':0
            }
        )
    @postgres_cursor_class
    def get_process(self,cursor):
        if not self.__validate_company(cursor):
            return standar_response(400,'Empresa inexistente',{})

        query = """ SELECT * FROM proceso where id_empresa = %s """
        cursor.execute(query,(self.company,))
        
        data = cursor.fetchall()

        for k in data:
            k['estado'] = 0
            k['fecha_inicio'] = k['fecha_inicio'].strftime("%Y-%m-%d")
            k['fecha_termino'] = k['fecha_termino'].strftime("%Y-%m-%d")

            del (k['id_empresa'])
        data = sorted(data,key=lambda k: k['id'],reverse=False) if data else []
        return standar_response(200,'Lista de procesos',data)

if __name__ == "__main__":
    # process = Process(
        
    #     name='Prueba',
    #     company=5,
    #     detail='PRUEBA',
    #     start_date='2019-05-05',
    #     end_date='2019-05-05'
    # )
    # print(process.add_process())
    # process = Process(id=1,company=5)
    # print(process.delete_process())

    # process = Process(
    #     id=2,
    #     name='Prueba CAMBIO',
    #     company=5,
    #     detail='PRUEBA',
    #     start_date='2019-05-05',
    #     end_date='2019-05-05'
    # )
    # print(process.update_process())

    process = Process(
        company=5
    )
    print(    process.get_process())