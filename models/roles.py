from library.decorator import postgres_cursor_connection_class,postgres_cursor_class

class Role:

    def __init__(self,
                id=None,name=None,
                description=None,empresa=None
            ):
        self.id = id
        self.name = name
        self.description = description
        self.empresa = empresa

    @postgres_cursor_connection_class
    def add_role(self,cursor,connection):

        query_valid = """SELECT * FROM rol where nombre = %s """
        cursor.execute(query_valid,(self.name,))
        if cursor.fetchone():
            return {
                'status':200,
                'msg':'Nombre de rol existente',
                'data':[]
            }
        query = """INSERT INTO rol(nombre,descripcion,empresa) VALUES (%s,%s,%s) RETURNING id"""
        cursor.execute(query,(self.name,self.description,self.empresa))
        self.id = cursor.fetchone()['id']
        connection.commit()

        return {
            'status':200,
            'msg':'Rol agregado con exito',
            'data':{
                'id':self.id,
                'nombre':self.name,
                'descripcion':self.description  
            }
        }
    
    def __valid_role(self,cursor):
        query_valid = """SELECT * FROM rol WHERE id = %s """
        cursor.execute(query_valid,(self.id,))

        if not cursor.fetchall():
            return {
                'status':400,
                'msg':'Rol inexistente',
                'data':[]
            }
        else:
            return False

    @postgres_cursor_connection_class
    def update_role(self,cursor,connection):
        is_valid = self.__valid_role(cursor)
        if is_valid:
            return is_valid

        query = """UPDATE rol SET nombre = %s, descripcion = %s WHERE id = %s """
        cursor.execute(query,(self.name,self.description,self.id))
        connection.commit()
        return {
            'status':200,
            'msg':'Rol editado con exito',
            'data':{
                'id':self.id,
                'nombre':self.name,
                'descripcion':self.description  
            }
        }

    @postgres_cursor_connection_class
    def delete_role(self,cursor,connection):
        
        is_valid = self.__valid_role(cursor)
        if is_valid:
            return is_valid

        query_delete = """DELETE FROM rol WHERE id = %s """
        cursor.execute(query_delete,(self.id,))

        connection.commit()

        return {
            'status':200,
            'msg':'Rol eliminado con exito',
            'data':[]
        }
    @postgres_cursor_class
    def get_roles(self,cursor,correo):

        query_rol_user = """SELECT id_rol as rol FROM usuario where correo = %s """
        cursor.execute(query_rol_user,(correo,))

        rol_usuario = cursor.fetchone()
        if not rol_usuario:
            return {
                'status':204,
                'msg':'Lista de roles',
                'data':[]
            }
        rol_usuario = rol_usuario['rol']
        if rol_usuario == 0:
            query = """SELECT * FROM rol"""
        else:
            query = """SELECT * FROM rol where id >0"""
        
        cursor.execute(query)
        data = cursor.fetchall()
        code = 200 if data else 204
        response = [
            {
                'id':k['id'],
                'nombre':k['nombre'],
                'descripcion':k['descripcion']
            }
            for k in data
        ]

        response = sorted(response,key=lambda k: k['id'],reverse=False) if response else []
        return {
            'status':code,
            'msg':'Lista de roles',
            'data':response
        }
