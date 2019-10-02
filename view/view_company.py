from models.company import Company


def add_company_view(request):
    name = request.json['nombre']
    adress = request.json['direccion']
    city = request.json['ciudad']
    rut = request.json['rut']
    status = request.json['estado']

    company = Company(
        name = name,
        adress = adress,
        city = city,
        rut = rut,
        status = status
    )
    return company.add_company()

def update_company_view(request):
    id = request.json['id']
    name = request.json['nombre']
    adress = request.json['direccion']
    city = request.json['ciudad']
    rut = request.json['rut']
    status = request.json['estado']

    company = Company(
        id = id,
        name = name,
        adress = adress,
        city = city,
        rut = rut,
        status = status
    )
    return company.update_company()

def delete_company_view(request):
    id = request.json['id']

    company = Company(
        id=id
    )

    return company.delete_company()

def get_company_view():

    return Company().get_company()

def activate_view(request):
    id = request.json['id']
    company = Company(
        id=id
    )

    return company.activate_company()



def add_company_chart_view(request):
    id = request.json['id']
    organization_chart = request.json['jerarquia']
    company = Company(
        id=id,
        organization_chart=organization_chart
    )
    return company.add_company_chart()  

def update_company_char_view(request):
    id = request.json['id']
    organization_chart = request.json['jerarquia']
    company = Company(
        id=id,
        organization_chart=organization_chart
    )
    return company.update_company_char()

def delete_company_char_view(request):
    id = request.json['id']
    company = Company(
        id=id
    )
    
    return company.delete_company_char()

# add_company
# update_company
# delete_company
# get_company