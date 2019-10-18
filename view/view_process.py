from models.process import Process

def view_create_process(request):
    name = request.json['nombre']
    company = request.json['empresa']
    detail = request.json['detalle']
    start_date = request.json['fecha_inicio']
    end_date = request.json['fecha_termino']

    process = Process(
        name=name,
        company=company,
        detail=detail,
        start_date=start_date,
        end_date=end_date   
    )
    return process.add_process()
def view_delete_process(request):
    id = request.json['id']
    company =  request.json['empresa']
    process = Process(
        id=id,
        company=company
    )
    return process.delete_process()

def view_update_process(request):
    id = request.json['id']
    name = request.json['nombre']
    company = request.json['empresa']
    detail = request.json['detalle']
    start_date = request.json['fecha_inicio']
    end_date = request.json['fecha_termino']

    process = Process(
        id=id,
        name=name,
        company=company,
        detail=detail,
        start_date=start_date,
        end_date=end_date   
    )
    return process.update_process()

def view_get_process(id,limit,offset):
    process = Process(
        company=id
    )
    return process.get_process(limit,offset)
# process = Process(
        
    #     name='Prueba',
    #     company=5,
    #     detail='PRUEBA',
    #     start_date='2019-05-05',
    #     end_date='2019-05-05'
    # )
    # print(process.add_process())
    # process = Process(id=1,company=5)
    # print(process.delete_process())

    # process = Process(
    #     id=2,
    #     name='Prueba CAMBIO',
    #     company=5,
    #     detail='PRUEBA',
    #     start_date='2019-05-05',
    #     end_date='2019-05-05'
    # )
    # print(process.update_process())

    process = Process(
        company=5
    )
    print(    process.get_process())