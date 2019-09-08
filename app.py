from flask              import Flask
from flask              import request
from flask              import jsonify

from flask_cors         import CORS
from flask_cors         import cross_origin




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


if __name__ == "__main__":
    app.run()