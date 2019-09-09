from models.User    import User
from pbkdf2   import crypt
from flask import request

def add_user_view(request):
    mail= request.json['email']
    name= request.json['nombre']
    last_name= request.json['apellido_p']
    second_last_name= request.json['apellido_m']
    id_rol= request.json['id_rol']
    id_unidad= request.json['id_unidad']
    password= crypt(request.json['password'],'PORTAFOLIO',400)
    state= True if request.json['estado'] == 1 else False
    image=request.json['imagen']
    user = User(
        mail=mail,
        name=name,
        last_name=last_name,
        second_last_name=second_last_name,
        id_rol=id_rol,
        id_unidad=id_unidad,
        password=password,
        state=state,
        image=image
    )

    return user.add_user()


def list_user_view():
    user = User()
    return user.list_user()

def delete_user_view(request):
    
    id = request.json['id']
    user = User(id=id)
    return user.delete_user()
def login_view(request):
    mail = request.json['email']
    password = crypt(request.json['password'],'PORTAFOLIO',400)
    print (password)
    user = User(
        mail=mail,
        password=password
    )

    return user.login()