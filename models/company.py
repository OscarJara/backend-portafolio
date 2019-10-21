from library.decorator import postgres_cursor_connection_class,postgres_cursor_class

import json

class Company:

    def __init__(self,
            id=None,name=None,adress=None,
            city=None,rut=None,status=None,
            organization_chart=None
        ):

        self.id = id
        self.name = name
        self.adress = adress
        self.city = city
        self.rut = rut
        self.status = status
        self.organization_chart = organization_chart


    @postgres_cursor_connection_class
    def add_company(self,cursor,connection):
        query_valid = """SELECT * FROM empresa WHERE rut = %s """
        cursor.execute(query_valid,(self.rut,))

        if cursor.fetchone():
            return {
                'status':400,
                'msg':'Empresa existente',
                'data':[]
            }

        query_add = """ INSERT INTO empresa(nombre,direccion,ciudad,rut) VALUES ( %s,%s,%s,%s ) returning id """
        cursor.execute(query_add,(self.name,self.adress,self.city,self.rut))

        connection.commit()
        self.id = cursor.fetchone()['id']
        self.status= True
        return {
            'status':200,
            'msg':'Empresa agregada con exito',
            'data':{
                'id':self.id,
                'nombre':self.name,
                'direccion':self.adress,
                'ciudad':self.city,
                'rut':self.rut,
                'estado':self.status
            }
        }

    def __valid_company(self,cursor):
        query_valid =  """SELECT * FROM empresa WHERE id = %s """
        cursor.execute(query_valid,(self.id,))

        return cursor.fetchall()

    @postgres_cursor_connection_class
    def update_company(self,cursor,connection):

        if not self.__valid_company(cursor):
            return {
                'status':400,
                'msg':'Empresa no inexistente',
                'data':[]
            }

        query_update = """UPDATE empresa set nombre =%s,direccion=%s,ciudad=%s,rut=%s where id = %s """
        cursor.execute(query_update,(self.name,self.adress,self.city,self.rut,self.id))

        connection.commit()

        return {
            'status':200,
            'msg':'Empresa modificada con exito',
            'data':[]
        }

    @postgres_cursor_connection_class
    def delete_company(self,cursor,connection):

        if not self.__valid_company(cursor):
            return {
                'status':400,
                'msg':'Empresa inexistente',
                'data':[]
            }

        query_delete = """UPDATE  empresa set estado = False where id = %s """
        cursor.execute(query_delete,(self.id,))

        connection.commit()

        return {
            'status':200,
            'msg':'Empresa desactivada con exito',
            'data':[]
        }

    @postgres_cursor_connection_class
    def activate_company(self,cursor,connection):
        
        if not self.__valid_company(cursor):
            return {
                'status':400,
                'msg':'Empresa inexistente',
                'data':[]
            }

        query_delete = """UPDATE  empresa set estado = True where id = %s """
        cursor.execute(query_delete,(self.id,))

        connection.commit()

        return {
            'status':200,
            'msg':'Empresa Activada con exito',
            'data':[]
        }

    @postgres_cursor_class
    def get_company(self,cursor):
        query =  """ SELECT * FROM empresa """
        cursor.execute(query)

        response = [
            {
                'id':k['id'],
                'nombre':k['nombre'],
                'direccion':k['direccion'],
                'ciudad':k['ciudad'],
                'rut':k['rut'],
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

    @postgres_cursor_connection_class
    def add_company_chart(self,cursor,connection):
        
        if not self.__valid_company(cursor):
            return {
                'status':400,
                'msg':'Empresa inexistente',
                'data':[]
            }
        query = """ SELECT * FROM jerarquia where id_empresa = %s """
        cursor.execute(query,(self.id,))
        if cursor.fetchall():
            return {
                'status':400,
                'msg':'Jerarquia existente, no se puede crear otra',
                'data':[]
            }
        query = """INSERT INTO jerarquia (id_empresa,jerarquia) values (%s,%s) """
        cursor.execute(query,(self.id,json.dumps(self.organization_chart)))

        connection.commit()

        return {
            'status':200,
            'msg':'Jerarquia añadida con exito',
            'data':[]
        }

    @postgres_cursor_connection_class
    def update_company_char(self,cursor,connection):
        if not self.__valid_company(cursor):
            return {
                'status':400,
                'msg':'Empresa inexistente',
                'data':[]
            }
        query = """ SELECT * FROM jerarquia where id_empresa = %s """
        cursor.execute(query,(self.id,))
        if not cursor.fetchall():
            return {
                'status':400,
                'msg':'Jerarquia inexistente, primero se debe crear la Jerarquia',
                'data':[]
            }
        query = """UPDATE jerarquia set jerarquia =%s where id_empresa = %s """
        cursor.execute(query,(json.dumps(self.organization_chart),self.id))

        connection.commit()

        return {
            'status':200,
            'msg':'Jerarquia modificada con exito',
            'data':[]
        }

    @postgres_cursor_connection_class
    def get_company_chart(self,cursor,connection):
        if not self.__valid_company(cursor):
            return {
                'status':400,
                'msg':'Empresa inexistente',
                'data':[]
            }
        query = """ SELECT * FROM jerarquia where id_empresa = %s """
        cursor.execute(query,(self.id,))
        data_response = cursor.fetchone()
        if not data_response:
            return {
                'status':204,
                'msg':'Jerarquia no encontrada',
                'data':[]
            }
        data_response = data_response['jerarquia']

        return {
            'status':200,
            'msg':'Jerarquia',
            'data':data_response
        }
        
        
    @postgres_cursor_connection_class
    def delete_company_char(self,cursor,connection):
        if not self.__valid_company(cursor):
            return {
                'status':400,
                'msg':'Empresa inexistente',
                'data':[]
            }

        query = """DELETE FROM jerarquia where id_empresa = %s """
        cursor.execute(query,(self.id,))

        connection.commit()

        return {
            'status':200,
            'msg':'Jerarquia eliminada con exito',
            'data':[]
        }