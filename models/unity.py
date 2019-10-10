from library.decorator import postgres_cursor_connection_class,postgres_cursor_class

import json

class Unity:

    def __init__(self,
            id=None,name=None,company=None
        ):

        self.id = id
        self.name = name
        self.company = company


    @postgres_cursor_connection_class
    def add_unity(self,cursor,connection):

        if not self.__valid_company(cursor):
            return {
                'status':400,
                'msg':'Empresa inexistente',
                'data':[]
            }

        query_add = """ INSERT INTO unidad(nombre,id_empresa) VALUES ( %s,%s ) RETURNING id """
        cursor.execute(query_add,(self.name,self.company))

        connection.commit()
        id_unity = cursor.fetchone()

        return {
            'status':200,
            'msg':'Unidad agregada con exito',
            'data':{
                'id':id_unity,
                'nombre':self.name
            }
            
        }

    def __valid_company(self,cursor):
        query_valid =  """SELECT * FROM empresa WHERE id = %s """
        cursor.execute(query_valid,(self.company,))

        return cursor.fetchall()

    @postgres_cursor_connection_class
    def update_unity(self,cursor,connection):

        if not self.__valid_company(cursor):
            return {
                'status':400,
                'msg':'Empresa no inexistente',
                'data':[]
            }

        query_update = """UPDATE unidad set nombre =%s where id = %s """
        cursor.execute(query_update,(self.name,self.id))

        connection.commit()

        return {
            'status':200,
            'msg':'unidad modificada con exito',
            'data':[]
        }

    @postgres_cursor_connection_class
    def delete_unity(self,cursor,connection):

        if not self.__valid_company(cursor):
            return {
                'status':400,
                'msg':'Empresa inexistente',
                'data':[]
            }

        query_delete = """UPDATE  unidad set estado = False where id = %s """
        cursor.execute(query_delete,(self.id,))

        connection.commit()

        return {
            'status':200,
            'msg':'Unidad eliminada con exito',
            'data':[]
        }

    @postgres_cursor_connection_class
    def activate_unity(self,cursor,connection):
        
        if not self.__valid_company(cursor):
            return {
                'status':400,
                'msg':'Empresa inexistente',
                'data':[]
            }

        query_delete = """UPDATE  unidad set estado = True where id = %s """
        cursor.execute(query_delete,(self.id,))

        connection.commit()

        return {
            'status':200,
            'msg':'Unidad Activada con exito',
            'data':[]
        }

    @postgres_cursor_class
    def get_unity(self,cursor):
        query =  """ SELECT * FROM unidad where id_empresa = %s """
        cursor.execute(query,(self.company,))

        response = [
            {
                'id':k['id'],
                'nombre':k['nombre'],
                'estado':k['estado']
            }
            for k in cursor.fetchall()
        ]

        code = 200 if response else 204

        return {
            'status':code,
            'msg':'Lista empresas',
            'data':response
        }
