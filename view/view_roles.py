from models.roles import Role

def roles_view(mail):
    return Role().get_roles(mail)

def add_role_view(request):
    name = request.json['nombre']
    description = request.json['descripcion']
    empresa = request.json['empresa']

    rol = Role(
        name=name,
        description=description,
        empresa=empresa
    )

    return rol.add_role()

def delete_role_view(request):
    id = request.json['id']

    rol = Role(
        id=id
    )

    return rol.delete_role()

def update_role_view(request):
    id = request.json['id']
    name = request.json['nombre']
    description = request.json['descripcion']

    rol = Role(
        id=id,
        name=name,
        description=description
    )

    return rol.update_role()