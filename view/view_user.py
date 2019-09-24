from models.User    import User
from pbkdf2   import crypt
from flask import request

import base64


def add_user_view(request):
    mail= request.json['email']
    name= request.json['nombre']
    last_name= request.json['apellido_p']
    second_last_name= request.json['apellido_m']
    id_rol= request.json['id_rol']
    id_unidad= request.json['id_unidad']
    state= True if request.json['estado'] == 1 else False
    image=request.json['imagen']
    user = User(
        mail=mail,
        name=name,
        last_name=last_name,
        second_last_name=second_last_name,
        id_rol=id_rol,
        id_unidad=id_unidad,
        state=state,
        image=image
    )

    return user.add_user()

def recovery_pass_view(request):
    mail = request.json['email']

    user = User(
        mail=mail
    )

    return user.recovery_pass()
    
def list_user_view(id,company):
    user = User(
        id=id
    )
    return user.list_user(company)

def delete_user_view(request):
    
    id = request.json['id']
    user = User(id=id)
    return user.delete_user()

def reset_password_view(request,token):
    new_password = request.json['password']
    acces_token = token


    user = User(
        password=new_password
    )

    return user.reset_password(acces_token)

def login_view(request):
    mail = request.json['email']
    password = crypt(request.json['password'],'PORTAFOLIO',400)
    user = User(
        mail=mail,
        password=password
    )

    return user.login()

def validate_token_view(token):

    return User().validate_token(token)

def update_user_view(request):
    mail = request.json['email']
    name= request.json['nombre']
    last_name= request.json['apellido_p']
    second_last_name= request.json['apellido_m']
    id_rol= request.json['id_rol']
    id_unidad= request.json['id_unidad']
    state= True if request.json['estado'] == 1 else False
    image=request.json['imagen']
    id = request.json['id']

    user = User(
        id=id,
        mail=mail,
        name=name,
        last_name=last_name,
        second_last_name=second_last_name,
        id_rol=id_rol,
        id_unidad=id_unidad,
        state=state,
        image=image
    )

    return user.update_user()

def roles_view(mail):
    return User().get_roles(mail)