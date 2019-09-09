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
    return jsonify(list_user_view())

@app.route('/delete-user',methods=['POST'])
def delete_user():
    return jsonify(delete_user_view(request))
@app.route('/login',methods=['POST'])
def login():
    return jsonify(login_view(request))
    
if __name__ == "__main__":
    app.run(debug=True)