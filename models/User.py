#!/usr/bin/env python
# -*- coding: utf-8 -*-

from library.decorator import postgres_cursor_class,postgres_cursor_connection_class
from library.config    import postgres_connect,KEY_SECRET
from models.mails      import send_mail,get_plantilla
from pbkdf2            import crypt


import pandas as pd
import psycopg2.extras
import random
import string
import datetime
import jwt
import base64




class User:


    def __init__(self,
                    id=None,mail=None,
                    name=None,last_name=None,
                    second_last_name=None,id_rol=None,
                    id_unidad=None,password=None,
                    state=None,image=None):
        

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

    @property
    def mail(self):
        return self.__mail


    @mail.setter
    def mail(self,mail):
        self.__mail = mail

    @property
    def id(self):
        return self.__id


    @id.setter
    def id(self,id):
        self.__id = id

    def _validate_user(self,cursor,email):
        query = """SELECT * FROM usuario WHERE correo = %s """
        cursor.execute(query,(email,))
        return cursor.fetchone()

    @postgres_cursor_connection_class
    def add_user(self,cursor,connection):

        if self._validate_user(cursor,self.mail):
            return {
                'status':400,
                'msg':'Email ya existente',
                'data':[]
            }

        passuser = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(15))
        passEncript = crypt(passuser,'PORTAFOLIO',400)


        query = """INSERT INTO usuario (correo,nombres,apellido_paterno,apellido_materno,id_rol,id_unidad,password,estado,imagen)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
        cursor.execute(query,(self.mail,
                            self.name,
                            self.last_name,
                            self.second_last_name,
                            self.id_rol,
                            self.id_unidad,
                            passEncript,
                            self.state,
                            self.image))

        expiracion = datetime.datetime.now() + datetime.timedelta(minutes=30)
        encode = {
            'email':self.mail,
            'expiracion':str(expiracion)
        }

        token_cambio = jwt.encode(encode,KEY_SECRET)
        
        connection.commit()
        body = get_plantilla(self.mail,self.name,passuser,True,token=token_cambio)
        send_mail(self.mail,'Creación Usuario',body)
        return {
            'status':200,
            'msg':'Usuario agregado con exito, se envío un correo con la contraseña y link para realizar cambio.',
            'data':[]
        }

    @postgres_cursor_connection_class
    def update_user(self,cursor,connection):
        if not self._validate_user(cursor,self.mail):
            return {
                'status':400,
                'msg':'Email no existente',
                'data':[]
            }

        query = """UPDATE usuario set nombres = %s, apellido_paterno = %s, apellido_materno = %s, id_rol = %s, id_unidad = %s, estado=%s,imagen=%s where id = %s """
        cursor.execute(query,(
                            self.name,
                            self.last_name,
                            self.second_last_name,
                            self.id_rol,
                            self.id_unidad,
                            self.state,
                            self.image,
                            self.id))
        connection.commit()
        return {
            'status':200,
            'msg':'Usuario modificado con exito',
            'data':[]
        }

    @postgres_cursor_class
    def validate_token(self,cursor,token):
        token_encode = jwt.decode(token,KEY_SECRET)

        hora_expiracion =pd.to_datetime(token_encode['expiracion'])
        if hora_expiracion >= datetime.datetime.now():
            return {
                'status':200,
                'msg':'ok',
                'data':[]
            }
        else:
            return {
                'status':400,
                'msg':'La url para cambiar contraseña ha caducado',
                'data':[]
            }

    @postgres_cursor_connection_class
    def reset_password(self,cursor,connection,token):
        token_encode = jwt.decode(token,KEY_SECRET)

        self.mail = token_encode['email']
        
        query_token_valido = """SELECT token FROM usuario where correo=%s"""
        cursor.execute(query_token_valido,(self.mail,))
        token_value = cursor.fetchone()
        token_value = token_value['token'] if token_value else 0
        if token_value == 0:
            return {
                'status':400,
                'msg':'Ya realizo cambio de contraseña',
                'data':[]
            }

        passEncript = crypt(self.password,'PORTAFOLIO',400)
        query_update_password = """UPDATE usuario set password = %s,token=0 where correo = %s """
        cursor.execute(query_update_password,(passEncript,self.mail))
        connection.commit()
        
        return {
                'status':200,
                'msg':'Contraseña actualizada correctamente',
                'data':[]
            }
    
    @postgres_cursor_connection_class
    def recovery_pass(self,cursor,connection):

        query_existe = """SELECT nombres FROM usuario where correo = %s """
        cursor.execute(query_existe,(self.mail,))
        data = cursor.fetchone()
        if not data:
            return {
                'status':400,
                'msg':'Usuario no encontrado',
                'data':[]
            }
        import datetime
        nombre = data['nombres']

        expiracion = datetime.datetime.now() + datetime.timedelta(minutes=30)
        encode = {
            'email':self.mail,
            'expiracion':str(expiracion)
        }

        token_cambio = jwt.encode(encode,KEY_SECRET)
        print (token_cambio)
        query = """UPDATE usuario SET token=1 WHERE correo = %s"""
        cursor.execute(query,(self.mail,))
        connection.commit()

        body = get_plantilla(self.mail,nombre,creacion=False,token=token_cambio)
        send_mail(self.mail,'Recuperación de Contraseña',body)

        return {
            'status':200,
            'msg':'Se ha enviado un correo para recuperar la contraseña',
            'data':[]
        }

        
    @postgres_cursor_class
    def list_user(self,cursor,company):
        if self.id == 'all':
            query = """SELECT us.* FROM 
                usuario as us
                inner join unidad as un
                on us.id_unidad = un.id
                inner join empresa as em
                on un.id_empresa = em.id
                where em.id = %s"""
            cursor.execute(query,(company,))
        else:
            try:
                query = """SELECT us.* FROM usuario as us
                        inner join unidad as un
                        on us.id_unidad = un.id
                        inner join empresa as em
                        on un.id_empresa = em.id
                        where em.id = %s and us.id=%s """
                cursor.execute(query,(company,self.id))
            except Exception as e:
                return {
                    'status':204,
                    'msg':'Lista de usuarios',
                    'data':[]
                }
        data = cursor.fetchall()
        code = 200 if data else 204
        response = []
        for k in data:
            response.append(
                {
                    'nombre': k['nombres'],
                    'apellido_paterno':k['apellido_paterno'],
                    'apellido_materno':k['apellido_materno'],
                    'id':k['id'],
                    'imagen':k['imagen'].split(',')[1] if k['imagen'] else ''
                }
            )
        return {
            'status':code,
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
        cursor.execute(query,(self.mail,
                            self.password))
        data = cursor.fetchone()
        if not data:
            return {
                'status':204,
                'msg':'Usuario o contraseña incorrectos',
                'data':data
            }
        data['imagen'] = data['imagen'].split(',')[1] if data['imagen'] else ''
        return {
            'status':200,
            'msg':'Login Usuario',
            'data':data
        }

    @postgres_cursor_connection_class
    def delete_user(self,cursor,connection):
        query = """DELETE FROM usuario where id= %s """
        cursor.execute(query,(self.id,))
        connection.commit()

        return {
            'status':200,
            'msg':'Usuario eliminado con exito',
            'data':[]
        }