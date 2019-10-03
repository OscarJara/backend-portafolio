from flask              import Flask
from flask              import request
from flask              import jsonify

from flask_cors         import CORS
from flask_cors         import cross_origin


from view.view_user     import *
import view.view_roles  as role
import view.view_company as company


app = Flask(__name__)
CORS(app)


@app.route('/',methods=['GET'])
def inicial():
    return jsonify(
        {
            'estado':200,
            'glosa':'endpoint inicial ok'
        }
    ),200

### ROLE
@app.route('/roles',methods=['GET'])
def get_rol():
    mail = request.args.get('i')
    return jsonify(role.roles_view(mail))

@app.route('/role',methods=['POST'])
def add_role():
    return jsonify(role.add_role_view(request))

@app.route('/role',methods=['DELETE'])
def delete_role():
    return jsonify(role.delete_role_view(request))

@app.route('/role',methods=['PUT'])
def update_role():
    return jsonify(role.update_role_view(request))

### END ROLE

### USER

@app.route('/user',methods=['POST'])
def add_user():
    return jsonify(add_user_view(request))

@app.route('/user',methods=['GET'])
def get_user():
    id = request.args.get('id')
    company = request.args.get('e')
    return jsonify(list_user_view(id,company))

@app.route('/user',methods=['PUT'])
def update_user():
    return jsonify(update_user_view(request))

@app.route('/delete-user',methods=['POST'])
def delete_user():
    return jsonify(delete_user_view(request))

@app.route('/recovery-password',methods=['POST'])
def recovery():
    return jsonify(recovery_pass_view(request))

@app.route('/new-password',methods=['POST'])
def reset():
    if 'Access-Token' not in request.headers:
        return jsonify(
            {
                'status':401,
                'msg':'autorización fallida',
                'data':[],
                'error':''
            }
        ),401
    return jsonify(reset_password_view(request,dict(request.headers)['Access-Token']))

@app.route('/vd-tkn',methods=['GET'])
def vd_token():
    if 'Access-Token' not in request.headers:
        return jsonify(
            {
                'status':401,
                'msg':'autorización fallida',
                'data':[],
                'error':''
            }
        ),401
    return jsonify(validate_token_view(dict(request.headers)['Access-Token']))

@app.route('/login',methods=['POST'])
def login():
    return jsonify(login_view(request))
    
@app.route('/activate-user',methods=['POST'])
def activate():
    return jsonify(activate_user_view(request))
### END USER


### COMPANY

@app.route('/company',methods=['POST'])
def add_company():
    return jsonify(company.add_company_view(request))

@app.route('/company',methods=['GET'])
def get_company():
    return jsonify(company.get_company_view())

@app.route('/company',methods=['PUT'])
def update_company():
    return jsonify(company.update_company_view(request))

@app.route('/company',methods=['DELETE'])
def delete_company():
    return jsonify(company.delete_company_view(request))

@app.route('/activate-company',methods=['POST'])
def activate_company():
    return jsonify(company.activate_view(request))


@app.route('/organization-chart',methods=['POST'])
def add_company_chart():
    return jsonify(company.add_company_chart_view(request))

@app.route('/organization-chart',methods=['PUT'])
def update_company_chart():
    return jsonify(company.update_company_char_view(request))
    
@app.route('/organization-chart',methods=['DELETE'])
def delete_company_chart():
    return jsonify(company.delete_company_char_view(request))

@app.route('/organization-chart/<id>',methods=['GET'])
def get_company_chart(id):
    
    return jsonify(company.get_company_chart_view(id))
if __name__ == "__main__":
    app.run(debug=True)