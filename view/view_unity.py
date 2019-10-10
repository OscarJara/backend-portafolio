from models.unity import Unity

def unity_view(empresa):
    unity = Unity(
        company=empresa
    )
    return unity.get_unity()

def add_unity_view(request):
    name = request.json['nombre']
    empresa = request.json['empresa']

    unity = Unity(
        name=name,
        company=empresa
    )

    return unity.add_unity()

def delete_unity_view(request):
    id = request.json['id']

    unity = Unity(
        id=id
    )

    return unity.delete_unity()

def update_unity_view(request):
    id = request.json['id']
    name = request.json['nombre']

    unity = Unity(
        id=id,
        name=name
    )

    return unity.update_unity()