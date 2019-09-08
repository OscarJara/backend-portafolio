from library.decorator import postgres_cursor_class,postgres_cursor_connection_class



class User:


    def __init__(self,id=None,mail=None,name=None,last_name=None,second_last_name=None,id_rol=None,id_unidad=None,password=None,state=None,image=None):
        self.id = id
        self.mail = mail
        self.name = name
        self.last_name = last_name
        self.second_last_name = second_last_name
        self.id_rol = id_rol
        self.id_unidad = id_unidad
        self.password = password
        self.state = state
        self.image = image

    @postgres_cursor_connection_class
    def add_user(self,cursor,connection):
        query = """INSERT INTO usuario (correo,nombres,apellido_paterno,apellido_materno,id_rol,id_unidad,password,estado,imagen)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
        cursor.execute(query,(self.mail,self.name,self.last_name,self.second_last_name,self.id_rol,self.id_unidad,self.password,self.state,self.image))
        connection.commit()
        return {
            'status':200,
            'msg':'Usuario agregado con exito',
            'desc':''
        }

    @postgres_cursor_class
    def list_user(self,cursor):
        print ('USER')
        query = """SELECT * FROM usuario"""
        cursor.execute(query)
        data = cursor.fetchall()
        response = []
        for k in data:
            response.append(
                {
                    'nombre': k['nombres'],
                    'apellido_paterno':k['apellido_paterno'],
                    'apellido_materno':k['apellido_materno'],
                    'id':k['id'],
                    'imagen':k['imagen']
                }
            )
        return {
            'status':200,
            'msg':'Lista de usuarios',
            'data':response
        }

    @postgres_cursor_class
    def login(self,cursor):
        query = """select us.id,us.nombres,us.apellido_paterno,us.apellido_materno,us.id_rol,us.id_unidad,us.imagen,un.id_empresa
        from usuario as us
        join unidad as un 
        on un.id=us.id_unidad
            where correo=%s and password = %s"""
        cursor.execute(query,(self.mail,self.password))
        data = cursor.fetchone()
        return {
            'status':200,
            'msg':'Login Usuario',
            'data':data
        }