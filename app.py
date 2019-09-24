from flask              import Flask
from flask              import request
from flask              import jsonify

from flask_cors         import CORS
from flask_cors         import cross_origin


from view.view_user     import *



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
    return jsonify(reset_password_view(request,request.headers['Acces-Token']))

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
    return jsonify(validate_token_view(request.headers['Acces-Token']))

@app.route('/login',methods=['POST'])
def login():
    return jsonify(login_view(request))
    
if __name__ == "__main__":
    app.run(debug=True)